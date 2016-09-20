# *************************
# Application initializer
# *************************
def initApplication():
	_globals_['i18nCache'] = XModLib.TextUtils.TranslatorsCache()
	_globals_['i18nFormatter'] = XModLib.TextUtils.TranslatorFormatter(_globals_['i18nCache'])
	_globals_['macrosFormatter'] = XModLib.TextUtils.MacrosFormatter()
	global _config_
	_config_ = readConfig()
	if not _config_['ignoreClientVersion'] and not XModLib.ClientInfo.ClientInfo.isCompatibleClientVersion(__client__):
		print '[{0[1]}] {0[0]} is incompatible with current client version.'.format(__application__)
		_globals_['appResultMessage'] = _config_['appFailedMessage']
	elif _config_['applicationEnabled']:
		print '[{0[1]}] {0[0]} successfully loaded.'.format(__application__)
		_globals_['appResultMessage'] = _config_['appLoadedMessage']
		_inject_chain_.append(_inject_hooks_)
	_inject_chain_.insert(0, _inject_loads_)
	_inject_inits_()
	return

# *************************
# Application init
# *************************
initApplication()
