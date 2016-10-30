# *************************
# GuiController Class
# *************************
class GuiController(object):
	@staticmethod
	def dispatchEvent(eventType, ctx=None, scope=gui.shared.EVENT_BUS_SCOPE.BATTLE):
		gui.shared.g_eventBus.handleEvent(GuiEvent(eventType, ctx), scope)
		return

	def __init__(self, formatter=None, updateInterval=0.04):
		self.formatter = formatter if formatter is not None else lambda string, *args, **kwargs: string
		self._updateCallbackLoop = XModLib.Callback.CallbackLoop(updateInterval, XModLib.Callback.Callback.getMethodProxy(self._update))
		return

	def getAimCorrectionMacroData(self):
		aimCorrection = getattr(BigWorld.player().inputHandler.ctrl, 'XAimCorrection', None)
		return aimCorrection.getMacroData() if aimCorrection is not None else None

	def getTargetInfoMacroData(self):
		targetInfo = getattr(BigWorld.player().inputHandler, 'XTargetInfo', None)
		return targetInfo.getMacroData() if targetInfo is not None else None

	def getPlayerAimingInfoMacroData(self):
		return AimingInfo.getMacroData()

	def _update(self):
		self.dispatchEvent(GuiEvent.CORRECTION_UPDATE, {'formatter': self.formatter, 'macrodata': self.getAimCorrectionMacroData()})
		self.dispatchEvent(GuiEvent.TARGET_UPDATE, {'formatter': self.formatter, 'macrodata': self.getTargetInfoMacroData()})
		self.dispatchEvent(GuiEvent.AIMING_UPDATE, {'formatter': self.formatter, 'macrodata': self.getPlayerAimingInfoMacroData()})
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
