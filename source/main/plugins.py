# *************************
# Application plug-ins initializer
# *************************
def initApplicationPlugins(targetGlobals=globals(), targetLocals=locals()):
	archiveFile = XModLib.EngineUtils.resolveResMgrPath(__file__)
	with zipfile.ZipFile(archiveFile, 'r') as fzip:
		for pluginFile in fzip.namelist():
			pluginName, pluginExt = os.path.splitext(pluginFile)
			if pluginExt == '.pyc':
				print '[{0}] Trying to load plug-in {1}...'.format(__application__[1], pluginName)
				exec(marshal.loads(fzip.read(pluginFile)[8:]), targetGlobals, targetLocals)
				print '[{0}] Plug-in {1} successfully loaded.'.format(__application__[1], pluginName)
	return

# *************************
# Application plug-ins init
# *************************
initApplicationPlugins()
