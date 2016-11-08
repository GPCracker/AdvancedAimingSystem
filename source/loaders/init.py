# *************************
# Python
# *************************
import os
import importlib
import traceback

# *************************
# BigWorld
# *************************
import ResMgr

# *************************
# Required functions
# *************************
def getModulesIterator(initfile, package):
	dirname, basename = os.path.split(initfile)
	dirname = os.path.relpath(ResMgr.resolveToAbsolutePath(dirname)).replace(os.sep, '/')
	if not os.path.isdir(dirname):
		raise IOError('Path \'{}\' does not exist.'.format(dirname))
	for entry in os.listdir(dirname):
		if entry == basename:
			continue
		name, extension = os.path.splitext(entry)
		entry = os.path.join(dirname, entry).replace(os.sep, '/')
		if os.path.isfile(entry) and extension == '.pyc' or os.path.isdir(entry) and os.path.isfile(os.path.join(entry, '__init__.pyc')):
			yield package + '.' + name
	return

# *************************
# Modules loading routine
# *************************
print '[PyMod] Python mods loading started.'
for module in getModulesIterator(__file__, __name__):
	print '[PyMod] Importing module \'{}\'...'.format(module)
	try:
		importlib.import_module(module)
	except:
		traceback.print_exc()
		print '[PyMod] Exception in module \'{}\', skipping.'.format(module)
print '[PyMod] Python mods loading completed.'
