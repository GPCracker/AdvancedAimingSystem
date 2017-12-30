# -------------------------------------- #
#    Application plug-ins initializer    #
# -------------------------------------- #
def initApplicationPlugins(targetGlobals=globals(), targetLocals=locals()):
	for dirpath, dirnames, filenames in XModLib.EngineUtils.walkResMgrTree('mods/{0}/plugins'.format(__application__[2])):
		for filename in filenames:
			if os.path.splitext(filename)[1] == '.pyc':
				pluginContent = XModLib.EngineUtils.getResMgrBinaryFileContent(XModLib.EngineUtils.joinResMgrPath(dirpath, filename))
				if pluginContent is not None:
					pluginCodeObject = marshal.loads(pluginContent[8:])
					pluginName = os.path.splitext(pluginCodeObject.co_filename)[0]
					print '[{0}] Trying to load plug-in {1}...'.format(__application__[1], pluginName)
					exec(pluginCodeObject, targetGlobals, targetLocals)
					print '[{0}] Plug-in {1} successfully loaded.'.format(__application__[1], pluginName)
	return

# ------------------------------- #
#    Application plug-ins init    #
# ------------------------------- #
initApplicationPlugins()
