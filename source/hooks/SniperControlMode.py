# *************************
# SniperControlMode Hooks
# *************************
@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.control_modes.SniperControlMode, 'enable', calltype=XModLib.HookUtils.HookFunction.CALL_ORIGIN_BEFORE_HOOK)
def new_SniperControlMode_enable(self, *args, **kwargs):
	## AimCorrection - ManualMode
	self.XLockedDistance = None
	## AimCorrection - GUI
	config0 = _config_['sniperAS']['aimCorrection']['gui']
	if config0['enabled']:
		if not hasattr(self, 'XAimCorrectionGUI') or self.XAimCorrectionGUI is None:
			## Init GUI
			self.XAimCorrectionGUI = XModLib.GUIWrapper.GUIWrapper.createGUI('Text', config0['settings'])
		if hasattr(self, 'XAimCorrectionGUI') and self.XAimCorrectionGUI is not None:
			## Set GUI visible
			self.XAimCorrectionGUI.gui.visible = True and BigWorld.player().isGuiVisible
	## TargetInfo - GUI
	config1 = _config_['sniperAS']['targetLock']['gui']
	if config1['enabled']:
		if not hasattr(self, 'XTargetInfoGUI') or self.XTargetInfoGUI is None:
			## Init GUI
			self.XTargetInfoGUI = XModLib.GUIWrapper.GUIWrapper.createGUI('Text', config1['settings'])
		if hasattr(self, 'XTargetInfoGUI') and self.XTargetInfoGUI is not None:
			## Set GUI visible
			self.XTargetInfoGUI.gui.visible = True and BigWorld.player().isGuiVisible
	## AimingInfo - GUI
	config2 = _config_['sniperAS']['aimingInfo']
	if config2['enabled']:
		if not hasattr(self, 'XAimingInfo') or self.XAimingInfo is None:
			## Init GUI
			self.XAimingInfo = AimingInfo(config2['settings']['window'], config2['settings']['label'])
		if hasattr(self, 'XAimingInfo') and self.XAimingInfo is not None:
			## Set GUI visible
			self.XAimingInfo.window.gui.visible = config2['activated'] and BigWorld.player().isGuiVisible
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.control_modes.SniperControlMode, 'disable', calltype=XModLib.HookUtils.HookFunction.CALL_HOOK_BEFORE_ORIGIN)
def new_SniperControlMode_disable(self, *args, **kwargs):
	## AimCorrection - ManualMode
	self.XLockedDistance = None
	## AimCorrection - GUI
	config0 = _config_['sniperAS']['aimCorrection']['gui']
	if config0['enabled']:
		if hasattr(self, 'XAimCorrectionGUI') and self.XAimCorrectionGUI is not None:
			## Set GUI invisible
			self.XAimCorrectionGUI.gui.visible = False
	## TargetInfo - GUI
	config1 = _config_['sniperAS']['targetLock']['gui']
	if config1['enabled']:
		if hasattr(self, 'XTargetInfoGUI') and self.XTargetInfoGUI is not None:
			## Set GUI invisible
			self.XTargetInfoGUI.gui.visible = False
	## AimingInfo - GUI
	config2 = _config_['sniperAS']['aimingInfo']
	if config2['enabled']:
		if hasattr(self, 'XAimingInfo') and self.XAimingInfo is not None:
			## Set GUI invisible
			self.XAimingInfo.window.gui.visible = False
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.control_modes.SniperControlMode, 'getDesiredShotPoint', calltype=XModLib.HookUtils.HookFunction.CALL_ORIGIN_INSIDE_HOOK)
def new_SniperControlMode_getDesiredShotPoint(old_SniperControlMode_getDesiredShotPoint, self, *args, **kwargs):
	result = old_SniperControlMode_getDesiredShotPoint(self, *args, **kwargs)
	## AimCorrection
	if result is not None:
		cameraRay, cameraPoint = AvatarInputHandler.cameras.getWorldRayAndPoint(*self.getAim().offset())
		cameraRay.normalise()
		## AimCorrection - ManualMode
		if hasattr(self, 'XLockedDistance') and self.XLockedDistance is not None:
			result = cameraPoint + cameraRay.scale(self.XLockedDistance)
		## AimCorrection - TargetMode
		elif _config_['sniperAS']['aimCorrection']['targetMode']['enabled']:
			inputHandler = BigWorld.player().inputHandler
			if hasattr(inputHandler, 'XTargetInfo') and inputHandler.XTargetInfo is not None:
				# Disable correction when target is focused
				target = BigWorld.target()
				if target is None or target.id != inputHandler.XTargetInfo.id:
					result = cameraPoint + cameraRay.scale((inputHandler.XTargetInfo.position - cameraPoint).length)
	return result
