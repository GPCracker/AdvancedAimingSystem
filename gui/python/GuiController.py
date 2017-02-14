# *************************
# GuiController Class
# *************************
class GuiController(object):
	__slots__ = ('__weakref__', 'formatter', '_updateCallbackLoop')

	@staticmethod
	def dispatchEvent(eventType, ctx=None, scope=gui.shared.EVENT_BUS_SCOPE.BATTLE):
		gui.shared.g_eventBus.handleEvent(GuiEvent(eventType, ctx), scope)
		return

	def __init__(self, formatter=None, updateInterval=0.04):
		super(GuiController, self).__init__()
		self.formatter = formatter if callable(formatter) else lambda string, *args, **kwargs: string
		self._updateCallbackLoop = XModLib.CallbackUtils.CallbackLoop(updateInterval, XModLib.CallbackUtils.getMethodProxy(self._update))
		return

	def getAimCorrectionMacroData(self):
		aimCorrection = getattr(BigWorld.player().inputHandler.ctrl, 'XAimCorrection', None)
		return aimCorrection.getMacroData() if aimCorrection is not None else None

	def getTargetInfoMacroData(self):
		targetInfo = getattr(BigWorld.player().inputHandler, 'XTargetInfo', None)
		return targetInfo.getMacroData() if targetInfo is not None else None

	def getPlayerAimingInfoMacroData(self):
		return AimingInfo.getMacroData()

	def _updateInfoPanelMacroData(self, alias, macrodata):
		self.dispatchEvent(GuiEvent.INFO_PANEL_UPDATE, {'alias': alias, 'formatter': self.formatter, 'macrodata': macrodata})
		return

	def _update(self):
		self._updateInfoPanelMacroData(GuiSettings.CORRECTION_PANEL_ALIAS, self.getAimCorrectionMacroData())
		self._updateInfoPanelMacroData(GuiSettings.TARGET_PANEL_ALIAS, self.getTargetInfoMacroData())
		self._updateInfoPanelMacroData(GuiSettings.AIMING_PANEL_ALIAS, self.getPlayerAimingInfoMacroData())
		return

	@property
	def isUpdateActive(self):
		return self._updateCallbackLoop.isActive

	def start(self, delay=None):
		self._updateCallbackLoop.start(delay)
		return

	def stop(self):
		self._updateCallbackLoop.stop()
		return

	def handleControlModeEnable(self, ctrlModeName):
		self.dispatchEvent(GuiEvent.CTRL_MODE_ENABLE, {'ctrlModeName': ctrlModeName})
		return

	def handleControlModeDisable(self, ctrlModeName):
		self.dispatchEvent(GuiEvent.CTRL_MODE_DISABLE, {'ctrlModeName': ctrlModeName})
		return

	def __del__(self):
		self._updateCallbackLoop = None
		self.formatter = None
		return
