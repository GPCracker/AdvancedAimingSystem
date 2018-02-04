# ------------------------ #
#    BattleShared Hooks    #
# ------------------------ #
@XModLib.HookUtils.staticMethodHookExt(g_inject_hooks, gui.Scaleform.daapi.view.battle.shared, 'getContextMenuHandlers', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_BattleShared_getContextMenuHandlers(old_BattleShared_getContextMenuHandlers, *args, **kwargs):
	result = old_BattleShared_getContextMenuHandlers(*args, **kwargs)
	if g_config['gui']['enabled']:
		result += GuiSettings.getContextMenuHandlers()
	return result

@XModLib.HookUtils.staticMethodHookExt(g_inject_hooks, gui.Scaleform.daapi.view.battle.shared, 'getViewSettings', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_BattleShared_getViewSettings(old_BattleShared_getViewSettings, *args, **kwargs):
	result = old_BattleShared_getViewSettings(*args, **kwargs)
	if g_config['gui']['enabled']:
		result += GuiSettings.getViewSettings()
	return result

@XModLib.HookUtils.staticMethodHookExt(g_inject_hooks, gui.Scaleform.daapi.view.battle.shared, 'getBusinessHandlers', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_BattleShared_getBusinessHandlers(old_BattleShared_getBusinessHandlers, *args, **kwargs):
	result = old_BattleShared_getBusinessHandlers(*args, **kwargs)
	config = g_config['gui']
	if config['enabled']:
		result += (
			GuiBattleBusinessHandler(config['panels']['static'], config['panels']['ingame']),
			GuiGlobalBusinessHandler(config['panels']['static'], config['panels']['ingame'])
		)
	return result

# ---------------------- #
#    SharedPage Hooks    #
# ---------------------- #
@XModLib.HookUtils.methodHookExt(g_inject_hooks, gui.Scaleform.daapi.view.battle.shared.SharedPage, '_populate', invoke=XModLib.HookUtils.HookInvoke.SECONDARY)
def new_SharedPage_populate(self, *args, **kwargs):
	if g_config['gui']['enabled']:
		self.as_createBattlePagePanelS(GuiSettings.CORRECTION_PANEL_ALIAS, 'TextPanel', 0)
		self.as_createBattlePagePanelS(GuiSettings.TARGET_PANEL_ALIAS, 'TextPanel', 1)
		self.as_createBattlePagePanelS(GuiSettings.AIMING_PANEL_ALIAS, 'TextPanel', 2)
	return
