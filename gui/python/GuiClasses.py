# *************************
# GuiClasses
# *************************
class GuiLoaderView(XModLib.pygui.battle.views.PanelsLoaderView.PanelsLoaderView):
	INFO_PANELS = (
		('AdvancedAimingSystemCorrectionPanel', 'TextPanel', 0),
		('AdvancedAimingSystemTargetPanel', 'TextPanel', 1),
		('AdvancedAimingSystemAimingPanel', 'TextPanel', 2)
	)

	def _populate(self):
		super(GuiLoaderView, self)._populate()
		for panelAlias, panelClass, panelIndex in self.INFO_PANELS:
			self.as_createBattlePagePanelS(panelAlias, panelClass, panelIndex)
		self.app.containerManager.onViewAddedToContainer += self.__onViewAddedToContainer
		return

	def __onViewAddedToContainer(self, container, view):
		if view.alias == self.alias:
			self.app.containerManager.onViewAddedToContainer -= self.__onViewAddedToContainer
			self.destroy()
		return

class GuiCorrectionPanel(XModLib.pygui.battle.views.components.panels.TextPanel.TextPanel):
	pass

class GuiTargetPanel(XModLib.pygui.battle.views.components.panels.TextPanel.TextPanel):
	pass

class GuiAimingPanel(XModLib.pygui.battle.views.components.panels.TextPanel.TextPanel):
	pass

class GuiSettings(object):
	CORRECTION_PANEL_ALIAS = 'AdvancedAimingSystemCorrectionPanel'
	TARGET_PANEL_ALIAS = 'AdvancedAimingSystemTargetPanel'
	AIMING_PANEL_ALIAS = 'AdvancedAimingSystemAimingPanel'
	LOADER_VIEW_ALIAS = 'AdvancedAimingSystemLoaderView'
	SWF_PATH = 'AdvancedAimingSystem.swf'

	@staticmethod
	def getViewSettings():
		return (
			GuiCorrectionPanel.getSettings(GuiSettings.CORRECTION_PANEL_ALIAS),
			GuiTargetPanel.getSettings(GuiSettings.TARGET_PANEL_ALIAS),
			GuiAimingPanel.getSettings(GuiSettings.AIMING_PANEL_ALIAS),
			GuiLoaderView.getSettings(GuiSettings.LOADER_VIEW_ALIAS, GuiSettings.SWF_PATH)
		)

class GuiEvent(gui.shared.events.GameEvent):
	CORRECTION_UPDATE = 'game/AdvancedAimingSystem/CorrectionPanelUpdate'
	TARGET_UPDATE = 'game/AdvancedAimingSystem/TargetPanelUpdate'
	AIMING_UPDATE = 'game/AdvancedAimingSystem/AimingPanelUpdate'
	CTRL_MODE_ENABLE = 'game/AdvancedAimingSystem/CtrlModeEnable'
	CTRL_MODE_DISABLE = 'game/AdvancedAimingSystem/CtrlModeDisable'

class GuiBaseBusinessHandler(gui.Scaleform.framework.package_layout.PackageBusinessHandler):
	def _getBattlePage(self):
		return self._app.containerManager.getContainer(gui.Scaleform.framework.ViewTypes.DEFAULT).getView()

	def _getBattlePageComponent(self, alias):
		battlePage = self._getBattlePage()
		return battlePage.components.get(alias, None) if battlePage is not None else None

	def _updatePanelText(self, alias, formatter, macrodata):
		panel = self._getBattlePageComponent(alias)
		if panel is not None:
			panel.updateText(formatter(panel.config['text'], **macrodata) if formatter and macrodata is not None else '')
		return

	def _setPanelConfig(self, alias, config):
		panel = self._getBattlePageComponent(alias)
		if panel is not None:
			panel.config = config
		return

class GuiBattleBusinessHandler(GuiBaseBusinessHandler):
	def __init__(self, panelConfigs):
		self._panelConfigs = panelConfigs
		super(GuiBattleBusinessHandler, self).__init__(
			(
				(GuiEvent.CORRECTION_UPDATE, self._handleCorrectionPanelUpdateEvent),
				(GuiEvent.TARGET_UPDATE, self._handleTargetPanelUpdateEvent),
				(GuiEvent.AIMING_UPDATE, self._handleAimingPanelUpdateEvent),
				(GuiEvent.CTRL_MODE_ENABLE, self._handleCtrlModeEnableEvent),
				(GuiEvent.CTRL_MODE_DISABLE, self._handleCtrlModeDisableEvent)
			),
			gui.app_loader.settings.APP_NAME_SPACE.SF_BATTLE,
			gui.shared.EVENT_BUS_SCOPE.BATTLE
		)
		return

	def _handleCorrectionPanelUpdateEvent(self, event):
		self._updatePanelText(GuiSettings.CORRECTION_PANEL_ALIAS, event.ctx.get('formatter', None), event.ctx.get('macrodata', None))
		return

	def _handleTargetPanelUpdateEvent(self, event):
		self._updatePanelText(GuiSettings.TARGET_PANEL_ALIAS, event.ctx.get('formatter', None), event.ctx.get('macrodata', None))
		return

	def _handleAimingPanelUpdateEvent(self, event):
		self._updatePanelText(GuiSettings.AIMING_PANEL_ALIAS, event.ctx.get('formatter', None), event.ctx.get('macrodata', None))
		return

	def _handleCtrlModeEnableEvent(self, event):
		ctrlModeName = event.ctx.get('ctrlModeName', None)
		if ctrlModeName is not None:
			for alias in (GuiSettings.CORRECTION_PANEL_ALIAS, GuiSettings.TARGET_PANEL_ALIAS, GuiSettings.AIMING_PANEL_ALIAS):
				self._setPanelConfig(alias, self._panelConfigs.get(alias, {}).get(ctrlModeName, {}))
		return

	def _handleCtrlModeDisableEvent(self, event):
		ctrlModeName = event.ctx.get('ctrlModeName', None)
		if ctrlModeName is not None:
			for alias in (GuiSettings.CORRECTION_PANEL_ALIAS, GuiSettings.TARGET_PANEL_ALIAS, GuiSettings.AIMING_PANEL_ALIAS):
				self._setPanelConfig(alias, {'visible': False})
		return

class GuiGlobalBusinessHandler(GuiBaseBusinessHandler):
	def __init__(self, panelConfigs):
		self._panelConfigs = panelConfigs
		super(GuiGlobalBusinessHandler, self).__init__(
			(
				(gui.shared.events.ComponentEvent.COMPONENT_REGISTERED, self._handleComponentRegistrationEvent),
			),
			gui.app_loader.settings.APP_NAME_SPACE.SF_BATTLE,
			gui.shared.EVENT_BUS_SCOPE.GLOBAL
		)
		return

	def _handleComponentRegistrationEvent(self, event):
		if event.alias in (GuiSettings.CORRECTION_PANEL_ALIAS, GuiSettings.TARGET_PANEL_ALIAS, GuiSettings.AIMING_PANEL_ALIAS):
			self._setPanelConfig(event.alias, self._panelConfigs.get(event.alias, {}).get('default', {}))
		return
