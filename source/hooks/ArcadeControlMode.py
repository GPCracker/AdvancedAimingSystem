# *************************
# ArcadeControlMode Hooks
# *************************
@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.control_modes.ArcadeControlMode, '__init__', calltype=XModLib.HookUtils.HookFunction.CALL_ORIGIN_BEFORE_HOOK)
def new_ArcadeControlMode_init(self, *args, **kwargs):
	config = _config_['arcadeAS']['aimCorrection']
	self.XAimCorrection = ArcadeAimCorrection(
		config['manualMode']['enabled'],
		config['targetMode']['enabled'] and config['targetMode']['activated']
	)
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.control_modes.ArcadeControlMode, 'enable', calltype=XModLib.HookUtils.HookFunction.CALL_ORIGIN_BEFORE_HOOK)
def new_ArcadeControlMode_enable(self, *args, **kwargs):
	self.XAimCorrection.handleControlModeEnable()
	targetScanner = getattr(BigWorld.player().inputHandler, 'XTargetScanner', None)
	if targetScanner is not None and not targetScanner.isUpdateActive:
		targetScanner.start()
	guiController = getattr(BigWorld.player().inputHandler, 'XGuiController', None)
	if guiController is not None and not guiController.isUpdateActive:
		guiController.start()
		guiController.handleControlModeEnable(avatar_helpers.aim_global_binding.CTRL_MODE_NAME.ARCADE)
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.control_modes.ArcadeControlMode, 'disable', calltype=XModLib.HookUtils.HookFunction.CALL_HOOK_BEFORE_ORIGIN)
def new_ArcadeControlMode_disable(self, *args, **kwargs):
	self.XAimCorrection.handleControlModeDisable()
	targetScanner = getattr(BigWorld.player().inputHandler, 'XTargetScanner', None)
	if targetScanner is not None and targetScanner.isUpdateActive:
		targetScanner.stop()
	guiController = getattr(BigWorld.player().inputHandler, 'XGuiController', None)
	if guiController is not None and guiController.isUpdateActive:
		guiController.stop()
		guiController.handleControlModeDisable(avatar_helpers.aim_global_binding.CTRL_MODE_NAME.ARCADE)
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.control_modes.ArcadeControlMode, 'getDesiredShotPoint', calltype=XModLib.HookUtils.HookFunction.CALL_ORIGIN_INSIDE_HOOK)
def new_ArcadeControlMode_getDesiredShotPoint(old_ArcadeControlMode_getDesiredShotPoint, self, *args, **kwargs):
	shotPoint = old_ArcadeControlMode_getDesiredShotPoint(self, *args, **kwargs)
	return self.XAimCorrection.getDesiredShotPoint(shotPoint)
