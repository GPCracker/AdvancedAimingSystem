# *************************
# GuiClasses
# *************************
class AasGuiLoaderView(GuiLoaderView):
	INFO_PANELS = (
		('AdvancedAimingSystemCorrectionPanel', 'TextPanel', 0),
		('AdvancedAimingSystemTargetPanel', 'TextPanel', 1),
		('AdvancedAimingSystemAimingPanel', 'TextPanel', 2)
	)

	def _populate(self):
		super(AasGuiLoaderView, self)._populate()
		for panelAlias, panelClass, panelIndex in self.INFO_PANELS:
			self.as_createBattlePageComponentS(panelAlias, panelClass, panelIndex)
		return

class AasGuiCorrectionPanel(GuiTextPanel):
	pass

class AasGuiTargetPanel(GuiTextPanel):
	pass

class AasGuiAimingPanel(GuiTextPanel):
	pass

class AasGuiSettings(GuiSettings):
	CORRECTION_PANEL_ALIAS = 'AdvancedAimingSystemCorrectionPanel'
	TARGET_PANEL_ALIAS = 'AdvancedAimingSystemTargetPanel'
	AIMING_PANEL_ALIAS = 'AdvancedAimingSystemAimingPanel'
	LOADER_VIEW_ALIAS = 'AdvancedAimingSystemLoaderView'
	SWF_PATH = 'AdvancedAimingSystem.swf'

	@staticmethod
	def getViewSettings():
		return (
			GuiSettings.getComponentSettings(AasGuiSettings.CORRECTION_PANEL_ALIAS, AasGuiCorrectionPanel),
			GuiSettings.getComponentSettings(AasGuiSettings.TARGET_PANEL_ALIAS, AasGuiTargetPanel),
			GuiSettings.getComponentSettings(AasGuiSettings.AIMING_PANEL_ALIAS, AasGuiAimingPanel),
			GuiSettings.getViewSettings(AasGuiSettings.LOADER_VIEW_ALIAS, AasGuiLoaderView, AasGuiSettings.SWF_PATH)
		)

class AasGuiEvent(gui.shared.events.GameEvent):
	AAS_CORRECTION_UPDATE = 'game/AdvancedAimingSystem/CorrectionPanelUpdate'
	AAS_TARGET_UPDATE = 'game/AdvancedAimingSystem/TargetPanelUpdate'
	AAS_AIMING_UPDATE = 'game/AdvancedAimingSystem/AimingPanelUpdate'
	AAS_CTRL_MODE_ENABLE = 'game/AdvancedAimingSystem/CtrlModeEnable'
	AAS_CTRL_MODE_DISABLE = 'game/AdvancedAimingSystem/CtrlModeDisable'

class AasGuiBaseBusinessHandler(gui.Scaleform.framework.package_layout.PackageBusinessHandler):
	def _getBattlePage(self):
		arenaGuiTypeVisitor = gui.battle_control.g_sessionProvider.arenaVisitor.gui
		if arenaGuiTypeVisitor.isTutorialBattle():
			battlePageAlias = gui.Scaleform.daapi.settings.views.VIEW_ALIAS.TUTORIAL_BATTLE_PAGE
		elif arenaGuiTypeVisitor.isFalloutClassic():
			battlePageAlias = gui.Scaleform.daapi.settings.views.VIEW_ALIAS.FALLOUT_CLASSIC_PAGE
		elif arenaGuiTypeVisitor.isFalloutMultiTeam():
			battlePageAlias = gui.Scaleform.daapi.settings.views.VIEW_ALIAS.FALLOUT_MULTITEAM_PAGE
		else:
			battlePageAlias = gui.Scaleform.daapi.settings.views.VIEW_ALIAS.CLASSIC_BATTLE_PAGE
		return self.findViewByAlias(gui.Scaleform.framework.ViewTypes.VIEW, battlePageAlias)

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

class AasGuiBattleBusinessHandler(AasGuiBaseBusinessHandler):
	def __init__(self, panelConfigs):
		self._panelConfigs = panelConfigs
		listeners = (
			(AasGuiEvent.AAS_CORRECTION_UPDATE, self._handleCorrectionPanelUpdateEvent),
			(AasGuiEvent.AAS_TARGET_UPDATE, self._handleTargetPanelUpdateEvent),
			(AasGuiEvent.AAS_AIMING_UPDATE, self._handleAimingPanelUpdateEvent),
			(AasGuiEvent.AAS_CTRL_MODE_ENABLE, self._handleCtrlModeEnableEvent),
			(AasGuiEvent.AAS_CTRL_MODE_DISABLE, self._handleCtrlModeDisableEvent)
		)
		super(AasGuiBattleBusinessHandler, self).__init__(
			listeners,
			gui.app_loader.settings.APP_NAME_SPACE.SF_BATTLE,
			gui.shared.EVENT_BUS_SCOPE.BATTLE
		)
		return

	def _handleCorrectionPanelUpdateEvent(self, event):
		self._updatePanelText(AasGuiSettings.CORRECTION_PANEL_ALIAS, event.ctx.get('formatter', None), event.ctx.get('macrodata', None))
		return

	def _handleTargetPanelUpdateEvent(self, event):
		self._updatePanelText(AasGuiSettings.TARGET_PANEL_ALIAS, event.ctx.get('formatter', None), event.ctx.get('macrodata', None))
		return

	def _handleAimingPanelUpdateEvent(self, event):
		self._updatePanelText(AasGuiSettings.AIMING_PANEL_ALIAS, event.ctx.get('formatter', None), event.ctx.get('macrodata', None))
		return

	def _handleCtrlModeEnableEvent(self, event):
		ctrlModeName = event.ctx.get('ctrlModeName', None)
		if ctrlModeName is not None:
			for alias in (AasGuiSettings.CORRECTION_PANEL_ALIAS, AasGuiSettings.TARGET_PANEL_ALIAS, AasGuiSettings.AIMING_PANEL_ALIAS):
				self._setPanelConfig(alias, self._panelConfigs.get(alias, {}).get(ctrlModeName, {}))
		return

	def _handleCtrlModeDisableEvent(self, event):
		ctrlModeName = event.ctx.get('ctrlModeName', None)
		if ctrlModeName is not None:
			for alias in (AasGuiSettings.CORRECTION_PANEL_ALIAS, AasGuiSettings.TARGET_PANEL_ALIAS, AasGuiSettings.AIMING_PANEL_ALIAS):
				self._setPanelConfig(alias, {'visible': False})
		return

class AasGuiGlobalBusinessHandler(AasGuiBaseBusinessHandler):
	def __init__(self, panelConfigs):
		self._panelConfigs = panelConfigs
		listeners = (
			(gui.shared.events.ComponentEvent.COMPONENT_REGISTERED, self._handleComponentRegistrationEvent),
		)
		super(AasGuiGlobalBusinessHandler, self).__init__(
			listeners,
			gui.app_loader.settings.APP_NAME_SPACE.SF_BATTLE,
			gui.shared.EVENT_BUS_SCOPE.GLOBAL
		)
		return

	def _handleComponentRegistrationEvent(self, event):
		if event.alias in (AasGuiSettings.CORRECTION_PANEL_ALIAS, AasGuiSettings.TARGET_PANEL_ALIAS, AasGuiSettings.AIMING_PANEL_ALIAS):
			self._setPanelConfig(event.alias, self._panelConfigs.get(event.alias, {}).get('default', {}))
		elif event.alias == gui.Scaleform.genConsts.BATTLE_VIEW_ALIASES.BATTLE_VIEW_ALIASES.CONSUMABLES_PANEL:
			self._app.containerManager.onViewAddedToContainer += self._onViewAddedToContainer
			self.loadViewWithDefName(AasGuiSettings.LOADER_VIEW_ALIAS)
		return

	def _onViewAddedToContainer(self, container, view):
		if view.alias == AasGuiSettings.LOADER_VIEW_ALIAS:
			self._app.containerManager.onViewAddedToContainer -= self._onViewAddedToContainer
			view.destroy()
		return
