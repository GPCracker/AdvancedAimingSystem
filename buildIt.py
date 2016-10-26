import io
import os
import imp
import json
import time
import shutil
import struct
import marshal
import zipfile
import functools
import traceback
import subprocess

def compile_python_string(source, filename='<string>', filetime=time.time()):
	with io.BytesIO() as dst_bin_buffer:
		dst_bin_buffer.write(imp.get_magic())
		dst_bin_buffer.write(struct.pack('<I', int(filetime)))
		dst_bin_buffer.write(marshal.dumps(compile(source, filename, 'exec')))
		dst_bin_data = dst_bin_buffer.getvalue()
	return dst_bin_data

def compile_gettext_string(src_bin_data):
	if os.name == 'posix':
		msgfmt = 'msgfmt'
	elif os.name == 'nt':
		msgfmt = 'tools/gettext/bin/msgfmt.exe'
	else:
		raise RuntimeError('Current operation system is not supported.')
	gettext_process = subprocess.Popen([msgfmt, '-', '-o', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	dst_bin_data = gettext_process.communicate(src_bin_data)[0]
	if gettext_process.poll():
		raise RuntimeError('An error occured while compiling localization file.')
	return dst_bin_data

def compile_zipfile_string(src_data_blocks):
	with io.BytesIO() as dst_bin_buffer:
		with zipfile.ZipFile(dst_bin_buffer, 'w', zipfile.ZIP_DEFLATED) as dst_zip_buffer:
			for src_block_name, src_block_data in src_data_blocks:
				dst_zip_buffer.writestr(src_block_name, src_block_data)
		dst_bin_data = dst_bin_buffer.getvalue()
	return dst_bin_data

def acquire_version_data(vcs_filename):
	vcs_str_data = '<custom_build>'
	if os.path.isfile(vcs_filename):
		with open(vcs_filename, 'r+b') as vcs_bin_buffer:
			vcs_obj_data = json.load(vcs_bin_buffer)
			vcs_str_data = '{release}#{next_build}'.format(**vcs_obj_data)
			vcs_obj_data['next_build'] += 1
			vcs_bin_buffer.seek(0)
			vcs_bin_buffer.truncate()
			vcs_bin_buffer.write(json.dumps(vcs_obj_data) + '\n')
	return vcs_str_data

def merge_dicts(base, *args, **kwargs):
	result = base.copy()
	map(result.update, args)
	result.update(**kwargs)
	return result

def format_macros(string, macros):
	for macro, replace in macros.items():
		string = string.replace(macro, replace)
	return string

def join_path(*args, **kwargs):
	path = os.path.normpath(os.path.join(*args, **kwargs)).replace(os.sep, '/')
	return path + ('/' if os.path.isdir(path) else '')

def norm_path(path):
	path = os.path.normpath(path).replace(os.sep, '/')
	return path + ('/' if os.path.isdir(path) else '')

def get_path_iterator(path_group, home='./'):
	_path = join_path(home, path_group)
	if os.path.isfile(_path):
		yield norm_path('./')
	elif os.path.isdir(_path):
		for root, dirs, files in os.walk(_path):
			root = os.path.relpath(root, _path)
			for file in files:
				yield join_path(root, file)
	return

def get_path_groups_iterator(path_groups, home='./'):
	for path_group in path_groups:
		for path in get_path_iterator(path_group, home):
			yield join_path(path_group, path)
	return

def get_path_blocks_iterator(path_blocks, home='./'):
	for path_block in path_blocks:
		for path in get_path_iterator(path_block[0], home):
			yield [join_path(base, path) for base in path_block]
	return

def load_file_data(src_filename):
	with open(src_filename, 'rb') as src_bin_buffer:
		dst_bin_data = src_bin_buffer.read()
	return dst_bin_data

def load_file_str(src_filename, encoding='acsii'):
	return unicode(load_file_data(src_filename), encoding=encoding)

def save_file_data(dst_filename, src_bin_data):
	if not os.path.isdir(os.path.dirname(dst_filename)):
		os.makedirs(os.path.dirname(dst_filename))
	with open(dst_filename, 'wb') as dst_bin_buffer:
		dst_bin_buffer.write(src_bin_data)
	return

def save_file_str(dst_filename, src_str_data, encoding='acsii'):
	save_file_data(dst_filename, src_str_data.encode(encoding=encoding))
	return

def load_source_string(src_filenames, source_encoding='acsii'):
	return u'\n'.join([load_file_str(src_filename, encoding=source_encoding) for src_filename in get_path_groups_iterator(src_filenames)])

if __name__ == '__main__':
	try:
		# Reading configuration.
		cfg_filename = join_path(os.path.splitext(__file__)[0] + '.cfg')
		with open(cfg_filename, 'rb') as cfg_bin_buffer:
			g_config = json.loads(cfg_bin_buffer.read())
		# Printing status.
		print 'Build config file loaded.'
		# Reading build version.
		vcs_filename = join_path(os.path.dirname(__file__), 'version.cfg')
		g_version = acquire_version_data(vcs_filename)
		# Printing status.
		print 'Acquired new version for build: {}.'.format(g_version)
		# Loading macros.
		g_globalMacros = {macro: format_macros(replace, {'<version>': g_version}) for macro, replace in g_config["globalMacros"].items()}
		g_pathsMacros = {macro: format_macros(replace, g_globalMacros) for macro, replace in g_config["pathsMacros"].items()}
		g_allMacros = merge_dicts(g_globalMacros, g_pathsMacros)
		# Cleanup previous build.
		for cleanup in g_config["cleanup"]:
			cleanup = norm_path(format_macros(cleanup, g_allMacros))
			# Printing status.
			print 'Cleaning build path: {}.'.format(cleanup)
			# Removing all content.
			if os.path.isdir(cleanup):
				shutil.rmtree(cleanup)
			# Creating new folder.
			os.makedirs(cleanup)
		# Loading source encoding.
		g_sourceEncoding = g_config["sourceEncoding"]
		# Source group build command.
		def g_buildSourceGroup(src_group, src_plugins=None, level=0):
			# Parsing source group.
			cmp_filename, src_filenames, asm_filename, bin_filename, zip_filename = src_group
			# Formatting macros.
			cmp_filename = norm_path(format_macros(cmp_filename, g_allMacros))
			src_filenames = [norm_path(format_macros(src_filename, g_allMacros)) for src_filename in src_filenames]
			asm_filename = norm_path(format_macros(asm_filename, g_allMacros))
			bin_filename = norm_path(format_macros(bin_filename, g_allMacros))
			zip_filename = norm_path(format_macros(zip_filename, g_allMacros))
			# Printing status.
			indent = ' ' * level
			print indent + 'Building source group to single file: {}.'.format(cmp_filename)
			for src_filename in get_path_groups_iterator(src_filenames):
				print indent + ' Source file: {}.'.format(src_filename)
			print indent + ' Target assembled file: {}.'.format(asm_filename)
			print indent + ' Target binary file: {}.'.format(bin_filename)
			print indent + ' Target zip archive file: {}.'.format(zip_filename)
			print indent + ' Building binaries {} plug-ins.'.format('with' if src_plugins is not None else 'without')
			# Loading source as single block.
			src_str_data = format_macros(load_source_string(src_filenames, g_sourceEncoding), g_globalMacros)
			# Saving assembled file.
			save_file_str(asm_filename, src_str_data, g_sourceEncoding)
			# Getting parameters for compiler.
			cmp_filetime = os.path.getmtime(asm_filename)
			# Compiling source block.
			dst_bin_data = compile_python_string(src_str_data, cmp_filename, cmp_filetime)
			# Attaching plug-in.
			if src_plugins is not None and cmp_filename in src_plugins:
				dst_bin_data += src_plugins[cmp_filename]
			# Saving binary file.
			save_file_data(bin_filename, dst_bin_data)
			# Returning archive block.
			return zip_filename, dst_bin_data
		# Plug-in build command.
		def g_buildPluginAttachGroup(att_group, level=0):
			# Parsing resource entry.
			att_filename, src_groups = att_group
			# Formatting macros.
			att_filename = norm_path(format_macros(att_filename, g_allMacros))
			# Printing status.
			indent = ' ' * level
			print indent + 'Building plug-in attach group: {}.'.format(att_filename)
			# Building zip archive attachment.
			dst_bin_data = compile_zipfile_string([g_buildSourceGroup(src_group, level=level + 1) for src_group in src_groups])
			return att_filename, dst_bin_data
		# Resource build command.
		def g_buildResourceEntry(src_entry, level=0):
			# Parsing resource entry.
			src_bin_filename, dst_zip_filename = src_entry
			# Formatting macros.
			src_bin_filename = norm_path(format_macros(src_bin_filename, g_allMacros))
			dst_zip_filename = norm_path(format_macros(dst_zip_filename, g_allMacros))
			# Printing status.
			indent = ' ' * level
			print indent + 'Building resource file: {}.'.format(src_bin_filename)
			print indent + ' Target zip archive file: {}.'.format(dst_zip_filename)
			# Loading binary file.
			dst_bin_data = load_file_data(src_bin_filename)
			# Returning archive block.
			return dst_zip_filename, dst_bin_data
		# Localization build command.
		def g_buildLocalizationEntry(src_entry, level=0):
			# Parsing localization entry.
			src_filename, bin_filename, zip_filename = src_entry
			# Formatting macros.
			src_filename = norm_path(format_macros(src_filename, g_allMacros))
			bin_filename = norm_path(format_macros(bin_filename, g_allMacros))
			zip_filename = norm_path(format_macros(zip_filename, g_allMacros))
			# Printing status.
			indent = ' ' * level
			print indent + 'Building localization file: {}.'.format(src_filename)
			print indent + ' Target binary file: {}.'.format(bin_filename)
			print indent + ' Target zip archive file: {}.'.format(zip_filename)
			# Loading portable object file.
			src_bin_data = load_file_data(src_filename)
			# Compiling portable object file.
			dst_bin_data = compile_gettext_string(src_bin_data)
			# Saving binary file.
			save_file_data(bin_filename, dst_bin_data)
			# Returning archive block.
			return zip_filename, dst_bin_data
		# Printing status.
		print 'Plug-ins build started.'
		# Building plug-ins.
		g_sourcePlugins = dict(g_buildPluginAttachGroup(att_group, level=1) for att_group in g_config["plugins"])
		# Creating release archive data blocks storage.
		g_releaseBlocks = list()
		# Printing status.
		print 'Source build started.'
		# Building and adding sources.
		g_releaseBlocks.extend([g_buildSourceGroup(src_group, g_sourcePlugins, level=1) for src_group in g_config["sources"]])
		# Printing status.
		print 'Resource build started.'
		# Adding resources.
		g_releaseBlocks.extend([g_buildResourceEntry(src_entry, level=1) for src_entry in get_path_blocks_iterator(g_config["resources"])])
		# Printing status.
		print 'Localization build started.'
		# Compiling and adding localization.
		g_releaseBlocks.extend([g_buildLocalizationEntry(src_entry, level=1) for src_entry in get_path_blocks_iterator(g_config["localizations"])])
		# Loading release archive filename.
		g_releaseArchive = format_macros(g_config["releaseArchive"], g_allMacros)
		# Printing status.
		print 'Saving release archive.'
		# Saving release archive file.
		save_file_data(g_releaseArchive, compile_zipfile_string(g_releaseBlocks))
		# Build finished.
		print 'Build finished.'
	except:
		traceback.print_exc()
