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

def compileSource(source, filename = '<string>', filetime = time.time()):
	with io.BytesIO() as bytesIO:
		bytesIO.write(imp.get_magic())
		bytesIO.write(struct.pack('<I', int(filetime)))
		bytesIO.write(marshal.dumps(compile(source, filename, 'exec')))
		result = bytesIO.getvalue()
	return result

def compileLocalization(src_file, bin_file):
	return subprocess.call(['tools/gettext/bin/msgfmt.exe', src_file, '-o', bin_file])

def joinPath(*args, **kwargs):
	return os.path.normpath(os.path.join(*args, **kwargs)).replace(os.sep, '/')

def sourceIterator(src_list):
	for source in src_list:
		if os.path.isfile(source):
			yield joinPath(source)
		elif os.path.isdir(source):
			for root, dirs, files in os.walk(source):
				root = os.path.relpath(root, source)
				for file in files:
					yield joinPath(source, root, file)
	return

def processSource(src_file, encoding='utf-8'):
	print '{0} --> {1}'.format(src_file, '<source>')
	with open(src_file, 'rb') as f:
		src_text = f.read().decode(encoding)
	return src_text

def getSource(src_list, encoding='utf-8'):
	processor = functools.partial(processSource, encoding=encoding)
	return '\n'.join(map(processor, src_list))

def processScript(source, src_file, bin_file, zip_file, fzip, filename, encoding='utf-8'):
	print '{0} --> {1}'.format('<source>', src_file)
	print '{0} --> {1}'.format(src_file, bin_file)
	print '{0} --> {1}'.format(bin_file, '<release>')
	if not os.path.isdir(os.path.dirname(src_file)):
		os.makedirs(os.path.dirname(src_file))
	if not os.path.isdir(os.path.dirname(bin_file)):
		os.makedirs(os.path.dirname(bin_file))
	with open(src_file, 'wb') as f:
		f.write(source.encode(encoding))
	with open(bin_file, 'wb') as f:
		f.write(compileSource(source, filename, os.path.getmtime(src_file)))
	fzip.write(bin_file, zip_file)
	return

def resourceIterator(res_list):
	for resource, target in res_list:
		if os.path.isfile(resource):
			yield (
				joinPath(resource),
				joinPath(target)
			)
		elif os.path.isdir(resource):
			for root, dirs, files in os.walk(resource):
				root = os.path.relpath(root, resource)
				for file in files:
					yield (
						joinPath(resource, root, file),
						joinPath(target, root, file)
					)
	return

def processResource(src_file, zip_file, fzip):
	print '{0} --> {1}'.format(src_file, '<release>')
	fzip.write(src_file, zip_file)
	return

def processLocalization(src_file, bin_file, zip_file, fzip):
	print '{0} --<msgfmt>--> {1}'.format(src_file, '<release>')
	if compileLocalization(src_file, bin_file):
		raise RuntimeError('An error occured while compiling localization file.')
	fzip.write(bin_file, zip_file)
	return

if __name__ == '__main__':
	try:
		cfg_file = joinPath(os.path.splitext(__file__)[0] + '.cfg')
		with open(cfg_file, 'rb') as f:
			config = json.loads(f.read())
		vcs_file = joinPath(os.path.dirname(__file__), 'version.cfg')
		version = '<custom_build>'
		if os.path.isfile(vcs_file):
			with open(vcs_file, 'r+b') as f:
				vcs_info = json.load(f)
				version = '{release}#{next_build}'.format(**vcs_info)
				vcs_info['next_build'] += 1
				f.seek(0)
				f.truncate()
				f.write(json.dumps(vcs_info) + '\n')
		application = config["application"]
		versionMacros = config["versionMacros"]
		clientVersion = config["clientVersion"]
		encoding = config["encoding"]
		buildPath = config["buildPath"].replace('<client>', clientVersion)
		releasePath = config["releasePath"].replace('<client>', clientVersion)
		zipPath = config["zipPath"].replace('<client>', clientVersion)
		sources = config["sources"]
		resources = config["resources"]
		localizations = config["localizations"]
		if os.path.isdir(buildPath):
			shutil.rmtree(buildPath)
		if os.path.isdir(releasePath):
			shutil.rmtree(releasePath)
		os.makedirs(buildPath)
		os.makedirs(releasePath)
		with zipfile.ZipFile(os.path.join(releasePath, application + '.zip').replace(os.sep, '/'), 'w', zipfile.ZIP_DEFLATED) as fzip:
			src_file = joinPath(buildPath, '{0}.py'.format(application))
			bin_file = joinPath(buildPath, '{0}.pyc'.format(application))
			zip_file = joinPath(zipPath, '{0}.pyc'.format(application))
			script = getSource(sourceIterator(sources), encoding).replace(versionMacros, version)
			processScript(script, src_file, bin_file, zip_file, fzip, '{0}.py'.format(application), encoding)
			for src_file, zip_file in resourceIterator(resources):
				processResource(src_file, zip_file.replace('<client>', clientVersion), fzip)
			for src_file, zip_file in resourceIterator(localizations):
				bin_file = joinPath(buildPath, os.path.splitext(os.path.basename(src_file))[0] + '.mo')
				processLocalization(src_file, bin_file, zip_file.replace('<client>', clientVersion), fzip)
	except:
		traceback.print_exc()
