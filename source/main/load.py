# *************************
# Application loading
# *************************
def delayedCall(timeout, function, args=(), kwargs={}, daemon=False):
	timer = threading.Timer(timeout, function, args, kwargs)
	timer.daemon = daemon
	timer.start()
	return timer

def loadApplication():
	global _config_
	_config_ = readConfig()
	if not _config_['ignoreClientVersion'] and not XModLib.ClientInfo.ClientInfo.isCompatibleClientVersion(__client__):
		_globals_['appResultMessage'] = _config_['appFailedMessage']
		print '[{0[1]}] {0[0]} {1}'.format(__application__, 'is incompatible with current client version.')
	elif _config_['applicationEnabled']:
		_globals_['appResultMessage'] = _config_['appLoadedMessage']
		print '[{0[1]}] {0[0]} {1}'.format(__application__, 'successfully loaded.')
		delayedCall(_config_['hookInjectTimeout'], _inject_hooks_, daemon=True)
	delayedCall(_config_['hookInjectTimeout'], _inject_loads_, daemon=True)
	return

# *************************
# Application start
# *************************
loadApplication()
