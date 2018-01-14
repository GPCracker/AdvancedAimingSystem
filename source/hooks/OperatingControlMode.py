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
			fixGunMarker=config['fixGunMarker'],
			manualEnabled=config['manualMode']['enabled'],
			targetEnabled=config['targetMode']['enabled'] and config['targetMode']['activated'],
			minDistance=config['targetMode']['distance'][0],
			maxDistance=config['targetMode']['distance'][1]
		) if config['enabled'] else None
	elif type(self) is AvatarInputHandler.control_modes.SniperControlMode:
		config = _config_['modules']['aimCorrection'][AvatarInputHandler.aih_constants.CTRL_MODE_NAME.SNIPER]
		self.XAimCorrection = SniperAimCorrection(
			self,
			fixGunMarker=config['fixGunMarker'],
			manualEnabled=config['manualMode']['enabled'],
			targetEnabled=config['targetMode']['enabled'] and config['targetMode']['activated'],
			minDistance=config['targetMode']['distance'][0],
			maxDistance=config['targetMode']['distance'][1]
		) if config['enabled'] else None
	elif type(self) is AvatarInputHandler.control_modes.StrategicControlMode:
		config = _config_['modules']['aimCorrection'][AvatarInputHandler.aih_constants.CTRL_MODE_NAME.STRATEGIC]
		self.XAimCorrection = StrategicAimCorrection(
			self,
			fixGunMarker=config['fixGunMarker'],
			manualEnabled=config['manualMode']['enabled'],
			targetEnabled=config['targetMode']['enabled'] and config['targetMode']['activated'],
			ignoreVehicles=config['ignoreVehicles'],
			heightMultiplier=config['targetMode']['heightMultiplier']
		) if config['enabled'] else None
	elif type(self) is AvatarInputHandler.control_modes.ArtyControlMode:
		config = _config_['modules']['aimCorrection'][AvatarInputHandler.aih_constants.CTRL_MODE_NAME.ARTY]
		self.XAimCorrection = ArtyAimCorrection(
			self,
			fixGunMarker=config['fixGunMarker'],
			manualEnabled=config['manualMode']['enabled'],
			targetEnabled=config['targetMode']['enabled'] and config['targetMode']['activated']
		) if config['enabled'] else None
	return

@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.ArcadeControlMode, 'enable', invoke=XModLib.HookUtils.HookInvoke.SECONDARY)
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.SniperControlMode, 'enable', invoke=XModLib.HookUtils.HookInvoke.SECONDARY)
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.StrategicControlMode, 'enable', invoke=XModLib.HookUtils.HookInvoke.SECONDARY)
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.ArtyControlMode, 'enable', invoke=XModLib.HookUtils.HookInvoke.SECONDARY)
def new_OperatingControlMode_enable(self, *args, **kwargs):
	# These strict type checks ensure hooks will work only in original classes themselves, but not in their subclasses.
	if type(self) in (AvatarInputHandler.control_modes.ArcadeControlMode, AvatarInputHandler.control_modes.SniperControlMode, AvatarInputHandler.control_modes.StrategicControlMode, AvatarInputHandler.control_modes.ArtyControlMode):
		aimCorrection = getattr(self, 'XAimCorrection', None)
		if aimCorrection is not None:
			aimCorrection.enable()
		targetScanner = getattr(self._aih, 'XTargetScanner', None)
		if targetScanner is not None and not targetScanner.isUpdateActive:
			targetScanner.start()
		guiController = getattr(self._aih, 'XGuiController', None)
		if guiController is not None and not guiController.isUpdateActive:
			guiController.start()
	return

@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.ArcadeControlMode, 'disable', invoke=XModLib.HookUtils.HookInvoke.PRIMARY)
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.SniperControlMode, 'disable', invoke=XModLib.HookUtils.HookInvoke.PRIMARY)
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.StrategicControlMode, 'disable', invoke=XModLib.HookUtils.HookInvoke.PRIMARY)
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.ArtyControlMode, 'disable', invoke=XModLib.HookUtils.HookInvoke.PRIMARY)
def new_OperatingControlMode_disable(self, *args, **kwargs):
	# These strict type checks ensure hooks will work only in original classes themselves, but not in their subclasses.
	if type(self) in (AvatarInputHandler.control_modes.ArcadeControlMode, AvatarInputHandler.control_modes.SniperControlMode, AvatarInputHandler.control_modes.StrategicControlMode, AvatarInputHandler.control_modes.ArtyControlMode):
		aimCorrection = getattr(self, 'XAimCorrection', None)
		if aimCorrection is not None:
			aimCorrection.disable()
		targetScanner = getattr(self._aih, 'XTargetScanner', None)
		if targetScanner is not None and targetScanner.isUpdateActive:
			targetScanner.stop()
		guiController = getattr(self._aih, 'XGuiController', None)
		if guiController is not None and guiController.isUpdateActive:
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
		aimCorrection = getattr(self, 'XAimCorrection', None)
		if aimCorrection is not None:
			return aimCorrection.getDesiredShotPoint(shotPoint)
	return shotPoint
