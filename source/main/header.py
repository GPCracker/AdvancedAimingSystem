__application__ = ('Advanced Aiming System Mod', 'AdvancedAimingSystem', 'GPCracker.AdvancedAimingSystem')
__official_topic__ = 'http://www.koreanrandom.com/forum/topic/16559-/'
__authors__ = ('GPCracker', )
__version__ = '<<version>>'
__xmodlib__ = ('v0.1.9', None)
__client__ = (('ru', ), '<<client>>', None)

# *************************
# Application info
# *************************
if __name__ == '__main__':
	applicationInfo = '{appname} ({appshort}) {version} ({client} {clusters}) by {authors}'.format(
		appname = __application__[0],
		appshort = __application__[1],
		version = __version__,
		client = __client__[1],
		clusters = ', '.join(__client__[0]).upper(),
		authors = ', '.join(__authors__)
	)
	print applicationInfo
	__import__('time').sleep(len(applicationInfo) * 0.05)
	exit()

# *************************
# X-Mod Library
# *************************
import XModLib
if not XModLib.isCompatibleLibVersion(__xmodlib__):
	raise ImportError('XModLib version does not suit this version of application.')
