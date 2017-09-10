# *************************
# BattleShared Hooks
# *************************
@XModLib.HookUtils.staticMethodHookExt(_inject_hooks_, gui.Scaleform.daapi.view.battle.shared, 'getContextMenuHandlers', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_BattleShared_getContextMenuHandlers(old_BattleShared_getContextMenuHandlers, *args, **kwargs):
	result = old_BattleShared_getContextMenuHandlers(*args, **kwargs)
	if _config_['gui']['enabled']:
		result += GuiSettings.getContextMenuHandlers()
	return result

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
			GuiBattleBusinessHandler(config['panels']['static'], config['panels']['ingame']),
			GuiGlobalBusinessHandler(config['panels']['static'], config['panels']['ingame'])
		)
	return result

@XModLib.HookUtils.methodHookExt(_inject_hooks_, gui.Scaleform.daapi.view.battle.shared.SharedPage, '_populate', invoke=XModLib.HookUtils.HookInvoke.SECONDARY)
def new_SharedPage_populate(self, *args, **kwargs):
	if _config_['gui']['enabled']:
		self.app.loadView(gui.Scaleform.framework.managers.loaders.ViewLoadParams(GuiSettings.LOADER_VIEW_ALIAS))
	return
