# *************************
# StrategicControlMode Hooks
# *************************
@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.control_modes.StrategicControlMode, '__init__', calltype=XModLib.HookUtils.HookFunction.CALL_ORIGIN_BEFORE_HOOK)
def new_StrategicControlMode_init(self, *args, **kwargs):
	config = _config_['strategicAS']['aimCorrection']
	self.XAimCorrection = StrategicAimCorrection(
		config['manualMode']['enabled'],
		config['targetMode']['enabled'] and config['targetMode']['activated'],
		config['ignoreVehicles'],
		config['targetMode']['heightMultiplier']
	)
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.control_modes.StrategicControlMode, 'enable', calltype=XModLib.HookUtils.HookFunction.CALL_ORIGIN_BEFORE_HOOK)
def new_StrategicControlMode_enable(self, *args, **kwargs):
	self.XAimCorrection.handleControlModeEnable()
	targetScanner = getattr(self._aih, 'XTargetScanner', None)
	if targetScanner is not None and not targetScanner.isUpdateActive:
		targetScanner.start()
	guiController = getattr(self._aih, 'XGuiController', None)
	if guiController is not None and not guiController.isUpdateActive:
		guiController.start()
		guiController.handleControlModeEnable('strategic')
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.control_modes.StrategicControlMode, 'disable', calltype=XModLib.HookUtils.HookFunction.CALL_HOOK_BEFORE_ORIGIN)
def new_StrategicControlMode_disable(self, *args, **kwargs):
	self.XAimCorrection.handleControlModeDisable()
	targetScanner = getattr(self._aih, 'XTargetScanner', None)
	if targetScanner is not None and targetScanner.isUpdateActive:
		targetScanner.stop()
	guiController = getattr(self._aih, 'XGuiController', None)
	if guiController is not None and guiController.isUpdateActive:
		guiController.stop()
		guiController.handleControlModeDisable('strategic')
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.control_modes.StrategicControlMode, 'getDesiredShotPoint', calltype=XModLib.HookUtils.HookFunction.CALL_ORIGIN_INSIDE_HOOK)
def new_StrategicControlMode_getDesiredShotPoint(old_StrategicControlMode_getDesiredShotPoint, self, *args, **kwargs):
	shotPoint = old_StrategicControlMode_getDesiredShotPoint(self, *args, **kwargs)
	return self.XAimCorrection.getDesiredShotPoint(shotPoint)
