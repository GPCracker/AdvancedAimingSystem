# *************************
# ArtyControlMode Hooks
# *************************
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.ArtyControlMode, '__init__', invoke=XModLib.HookUtils.HookInvoke.SECONDARY)
def new_ArtyControlMode_init(self, *args, **kwargs):
	config = _config_['artyAS']['aimCorrection']
	self.XAimCorrection = ArtyAimCorrection(
		self,
		config['manualMode']['enabled'],
		config['targetMode']['enabled'] and config['targetMode']['activated']
	)
	return

@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.ArtyControlMode, 'enable', invoke=XModLib.HookUtils.HookInvoke.SECONDARY)
def new_ArtyControlMode_enable(self, *args, **kwargs):
	if self is self._aih.ctrls[AvatarInputHandler.aih_constants.CTRL_MODE_NAME.ARTY]:
		self.XAimCorrection.handleControlModeEnable()
		targetScanner = getattr(self._aih, 'XTargetScanner', None)
		if targetScanner is not None and not targetScanner.isUpdateActive:
			targetScanner.start()
		guiController = getattr(self._aih, 'XGuiController', None)
		if guiController is not None and not guiController.isUpdateActive:
			guiController.handleControlModeEnable(AvatarInputHandler.aih_constants.CTRL_MODE_NAME.ARTY)
			guiController.start()
	return

@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.ArtyControlMode, 'disable', invoke=XModLib.HookUtils.HookInvoke.PRIMARY)
def new_ArtyControlMode_disable(self, *args, **kwargs):
	if self is self._aih.ctrls[AvatarInputHandler.aih_constants.CTRL_MODE_NAME.ARTY]:
		self.XAimCorrection.handleControlModeDisable()
		targetScanner = getattr(self._aih, 'XTargetScanner', None)
		if targetScanner is not None and targetScanner.isUpdateActive:
			targetScanner.stop()
		guiController = getattr(self._aih, 'XGuiController', None)
		if guiController is not None and guiController.isUpdateActive:
			guiController.handleControlModeDisable(AvatarInputHandler.aih_constants.CTRL_MODE_NAME.ARTY)
			guiController.stop()
	return

@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.ArtyControlMode, 'getDesiredShotPoint', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_ArtyControlMode_getDesiredShotPoint(old_ArtyControlMode_getDesiredShotPoint, self, *args, **kwargs):
	shotPoint = old_ArtyControlMode_getDesiredShotPoint(self, *args, **kwargs)
	if self is self._aih.ctrls[AvatarInputHandler.aih_constants.CTRL_MODE_NAME.ARTY]:
		return self.XAimCorrection.getDesiredShotPoint(shotPoint)
	return shotPoint
