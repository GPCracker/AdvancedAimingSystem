# *************************
# BattleShared Hooks
# *************************
@XModLib.HookUtils.staticMethodHookExt(_inject_hooks_, gui.Scaleform.daapi.view.battle.shared, 'getViewSettings', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_BattleShared_getViewSettings(old_BattleShared_getViewSettings, *args, **kwargs):
	result = old_BattleShared_getViewSettings(*args, **kwargs)
	if _config_['gui']['enabled']:
		result += GuiSettings.getViewSettings()
	return result

@XModLib.HookUtils.staticMethodHookExt(_inject_hooks_, gui.Scaleform.daapi.view.battle.shared, 'getBusinessHandlers', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_BattleShared_getBusinessHandlers(old_BattleShared_getBusinessHandlers, *args, **kwargs):
	result = old_BattleShared_getBusinessHandlers(*args, **kwargs)
	config = _config_['gui']
	if config['enabled']:
		result += (
			GuiBattleBusinessHandler(config['panels']),
			GuiGlobalBusinessHandler(config['panels'])
		)
	return result
