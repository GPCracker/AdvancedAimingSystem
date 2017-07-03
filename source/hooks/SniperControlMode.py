# *************************
# SniperControlMode Hooks
# *************************
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.SniperControlMode, '__init__', invoke=XModLib.HookUtils.HookInvoke.SECONDARY)
def new_SniperControlMode_init(self, *args, **kwargs):
	config = _config_['sniperAS']['aimCorrection']
	self.XAimCorrection = SniperAimCorrection(
		self,
		config['manualMode']['enabled'],
		config['targetMode']['enabled'] and config['targetMode']['activated'],
		config['targetMode']['distance'][0],
		config['targetMode']['distance'][1]
	)
	return

@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.SniperControlMode, 'enable', invoke=XModLib.HookUtils.HookInvoke.SECONDARY)
def new_SniperControlMode_enable(self, *args, **kwargs):
	if self is self._aih.ctrls[AvatarInputHandler.aih_constants.CTRL_MODE_NAME.SNIPER]:
		self.XAimCorrection.handleControlModeEnable()
		targetScanner = getattr(self._aih, 'XTargetScanner', None)
		if targetScanner is not None and not targetScanner.isUpdateActive:
			targetScanner.start()
		guiController = getattr(self._aih, 'XGuiController', None)
		if guiController is not None and not guiController.isUpdateActive:
			guiController.handleControlModeEnable(AvatarInputHandler.aih_constants.CTRL_MODE_NAME.SNIPER)
			guiController.start()
	return

@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.SniperControlMode, 'disable', invoke=XModLib.HookUtils.HookInvoke.PRIMARY)
def new_SniperControlMode_disable(self, *args, **kwargs):
	if self is self._aih.ctrls[AvatarInputHandler.aih_constants.CTRL_MODE_NAME.SNIPER]:
		self.XAimCorrection.handleControlModeDisable()
		targetScanner = getattr(self._aih, 'XTargetScanner', None)
		if targetScanner is not None and targetScanner.isUpdateActive:
			targetScanner.stop()
		guiController = getattr(self._aih, 'XGuiController', None)
		if guiController is not None and guiController.isUpdateActive:
			guiController.handleControlModeDisable(AvatarInputHandler.aih_constants.CTRL_MODE_NAME.SNIPER)
			guiController.stop()
	return

@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.SniperControlMode, 'getDesiredShotPoint', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_SniperControlMode_getDesiredShotPoint(old_SniperControlMode_getDesiredShotPoint, self, *args, **kwargs):
	shotPoint = old_SniperControlMode_getDesiredShotPoint(self, *args, **kwargs)
	if self is self._aih.ctrls[AvatarInputHandler.aih_constants.CTRL_MODE_NAME.SNIPER]:
		return self.XAimCorrection.getDesiredShotPoint(shotPoint)
	return shotPoint
