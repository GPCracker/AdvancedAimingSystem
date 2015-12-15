# *************************
# StrategicControlMode Hooks
# *************************
@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.control_modes.StrategicControlMode, 'enable')
def new_StrategicControlMode_enable(self, *args, **kwargs):
	## AimCorrection - ManualMode
	self.XLockedHeight = None
	## AimCorrection - GUI
	config0 = _config_['strategicAS']['aimCorrection']['gui']
	if config0['enabled']:
		if not hasattr(self, 'XAimCorrectionGUI') or self.XAimCorrectionGUI is None:
			## Init GUI
			self.XAimCorrectionGUI = XModLib.GUIWrapper.GUIWrapper.createGUI('Text', config0['settings'])
		if hasattr(self, 'XAimCorrectionGUI') and self.XAimCorrectionGUI is not None:
			## Set GUI visible
			self.XAimCorrectionGUI.gui.visible = True
	## TargetInfo - GUI
	config1 = _config_['strategicAS']['targetLock']['gui']
	if config1['enabled']:
		if not hasattr(self, 'XTargetInfoGUI') or self.XTargetInfoGUI is None:
			## Init GUI
			self.XTargetInfoGUI = XModLib.GUIWrapper.GUIWrapper.createGUI('Text', config1['settings'])
		if hasattr(self, 'XTargetInfoGUI') and self.XTargetInfoGUI is not None:
			## Set GUI visible
			self.XTargetInfoGUI.gui.visible = True
	## AimingInfo - GUI
	config2 = _config_['strategicAS']['aimingInfo']
	if config2['enabled']:
		if not hasattr(self, 'XAimingInfo') or self.XAimingInfo is None:
			## Init GUI
			self.XAimingInfo = AimingInfo(config2['settings']['window'], config2['settings']['label'])
		if hasattr(self, 'XAimingInfo') and self.XAimingInfo is not None:
			## Set GUI visible
			self.XAimingInfo.window.gui.visible = config2['activated']
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.control_modes.StrategicControlMode, 'disable')
def new_StrategicControlMode_disable(self, *args, **kwargs):
	## AimCorrection - ManualMode
	self.XLockedHeight = None
	## AimCorrection - GUI
	config0 = _config_['strategicAS']['aimCorrection']['gui']
	if config0['enabled']:
		if hasattr(self, 'XAimCorrectionGUI') and self.XAimCorrectionGUI is not None:
			## Set GUI invisible
			self.XAimCorrectionGUI.gui.visible = False
	## TargetInfo - GUI
	config1 = _config_['strategicAS']['targetLock']['gui']
	if config1['enabled']:
		if hasattr(self, 'XTargetInfoGUI') and self.XTargetInfoGUI is not None:
			## Set GUI invisible
			self.XTargetInfoGUI.gui.visible = False
	## AimingInfo - GUI
	config2 = _config_['strategicAS']['aimingInfo']
	if config2['enabled']:
		if hasattr(self, 'XAimingInfo') and self.XAimingInfo is not None:
			## Set GUI invisible
			self.XAimingInfo.window.gui.visible = False
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.control_modes.StrategicControlMode, 'getDesiredShotPoint', XModLib.HookUtils.HookFunction.CALL_ORIGIN_INSIDE_HOOK)
def new_StrategicControlMode_getDesiredShotPoint(old_StrategicControlMode_getDesiredShotPoint, self, *args, **kwargs):
	result = old_StrategicControlMode_getDesiredShotPoint(self, *args, **kwargs)
	## AimCorrection
	# AimCorrection was moved to AimingSystem
	return result
