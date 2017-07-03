# *************************
# ArcadeControlMode Hooks
# *************************
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.ArcadeControlMode, '__init__', invoke=XModLib.HookUtils.HookInvoke.SECONDARY)
def new_ArcadeControlMode_init(self, *args, **kwargs):
	config = _config_['arcadeAS']['aimCorrection']
	self.XAimCorrection = ArcadeAimCorrection(
		self,
		config['manualMode']['enabled'],
		config['targetMode']['enabled'] and config['targetMode']['activated'],
		config['targetMode']['distance'][0],
		config['targetMode']['distance'][1]
	)
	return

@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.ArcadeControlMode, 'enable', invoke=XModLib.HookUtils.HookInvoke.SECONDARY)
def new_ArcadeControlMode_enable(self, *args, **kwargs):
	if self is self._aih.ctrls[AvatarInputHandler.aih_constants.CTRL_MODE_NAME.ARCADE]:
		self.XAimCorrection.handleControlModeEnable()
		targetScanner = getattr(self._aih, 'XTargetScanner', None)
		if targetScanner is not None and not targetScanner.isUpdateActive:
			targetScanner.start()
		guiController = getattr(self._aih, 'XGuiController', None)
		if guiController is not None and not guiController.isUpdateActive:
			guiController.handleControlModeEnable(AvatarInputHandler.aih_constants.CTRL_MODE_NAME.ARCADE)
			guiController.start()
	return

@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.ArcadeControlMode, 'disable', invoke=XModLib.HookUtils.HookInvoke.PRIMARY)
def new_ArcadeControlMode_disable(self, *args, **kwargs):
	if self is self._aih.ctrls[AvatarInputHandler.aih_constants.CTRL_MODE_NAME.ARCADE]:
		self.XAimCorrection.handleControlModeDisable()
		targetScanner = getattr(self._aih, 'XTargetScanner', None)
		if targetScanner is not None and targetScanner.isUpdateActive:
			targetScanner.stop()
		guiController = getattr(self._aih, 'XGuiController', None)
		if guiController is not None and guiController.isUpdateActive:
			guiController.handleControlModeDisable(AvatarInputHandler.aih_constants.CTRL_MODE_NAME.ARCADE)
			guiController.stop()
	return

@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.ArcadeControlMode, 'getDesiredShotPoint', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_ArcadeControlMode_getDesiredShotPoint(old_ArcadeControlMode_getDesiredShotPoint, self, *args, **kwargs):
	shotPoint = old_ArcadeControlMode_getDesiredShotPoint(self, *args, **kwargs)
	if self is self._aih.ctrls[AvatarInputHandler.aih_constants.CTRL_MODE_NAME.ARCADE]:
		return self.XAimCorrection.getDesiredShotPoint(shotPoint)
	return shotPoint
