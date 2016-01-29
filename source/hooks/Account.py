# *************************
# Account Hooks
# *************************
@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_loads_, Account.Account, 'onBecomePlayer')
def new_Account_onBecomePlayer(self, *args, **kwargs):
	if _globals_['appResultMessageFlag'] or not _globals_['appResultMessage']:
		return
	XModLib.Messages.LobbyMessenger.appendFormatter(
		__application__[1],
		XModLib.Messages.SystemMessageFormatter(
			XModLib.Messages.LobbyMessenger.getGuiSettings(True, auxData=['Information'])
		)
	)
	def handler(model, entityID, action):
		if action == '{}.official_topic'.format(__application__[1]):
			XModLib.Messages.Messenger.externalBrowserOpenURL(__official_topic__)
		return
	XModLib.Messages.SystemMessageActionHandler.factory('ActionHandler', handler).install()
	XModLib.Messages.LobbyMessenger.pushClientMessage(
		XModLib.Messages.SystemMessage({
			'message': HTMLParser.HTMLParser().unescape(_globals_['appResultMessage']),
			'timestamp': time.time(),
			'icon': 'img://gui/maps/icons/library/InformationIcon-1.png',
		}),
		__application__[1]
	)
	_globals_['appResultMessageFlag'] = True
	return
