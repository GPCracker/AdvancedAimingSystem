__application__ = ('Advanced Aiming System Mod', 'AdvancedAimingSystem', 'GPCracker.AdvancedAimingSystem')
__official_topic__ = 'http://www.koreanrandom.com/forum/topic/16559-/'
__authors__ = ('GPCracker', )
__version__ = ('<<version>>', None)
__xmodlib__ = ('v0.1.15', None)
__client__ = (('ru', ), '<<client>>')

# ---------------------- #
#    Application info    #
# ---------------------- #
if __name__ == '__main__':
	appinfo = '{appname} ({appid}) {version} ({client} {clusters}) by {authors}'.format(
		appname = __application__[0],
		appid = __application__[2],
		version = __version__[0],
		client = __client__[1],
		clusters = ', '.join(__client__[0]).upper(),
		authors = ', '.join(__authors__)
	)
	import sys, time
	print >> sys.stdout, appinfo
	time.sleep(len(appinfo) * 0.05)
	sys.exit(0)

# -------------------------------------- #
#    X-Mod Library compatibility test    #
# -------------------------------------- #
import XModLib
if not XModLib.isCompatibleLibVersion(__xmodlib__):
	raise ImportError('XModLib version does not suit this version of application')
