exec '''
# *************************
# Loading original module
# *************************
import os
import marshal

g_original_file = os.path.normpath(os.path.join('res', __file__)).replace(os.sep, '/')
if not os.path.isfile(g_original_file):
	raise IOError('Original file could not be found. Module loading impossible.')
with open(g_original_file, 'rb') as f:
	exec marshal.loads(f.read()[8:]) in target_globals, target_locals
''' in dict(globals(), target_globals=globals(), target_locals=locals()), dict(locals())

# *************************
# Loading Python mods
# *************************
import mods
