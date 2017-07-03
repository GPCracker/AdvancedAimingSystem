# *************************
# StrategicControlMode Hooks
# *************************
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.StrategicControlMode, '__init__', invoke=XModLib.HookUtils.HookInvoke.SECONDARY)
def new_StrategicControlMode_init(self, *args, **kwargs):
	config = _config_['strategicAS']['aimCorrection']
	self.XAimCorrection = StrategicAimCorrection(
		self,
		config['manualMode']['enabled'],
		config['targetMode']['enabled'] and config['targetMode']['activated'],
		config['ignoreVehicles'],
		config['targetMode']['heightMultiplier']
	)
	return

@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.StrategicControlMode, 'enable', invoke=XModLib.HookUtils.HookInvoke.SECONDARY)
def new_StrategicControlMode_enable(self, *args, **kwargs):
	if self is self._aih.ctrls[AvatarInputHandler.aih_constants.CTRL_MODE_NAME.STRATEGIC]:
		self.XAimCorrection.handleControlModeEnable()
		targetScanner = getattr(self._aih, 'XTargetScanner', None)
		if targetScanner is not None and not targetScanner.isUpdateActive:
			targetScanner.start()
		guiController = getattr(self._aih, 'XGuiController', None)
		if guiController is not None and not guiController.isUpdateActive:
			guiController.handleControlModeEnable(AvatarInputHandler.aih_constants.CTRL_MODE_NAME.STRATEGIC)
			guiController.start()
	return

@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.StrategicControlMode, 'disable', invoke=XModLib.HookUtils.HookInvoke.PRIMARY)
def new_StrategicControlMode_disable(self, *args, **kwargs):
	if self is self._aih.ctrls[AvatarInputHandler.aih_constants.CTRL_MODE_NAME.STRATEGIC]:
		self.XAimCorrection.handleControlModeDisable()
		targetScanner = getattr(self._aih, 'XTargetScanner', None)
		if targetScanner is not None and targetScanner.isUpdateActive:
			targetScanner.stop()
		guiController = getattr(self._aih, 'XGuiController', None)
		if guiController is not None and guiController.isUpdateActive:
			guiController.handleControlModeDisable(AvatarInputHandler.aih_constants.CTRL_MODE_NAME.STRATEGIC)
			guiController.stop()
	return

@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.StrategicControlMode, 'getDesiredShotPoint', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_StrategicControlMode_getDesiredShotPoint(old_StrategicControlMode_getDesiredShotPoint, self, *args, **kwargs):
	shotPoint = old_StrategicControlMode_getDesiredShotPoint(self, *args, **kwargs)
	if self is self._aih.ctrls[AvatarInputHandler.aih_constants.CTRL_MODE_NAME.STRATEGIC]:
		return self.XAimCorrection.getDesiredShotPoint(shotPoint)
	return shotPoint
