# *************************
# Application loading
# *************************
def loadApplication():
	global _config_
	_config_ = readConfig()
	if _config_['ignoreClientVersion'] or XModLib.ClientInfo.ClientInfo.isCompatibleClientVersion(__client__):
		if _config_['applicationEnabled']:
			_globals_['appResultMessage'] = _config_['appLoadedMessage']
			print '[{0[1]}] {0[0]} {1}'.format(__application__, 'successfully loaded.')
			BigWorld.callback(_config_['hookInjectTimeout'], _inject_hooks_)
	else:
		_globals_['appResultMessage'] = _config_['appFailedMessage']
		print '[{0[1]}] {0[0]} {1}'.format(__application__, 'is incompatible with current client version.')
	return

# *************************
# Application start
# *************************
loadApplication()
