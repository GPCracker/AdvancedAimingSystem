# *************************
# GuiController Class
# *************************
class GuiController(object):
	__slots__ = ('__weakref__', 'formatter', '_updateInterval', '_updateCallbackLoop')

	@staticmethod
	def dispatchEvent(eventType, ctx=None, scope=gui.shared.EVENT_BUS_SCOPE.BATTLE):
		gui.shared.g_eventBus.handleEvent(GuiEvent(eventType, ctx), scope)
		return

	@property
	def updateInterval(self):
		return self._updateInterval

	@updateInterval.setter
	def updateInterval(self, value):
		if self.isUpdateActive:
			raise RuntimeError('update interval could not be changed while controller is running')
		self._updateInterval = value
		# Recreate internal components.
		self._initInternalComponents()
		return

	def __init__(self, formatter=None, updateInterval=0.04):
		super(GuiController, self).__init__()
		self.formatter = formatter if callable(formatter) else lambda string, *args, **kwargs: string
		self._updateInterval = updateInterval
		# Initialize internal components.
		self._initInternalComponents()
		return

	def _initInternalComponents(self):
		self._updateCallbackLoop = XModLib.CallbackUtils.CallbackLoop(
			self._updateInterval, XModLib.CallbackUtils.getMethodProxy(self._updateInfoPanels)
		)
		return

	def _getAimCorrectionMacroData(self):
		aimCorrection = getattr(BigWorld.player().inputHandler.ctrl, 'XAimCorrection', None)
		return aimCorrection.getMacroData() if aimCorrection is not None else None

	def _getTargetInfoMacroData(self):
		targetInfo = getattr(BigWorld.player().inputHandler, 'XTargetInfo', None)
		return targetInfo.getMacroData() if targetInfo is not None else None

	def _getAimingInfoMacroData(self):
		return AimingInfo.getMacroData()

	def _updateInfoPanelMacroData(self, alias, macrodata):
		self.dispatchEvent(GuiEvent.INFO_PANEL_UPDATE, {'alias': alias, 'formatter': self.formatter, 'macrodata': macrodata})
		return

	def _updateInfoPanels(self):
		self._updateInfoPanelMacroData(GuiSettings.CORRECTION_PANEL_ALIAS, self._getAimCorrectionMacroData())
		self._updateInfoPanelMacroData(GuiSettings.TARGET_PANEL_ALIAS, self._getTargetInfoMacroData())
		self._updateInfoPanelMacroData(GuiSettings.AIMING_PANEL_ALIAS, self._getAimingInfoMacroData())
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

	def __repr__(self):
		return '{!s}(formatter={!r}, updateInterval={!r})'.format(self.__class__.__name__, self.formatter, self._updateInterval)

	def __del__(self):
		self._updateCallbackLoop = None
		self.formatter = None
		return
