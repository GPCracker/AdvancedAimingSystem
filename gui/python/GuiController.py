# --------------------------- #
#    GuiController Classes    #
# --------------------------- #
class GuiController(object):
	__slots__ = ('__weakref__', '_updateInterval', '_updateCallbackLoop')

	avatarCtrlMode = AvatarInputHandler.aih_global_binding.bindRO(AvatarInputHandler.aih_global_binding.BINDING_ID.CTRL_MODE_NAME)

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

	def __init__(self, updateInterval=0.04):
		super(GuiController, self).__init__()
		self._updateInterval = updateInterval
		# Initialize internal components.
		self._initInternalComponents()
		return

	def _initInternalComponents(self):
		self._updateCallbackLoop = XModLib.CallbackUtils.CallbackLoop(
			self._updateInterval, XModLib.CallbackUtils.getMethodProxy(self._updateInfoPanels)
		)
		return

	def enable(self):
		aihGlobalBinding = AvatarInputHandler.aih_global_binding
		aihGlobalBinding.subscribe(aihGlobalBinding.BINDING_ID.CTRL_MODE_NAME, self.__onAvatarControlModeChanged)
		self.dispatchEvent(GuiEvent.AVATAR_CTRL_MODE, {'ctrlMode': self.avatarCtrlMode})
		return

	def disable(self):
		aihGlobalBinding = AvatarInputHandler.aih_global_binding
		aihGlobalBinding.unsubscribe(aihGlobalBinding.BINDING_ID.CTRL_MODE_NAME, self.__onAvatarControlModeChanged)
		return

	def __onAvatarControlModeChanged(self, ctrlMode):
		self.dispatchEvent(GuiEvent.AVATAR_CTRL_MODE, {'ctrlMode': ctrlMode})
		return

	def _getAimCorrectionMacroData(self):
		aimCorrection = getattr(BigWorld.player().inputHandler.ctrl, 'XAimCorrection', None)
		return aimCorrection.getMacroData() if aimCorrection is not None else None

	def _getTargetInfoMacroData(self):
		targetInfo = getattr(BigWorld.player().inputHandler, 'XTargetInfo', None)
		return targetInfo.getMacroData() if targetInfo is not None else None

	def _getAimingInfoMacroData(self):
		aimingInfo = getattr(BigWorld.player().inputHandler, 'XAimingInfo', None)
		return aimingInfo.getMacroData() if aimingInfo is not None else None

	def _updateInfoPanelMacroData(self, alias, macrodata):
		self.dispatchEvent(GuiEvent.INFO_PANEL_UPDATE, {'alias': alias, 'macrodata': macrodata})
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

	def __repr__(self):
		return '{!s}(updateInterval={!r})'.format(self.__class__.__name__, self._updateInterval)

	def __del__(self):
		self._updateCallbackLoop = None
		return
