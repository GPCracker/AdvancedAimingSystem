exec '''
# *************************
# Loading original module
# *************************
import os, re, imp, sys, zipimport
g_original_loader = zipimport.zipimporter(
	os.path.normpath(os.path.join(
		'res/packages/scripts.pkg',
		re.sub('{0}(?:{1})$'.format(re.escape('__init__'), '|'.join(re.escape(suffix[0]) for suffix in imp.get_suffixes())), '', __file__),
		os.path.relpath('.', __name__.replace('.', '/'))
	)).replace(os.sep, '/')
).find_module(__name__, __package__)
if g_original_loader is None:
	raise IOError('Original module could not be found. Module loading impossible.')
exec g_original_loader.get_code(__name__) in target_globals, target_locals
''' in dict(globals(), target_globals=globals(), target_locals=locals())

# *************************
# Loading Python mods
# *************************
import mods
