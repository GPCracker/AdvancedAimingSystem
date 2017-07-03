# *************************
# OperatingControlMode Hooks
# *************************
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.ArcadeControlMode, '__init__')
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.SniperControlMode, '__init__')
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.StrategicControlMode, '__init__')
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.ArtyControlMode, '__init__')
def new_OperatingControlMode_init(self, *args, **kwargs):
	# These strict type checks ensure hooks will work only in original classes themselves, but not in their subclasses.
	if type(self) is AvatarInputHandler.control_modes.ArcadeControlMode:
		config = _config_['modules']['aimCorrection'][AvatarInputHandler.aih_constants.CTRL_MODE_NAME.ARCADE]
		self.XAimCorrection = ArcadeAimCorrection(
			self,
			config['manualMode']['enabled'],
			config['targetMode']['enabled'] and config['targetMode']['activated'],
			config['targetMode']['distance'][0],
			config['targetMode']['distance'][1]
		)
	elif type(self) is AvatarInputHandler.control_modes.SniperControlMode:
		config = _config_['modules']['aimCorrection'][AvatarInputHandler.aih_constants.CTRL_MODE_NAME.SNIPER]
		self.XAimCorrection = SniperAimCorrection(
			self,
			config['manualMode']['enabled'],
			config['targetMode']['enabled'] and config['targetMode']['activated'],
			config['targetMode']['distance'][0],
			config['targetMode']['distance'][1]
		)
	elif type(self) is AvatarInputHandler.control_modes.StrategicControlMode:
		config = _config_['modules']['aimCorrection'][AvatarInputHandler.aih_constants.CTRL_MODE_NAME.STRATEGIC]
		self.XAimCorrection = StrategicAimCorrection(
			self,
			config['manualMode']['enabled'],
			config['targetMode']['enabled'] and config['targetMode']['activated'],
			config['ignoreVehicles'],
			config['targetMode']['heightMultiplier']
		)
	elif type(self) is AvatarInputHandler.control_modes.ArtyControlMode:
		config = _config_['modules']['aimCorrection'][AvatarInputHandler.aih_constants.CTRL_MODE_NAME.ARTY]
		self.XAimCorrection = ArtyAimCorrection(
			self,
			config['manualMode']['enabled'],
			config['targetMode']['enabled'] and config['targetMode']['activated']
		)
	return

@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.ArcadeControlMode, 'enable', invoke=XModLib.HookUtils.HookInvoke.SECONDARY)
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.SniperControlMode, 'enable', invoke=XModLib.HookUtils.HookInvoke.SECONDARY)
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.StrategicControlMode, 'enable', invoke=XModLib.HookUtils.HookInvoke.SECONDARY)
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.ArtyControlMode, 'enable', invoke=XModLib.HookUtils.HookInvoke.SECONDARY)
def new_OperatingControlMode_enable(self, *args, **kwargs):
	# These strict type checks ensure hooks will work only in original classes themselves, but not in their subclasses.
	if type(self) in (AvatarInputHandler.control_modes.ArcadeControlMode, AvatarInputHandler.control_modes.SniperControlMode, AvatarInputHandler.control_modes.StrategicControlMode, AvatarInputHandler.control_modes.ArtyControlMode):
		self.XAimCorrection.handleControlModeEnable()
		targetScanner = getattr(self._aih, 'XTargetScanner', None)
		if targetScanner is not None and not targetScanner.isUpdateActive:
			targetScanner.start()
		guiController = getattr(self._aih, 'XGuiController', None)
		if guiController is not None and not guiController.isUpdateActive:
			ctrlModeName = next(name for name, ctrl in self._aih.ctrls.viewitems() if ctrl is self)
			guiController.handleControlModeEnable(ctrlModeName)
			guiController.start()
	return

@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.ArcadeControlMode, 'disable', invoke=XModLib.HookUtils.HookInvoke.PRIMARY)
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.SniperControlMode, 'disable', invoke=XModLib.HookUtils.HookInvoke.PRIMARY)
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.StrategicControlMode, 'disable', invoke=XModLib.HookUtils.HookInvoke.PRIMARY)
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.ArtyControlMode, 'disable', invoke=XModLib.HookUtils.HookInvoke.PRIMARY)
def new_OperatingControlMode_disable(self, *args, **kwargs):
	# These strict type checks ensure hooks will work only in original classes themselves, but not in their subclasses.
	if type(self) in (AvatarInputHandler.control_modes.ArcadeControlMode, AvatarInputHandler.control_modes.SniperControlMode, AvatarInputHandler.control_modes.StrategicControlMode, AvatarInputHandler.control_modes.ArtyControlMode):
		self.XAimCorrection.handleControlModeDisable()
		targetScanner = getattr(self._aih, 'XTargetScanner', None)
		if targetScanner is not None and targetScanner.isUpdateActive:
			targetScanner.stop()
		guiController = getattr(self._aih, 'XGuiController', None)
		if guiController is not None and guiController.isUpdateActive:
			ctrlModeName = next(name for name, ctrl in self._aih.ctrls.viewitems() if ctrl is self)
			guiController.handleControlModeDisable(ctrlModeName)
			guiController.stop()
	return

@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.ArcadeControlMode, 'getDesiredShotPoint', invoke=XModLib.HookUtils.HookInvoke.MASTER)
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.SniperControlMode, 'getDesiredShotPoint', invoke=XModLib.HookUtils.HookInvoke.MASTER)
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.StrategicControlMode, 'getDesiredShotPoint', invoke=XModLib.HookUtils.HookInvoke.MASTER)
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.ArtyControlMode, 'getDesiredShotPoint', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_OperatingControlMode_getDesiredShotPoint(old_OperatingControlMode_getDesiredShotPoint, self, *args, **kwargs):
	shotPoint = old_OperatingControlMode_getDesiredShotPoint(self, *args, **kwargs)
	# These strict type checks ensure hooks will work only in original classes themselves, but not in their subclasses.
	if type(self) in (AvatarInputHandler.control_modes.ArcadeControlMode, AvatarInputHandler.control_modes.SniperControlMode, AvatarInputHandler.control_modes.StrategicControlMode, AvatarInputHandler.control_modes.ArtyControlMode):
		return self.XAimCorrection.getDesiredShotPoint(shotPoint)
	return shotPoint
