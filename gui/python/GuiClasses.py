# ----------------- #
#    Gui Classes    #
# ----------------- #
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

class GuiInfoPanelContextMenuHandler(XModLib.pygui.battle.views.handlers.ContextMenuHandler.ContextMenuHandler):
	OPTIONS = (
		('hideInfoPanel', '_hideInfoPanel', _config_['gui']['panels']['context']['hideInfoPanel'], '', True, None),
		('resetInfoPanel', '_resetInfoPanel', _config_['gui']['panels']['context']['resetInfoPanel'], '', True, None)
	)

	@classmethod
	def _getOptionsHandlers(cls):
		def _getOptionsHandlersGenerator(options):
			for idx, handler, label, icon, enabled, submenu in options:
				if submenu is not None:
					for entry in _getOptionsHandlersGenerator(submenu):
						yield entry
				else:
					yield idx, handler
			return
		return dict(_getOptionsHandlersGenerator(cls.OPTIONS))

	@classmethod
	def _getOptionsItems(cls):
		def _makeOptionsItems(options):
			return [cls._makeItem(idx, label, optInitData={'enabled': enabled, 'iconType': icon}, optSubMenu=_makeOptionsItems(submenu) if submenu is not None else submenu) for idx, handler, label, icon, enabled, submenu in options]
		return _makeOptionsItems(cls.OPTIONS)

	def __init__(self, cmProxy, ctx=None):
		super(GuiInfoPanelContextMenuHandler, self).__init__(cmProxy, ctx=ctx, handlers=self._getOptionsHandlers())
		return

	def fini(self):
		super(GuiInfoPanelContextMenuHandler, self).fini()
		return

	def _initFlashValues(self, ctx):
		super(GuiInfoPanelContextMenuHandler, self)._initFlashValues(ctx)
		self._alias = ctx.alias
		return

	def _clearFlashValues(self):
		super(GuiInfoPanelContextMenuHandler, self)._clearFlashValues()
		self._alias = None
		return

	def _hideInfoPanel(self):
		gui.shared.g_eventBus.handleEvent(GuiEvent(GuiEvent.INFO_PANEL_INGAME_CONFIG, {'alias': self._alias, 'config': {'visible': False}}), gui.shared.EVENT_BUS_SCOPE.BATTLE)
		return

	def _resetInfoPanel(self):
		gui.shared.g_eventBus.handleEvent(GuiEvent(GuiEvent.INFO_PANEL_INGAME_RESET, {'alias': self._alias}), gui.shared.EVENT_BUS_SCOPE.BATTLE)
		return

	def _generateOptions(self, ctx=None):
		return self._getOptionsItems()

class GuiCorrectionPanelContextMenuHandler(GuiInfoPanelContextMenuHandler):
	pass

class GuiTargetPanelContextMenuHandler(GuiInfoPanelContextMenuHandler):
	pass

class GuiAimingPanelContextMenuHandler(GuiInfoPanelContextMenuHandler):
	pass

class GuiInfoPanel(XModLib.pygui.battle.views.components.panels.TextPanel.TextPanel):
	def __init__(self, *args, **kwargs):
		super(GuiInfoPanel, self).__init__(*args, **kwargs)
		self.__alias = None
		self.__config = {
			'template': ''
		}
		return

	def py_onPanelDrag(self, x, y):
		super(GuiInfoPanel, self).py_onPanelDrag(x, y)
		self.fireEvent(GuiEvent(GuiEvent.INFO_PANEL_DRAG, {'alias': self.__alias, 'position': (x, y)}), gui.shared.EVENT_BUS_SCOPE.BATTLE)
		return

	def py_onPanelDrop(self, x, y):
		super(GuiInfoPanel, self).py_onPanelDrop(x, y)
		self.fireEvent(GuiEvent(GuiEvent.INFO_PANEL_DROP, {'alias': self.__alias, 'position': (x, y)}), gui.shared.EVENT_BUS_SCOPE.BATTLE)
		return

	def _populate(self):
		super(GuiInfoPanel, self)._populate()
		self.__alias = self.flashObject.name if self._isDAAPIInited() else None
		self.addListener(GuiEvent.INFO_PANEL_CONFIG, self._handlePanelConfigEvent, gui.shared.EVENT_BUS_SCOPE.BATTLE)
		self.addListener(GuiEvent.INFO_PANEL_UPDATE, self._handlePanelUpdateEvent, gui.shared.EVENT_BUS_SCOPE.BATTLE)
		return

	def _dispose(self):
		self.removeListener(GuiEvent.INFO_PANEL_CONFIG, self._handlePanelConfigEvent, gui.shared.EVENT_BUS_SCOPE.BATTLE)
		self.removeListener(GuiEvent.INFO_PANEL_UPDATE, self._handlePanelUpdateEvent, gui.shared.EVENT_BUS_SCOPE.BATTLE)
		super(GuiInfoPanel, self)._dispose()
		return

	def _handlePanelConfigEvent(self, event):
		if event.ctx['alias'] == self.__alias:
			self.updateConfig(event.ctx['config'])
		return

	def _handlePanelUpdateEvent(self, event):
		if event.ctx['alias'] == self.__alias:
			self.updateMacroData(event.ctx['macrodata'])
		return

	def getConfig(self):
		config = super(GuiInfoPanel, self).getConfig()
		config.update(self.__config)
		return config

	def updateConfig(self, config):
		super(GuiInfoPanel, self).updateConfig(config)
		self.__config.update(self._computeConfigPatch(config, self.__config))
		return

	def updateMacroData(self, macrodata):
		self.updateText(self.__config['template'](**macrodata) if macrodata is not None else '')
		return

class GuiCorrectionPanel(GuiInfoPanel):
	pass

class GuiTargetPanel(GuiInfoPanel):
	pass

class GuiAimingPanel(GuiInfoPanel):
	pass

class GuiSettings(object):
	CORRECTION_PANEL_ALIAS = 'AdvancedAimingSystemCorrectionPanel'
	TARGET_PANEL_ALIAS = 'AdvancedAimingSystemTargetPanel'
	AIMING_PANEL_ALIAS = 'AdvancedAimingSystemAimingPanel'
	LOADER_VIEW_ALIAS = 'AdvancedAimingSystemLoaderView'
	SWF_PATH = 'AdvancedAimingSystem.swf'

	@staticmethod
	def getContextMenuHandlers():
		return (
			GuiCorrectionPanelContextMenuHandler.getHandler(GuiSettings.CORRECTION_PANEL_ALIAS),
			GuiTargetPanelContextMenuHandler.getHandler(GuiSettings.TARGET_PANEL_ALIAS),
			GuiAimingPanelContextMenuHandler.getHandler(GuiSettings.AIMING_PANEL_ALIAS)
		)

	@staticmethod
	def getViewSettings():
		return (
			GuiCorrectionPanel.getSettings(GuiSettings.CORRECTION_PANEL_ALIAS),
			GuiTargetPanel.getSettings(GuiSettings.TARGET_PANEL_ALIAS),
			GuiAimingPanel.getSettings(GuiSettings.AIMING_PANEL_ALIAS),
			GuiLoaderView.getSettings(GuiSettings.LOADER_VIEW_ALIAS, GuiSettings.SWF_PATH)
		)

class GuiEvent(gui.shared.events.GameEvent):
	INFO_PANEL_INGAME_CONFIG = 'game/AdvancedAimingSystem/InfoPanelIngameConfig'
	INFO_PANEL_INGAME_RESET = 'game/AdvancedAimingSystem/InfoPanelIngameReset'
	INFO_PANEL_CONFIG = 'game/AdvancedAimingSystem/InfoPanelConfig'
	INFO_PANEL_UPDATE = 'game/AdvancedAimingSystem/InfoPanelUpdate'
	INFO_PANEL_DRAG = 'game/AdvancedAimingSystem/InfoPanelDrag'
	INFO_PANEL_DROP = 'game/AdvancedAimingSystem/InfoPanelDrop'
	AVATAR_CTRL_MODE = 'game/AdvancedAimingSystem/AvatarCtrlMode'

class GuiBaseBusinessHandler(gui.Scaleform.framework.package_layout.PackageBusinessHandler):
	@staticmethod
	def _updatePanelConfig(alias, config):
		gui.shared.g_eventBus.handleEvent(GuiEvent(GuiEvent.INFO_PANEL_CONFIG, {'alias': alias, 'config': config}), gui.shared.EVENT_BUS_SCOPE.BATTLE)
		return

class GuiBattleBusinessHandler(GuiBaseBusinessHandler):
	def __init__(self, staticConfigs, ingameConfigs):
		self._ctrlModeName = 'default'
		self._staticConfigs = staticConfigs
		self._ingameConfigs = ingameConfigs
		super(GuiBattleBusinessHandler, self).__init__(
			(
				(GuiEvent.INFO_PANEL_INGAME_CONFIG, self._handleInfoPanelIngameConfigEvent),
				(GuiEvent.INFO_PANEL_INGAME_RESET, self._handleInfoPanelIngameResetEvent),
				(GuiEvent.INFO_PANEL_DRAG, self._handleInfoPanelDragEvent),
				(GuiEvent.INFO_PANEL_DROP, self._handleInfoPanelDropEvent),
				(GuiEvent.AVATAR_CTRL_MODE, self._handleAvatarCtrlModeEvent)
			),
			gui.app_loader.settings.APP_NAME_SPACE.SF_BATTLE,
			gui.shared.EVENT_BUS_SCOPE.BATTLE
		)
		return

	def _reconfigureInfoPanel(self, alias):
		config = self._staticConfigs.get(alias, {}).get('default', {}).copy()
		config.update(self._ingameConfigs.get(alias, {}).get('default', {}))
		if self._ctrlModeName != 'default':
			config.update(self._staticConfigs.get(alias, {}).get(self._ctrlModeName, {}))
			config.update(self._ingameConfigs.get(alias, {}).get(self._ctrlModeName, {}))
		self._updatePanelConfig(alias, config)
		return

	def _handleInfoPanelIngameConfigEvent(self, event):
		if self._ctrlModeName != 'default':
			self._ingameConfigs.setdefault(event.ctx['alias'], {}).setdefault(self._ctrlModeName, {}).update(event.ctx['config'])
			self._reconfigureInfoPanel(event.ctx['alias'])
			self._ingameConfigs.save()
		return

	def _handleInfoPanelIngameResetEvent(self, event):
		if self._ctrlModeName != 'default':
			self._ingameConfigs.setdefault(event.ctx['alias'], {}).setdefault(self._ctrlModeName, {}).clear()
			self._reconfigureInfoPanel(event.ctx['alias'])
			self._ingameConfigs.save()
		return

	def _handleInfoPanelDragEvent(self, event):
		if self._ctrlModeName != 'default':
			self._ingameConfigs.setdefault(event.ctx['alias'], {}).setdefault(self._ctrlModeName, {})['position'] = event.ctx['position']
			self._ingameConfigs.save()
		return

	def _handleInfoPanelDropEvent(self, event):
		if self._ctrlModeName != 'default':
			self._ingameConfigs.setdefault(event.ctx['alias'], {}).setdefault(self._ctrlModeName, {})['position'] = event.ctx['position']
			self._ingameConfigs.save()
		return

	def _handleAvatarCtrlModeEvent(self, event):
		ctrlMode = event.ctx['ctrlMode']
		if ctrlMode == AvatarInputHandler.aih_constants.CTRL_MODE_NAME.ARCADE:
			ctrlModeName = 'arcade'
		elif ctrlMode == AvatarInputHandler.aih_constants.CTRL_MODE_NAME.SNIPER:
			ctrlModeName = 'sniper'
		elif ctrlMode == AvatarInputHandler.aih_constants.CTRL_MODE_NAME.STRATEGIC:
			ctrlModeName = 'strategic'
		elif ctrlMode == AvatarInputHandler.aih_constants.CTRL_MODE_NAME.ARTY:
			ctrlModeName = 'arty'
		else:
			ctrlModeName = 'default'
		self._ctrlModeName = ctrlModeName
		for alias in (GuiSettings.CORRECTION_PANEL_ALIAS, GuiSettings.TARGET_PANEL_ALIAS, GuiSettings.AIMING_PANEL_ALIAS):
			config = self._staticConfigs.get(alias, {}).get(ctrlModeName, {}).copy()
			config.update(self._ingameConfigs.get(alias, {}).get(ctrlModeName, {}))
			self._updatePanelConfig(alias, config)
		return

class GuiGlobalBusinessHandler(GuiBaseBusinessHandler):
	def __init__(self, staticConfigs, ingameConfigs):
		self._staticConfigs = staticConfigs
		self._ingameConfigs = ingameConfigs
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
			config = self._staticConfigs.get(event.alias, {}).get('default', {}).copy()
			config.update(self._ingameConfigs.get(event.alias, {}).get('default', {}))
			self._updatePanelConfig(event.alias, config)
		return
