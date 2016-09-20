# *************************
# BattleShared Hooks
# *************************
@XModLib.HookUtils.HookFunction.staticMethodHookOnEvent(_inject_hooks_, gui.Scaleform.daapi.view.battle.shared, 'getViewSettings', calltype=XModLib.HookUtils.HookFunction.CALL_ORIGIN_INSIDE_HOOK)
def new_BattleShared_getViewSettings(old_BattleShared_getViewSettings, *args, **kwargs):
	result = old_BattleShared_getViewSettings(*args, **kwargs)
	if _config_['gui']['enabled']:
		result += AasGuiSettings.getViewSettings()
	return result

@XModLib.HookUtils.HookFunction.staticMethodHookOnEvent(_inject_hooks_, gui.Scaleform.daapi.view.battle.shared, 'getBusinessHandlers', calltype=XModLib.HookUtils.HookFunction.CALL_ORIGIN_INSIDE_HOOK)
def new_BattleShared_getBusinessHandlers(old_BattleShared_getBusinessHandlers, *args, **kwargs):
	result = old_BattleShared_getBusinessHandlers(*args, **kwargs)
	config = _config_['gui']
	if config['enabled']:
		result += (
			AasGuiBattleBusinessHandler(config['panels']),
			AasGuiGlobalBusinessHandler(config['panels'])
		)
	return result
