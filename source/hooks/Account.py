# ------------------- #
#    Account Hooks    #
# ------------------- #
@XModLib.HookUtils.methodHookExt(g_inject_basis, Account.Account, 'onBecomePlayer')
def new_Account_onBecomePlayer(self, *args, **kwargs):
	if g_globals['appLoadingMessage']:
		XModLib.ClientMessages.SystemMessageFormatter().install(__application__[1])
		def handler(model, entityID, action):
			if action == '{0[1]}.official_topic'.format(__application__):
				BigWorld.wg_openWebBrowser(__official_topic__)
			return
		XModLib.ClientMessages.SystemMessageActionHandler(handler).install()
		XModLib.ClientMessages.pushSystemMessage(
			{
				'message': g_globals['appLoadingMessage'],
				'timestamp': time.time(),
				'icon': 'img://gui/maps/icons/library/InformationIcon-1.png',
			},
			__application__[1],
			auxData=['Information']
		)
		g_globals['appLoadingMessage'] = None
	return
