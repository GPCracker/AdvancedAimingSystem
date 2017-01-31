# *************************
# Application initializer
# *************************
def initApplication():
	global _inject_chain_
	_inject_chain_ += _inject_loads_
	if not _config_['ignoreClientVersion'] and False:
		print '[{0[1]}] {0[0]} is incompatible with current client version.'.format(__application__)
		_globals_['appResultMessage'] = _config_['appFailedMessage']
	elif _config_['applicationEnabled']:
		print '[{0[1]}] {0[0]} successfully loaded.'.format(__application__)
		_globals_['appResultMessage'] = _config_['appLoadedMessage']
		_inject_chain_ += _inject_hooks_
	_inject_inits_()
	return

# *************************
# Application init
# *************************
initApplication()
