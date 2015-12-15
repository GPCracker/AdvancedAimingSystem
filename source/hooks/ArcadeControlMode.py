# *************************
# ArcadeControlMode Hooks
# *************************
@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.control_modes.ArcadeControlMode, 'enable')
def new_ArcadeControlMode_enable(self, *args, **kwargs):
	## AimCorrection - ManualMode
	# Not implemented yet
	## AimCorrection - GUI
	# Not implemented yet
	## TargetInfo - GUI
	config1 = _config_['arcadeAS']['targetLock']['gui']
	if config1['enabled']:
		if not hasattr(self, 'XTargetInfoGUI') or self.XTargetInfoGUI is None:
			## Init GUI
			self.XTargetInfoGUI = XModLib.GUIWrapper.GUIWrapper.createGUI('Text', config1['settings'])
		if hasattr(self, 'XTargetInfoGUI') and self.XTargetInfoGUI is not None:
			## Set GUI visible
			self.XTargetInfoGUI.gui.visible = True
	## AimingInfo - GUI
	config2 = _config_['arcadeAS']['aimingInfo']
	if config2['enabled']:
		if not hasattr(self, 'XAimingInfo') or self.XAimingInfo is None:
			## Init GUI
			self.XAimingInfo = AimingInfo(config2['settings']['window'], config2['settings']['label'])
		if hasattr(self, 'XAimingInfo') and self.XAimingInfo is not None:
			## Set GUI visible
			self.XAimingInfo.window.gui.visible = config2['activated']
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.control_modes.ArcadeControlMode, 'disable')
def new_ArcadeControlMode_disable(self, *args, **kwargs):
	## AimCorrection - ManualMode
	# Not implemented yet
	## AimCorrection - GUI
	# Not implemented yet
	## TargetInfo - GUI
	config1 = _config_['arcadeAS']['targetLock']['gui']
	if config1['enabled']:
		if hasattr(self, 'XTargetInfoGUI') and self.XTargetInfoGUI is not None:
			## Set GUI invisible
			self.XTargetInfoGUI.gui.visible = False
	## AimingInfo - GUI
	config2 = _config_['arcadeAS']['aimingInfo']
	if config2['enabled']:
		if hasattr(self, 'XAimingInfo') and self.XAimingInfo is not None:
			## Set GUI invisible
			self.XAimingInfo.window.gui.visible = False
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.control_modes.ArcadeControlMode, 'getDesiredShotPoint', XModLib.HookUtils.HookFunction.CALL_ORIGIN_INSIDE_HOOK)
def new_ArcadeControlMode_getDesiredShotPoint(old_ArcadeControlMode_getDesiredShotPoint, self, *args, **kwargs):
	result = old_ArcadeControlMode_getDesiredShotPoint(self, *args, **kwargs)
	## AimCorrection
	# Not implemented yet
	return result
