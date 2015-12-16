import io
import os
import imp
import json
import time
import shutil
import struct
import marshal
import zipfile
import traceback

def compileSource(source, filename = '<string>', filetime = time.time()):
	with io.BytesIO() as bytesIO:
		bytesIO.write(imp.get_magic())
		bytesIO.write(struct.pack('I', int(filetime)))
		bytesIO.write(marshal.dumps(compile(source, filename, 'exec')))
		result = bytesIO.getvalue()
	return result

def getPath(*args, **kwargs):
	return os.path.normpath(os.path.join(*args, **kwargs)).replace(os.sep, '/')

def sourceIterator(src_list):
	for source in src_list:
		if os.path.isfile(source):
			yield getPath(source)
		elif os.path.isdir(source):
			for root, dirs, files in os.walk(source):
				root = os.path.relpath(root, source)
				for file in files:
					yield getPath(source, root, file)
	return

def processSource(src_file):
	print '{0} --> {1}'.format(src_file, '<source>')
	with open(src_file, 'rt') as f:
		src_text = f.read()
	return src_text

def getSource(src_list):
	return '\n'.join(map(processSource, src_list))

def processScript(source, src_file, bin_file, zip_file, fzip, filename):
	print '{0} --> {1}'.format('<source>', src_file)
	print '{0} --> {1}'.format(src_file, bin_file)
	print '{0} --> {1}'.format(bin_file, '<release>')
	if not os.path.isdir(os.path.dirname(src_file)):
		os.makedirs(os.path.dirname(src_file))
	if not os.path.isdir(os.path.dirname(bin_file)):
		os.makedirs(os.path.dirname(bin_file))
	with open(src_file, 'wt') as f:
		f.write(source)
	with open(bin_file, 'wb') as f:
		f.write(compileSource(source, filename, os.path.getmtime(src_file)))
	fzip.write(bin_file, zip_file)
	return

def resourceIterator(res_list):
	for resource, target in res_list:
		if os.path.isfile(resource):
			yield (
				getPath(resource),
				getPath(target)
			)
		elif os.path.isdir(resource):
			for root, dirs, files in os.walk(resource):
				root = os.path.relpath(root, resource)
				for file in files:
					yield (
						getPath(resource, root, file),
						getPath(target, root, file)
					)
	return

def processResource(src_file, zip_file, fzip):
	print '{0} --> {1}'.format(src_file, '<release>')
	fzip.write(src_file, zip_file)
	return

if __name__ == '__main__':
	try:
		cfg_file = (os.path.splitext(__file__)[0] + '.cfg').replace(os.sep, '/')
		with open(cfg_file, 'rt') as f:
			config = json.load(f)
		application = config["application"]
		buildPath = config["buildPath"]
		releasePath = config["releasePath"]
		zipPath = config["zipPath"]
		sources = config["sources"]
		resources = config["resources"]
		if os.path.isdir(buildPath):
			shutil.rmtree(buildPath)
		if os.path.isdir(releasePath):
			shutil.rmtree(releasePath)
		os.makedirs(buildPath)
		os.makedirs(releasePath)
		with zipfile.ZipFile(os.path.join(releasePath, application + '.zip').replace(os.sep, '/'), 'w', zipfile.ZIP_DEFLATED) as fzip:
			src_file = getPath(buildPath, '{0}.py'.format(application))
			bin_file = getPath(buildPath, '{0}.pyc'.format(application))
			zip_file = getPath(zipPath, '{0}.pyc'.format(application))
			processScript(getSource(list(sourceIterator(sources))), src_file, bin_file, zip_file, fzip, '{0}.py'.format(application))
			for src_file, zip_file in resourceIterator(resources):
				processResource(src_file, zip_file, fzip)
	except:
		traceback.print_exc()
