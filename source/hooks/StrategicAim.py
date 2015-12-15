# *************************
# StrategicAim Hooks
# *************************
@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.aims.StrategicAim, '_update')
def new_StrategicAim_update(self, *args, **kwargs):
	inputHandler = BigWorld.player().inputHandler
	controlMode = inputHandler.ctrlModeName
	currentControl = inputHandler.ctrl
	## Update - Strategic
	if controlMode is 'strategic':
		config0 = _config_['strategicAS']['targetLock']['autoMode']
		## TargetLock - AutoMode - Lock/Update
		if config0['enabled']:
			target = BigWorld.target()
			target = target if XModLib.VehicleInfo.VehicleInfo.isVehicle(target) else None
			if target is None and config0['useXRay']:
				target = XModLib.XRayScanner.XRayScanner.getTarget()
			if target is not None and target.isAlive():
				if config0['allies'] or target.publicInfo['team'] is not BigWorld.player().team:
					if not hasattr(inputHandler, 'XTargetInfo') or inputHandler.XTargetInfo is None or (inputHandler.XTargetInfo.id != target.id and inputHandler.XTargetInfo.isAutoLocked):
						inputHandler.XTargetInfo = TargetInfo(target, BigWorld.time())
					elif inputHandler.XTargetInfo.isAutoLocked:
						inputHandler.XTargetInfo.lockTime = BigWorld.time()
		## TargetLock - AutoMode - Reset
		if hasattr(inputHandler, 'XTargetInfo') and inputHandler.XTargetInfo is not None and inputHandler.XTargetInfo.isAutoLocked:
			if (BigWorld.time() - inputHandler.XTargetInfo.lockTime) > config0['timeout'] > 0.0:
				inputHandler.XTargetInfo = None
		## AimCorrection - GUI
		if hasattr(currentControl, 'XAimCorrectionGUI') and currentControl.XAimCorrectionGUI is not None:
			config1 = _config_['strategicAS']['aimCorrection']['gui']
			absoluteHeight = None
			relativeHeight = None
			if hasattr(currentControl, 'XLockedHeight') and currentControl.XLockedHeight is not None:
				absoluteHeight = currentControl.XLockedHeight
				relativeHeight = absoluteHeight - BigWorld.player().getOwnVehiclePosition().y
			if hasattr(inputHandler, 'XTargetInfo') and inputHandler.XTargetInfo is not None:
				absoluteHeight = inputHandler.XTargetInfo.position.y
				relativeHeight=relativeHeight = absoluteHeight - BigWorld.player().getOwnVehiclePosition().y
			text = _globals_['macrosFormatter'](config1['template'], absoluteHeight=absoluteHeight, relativeHeight=relativeHeight) if absoluteHeight is not None and relativeHeight is not None else ''
			currentControl.XAimCorrectionGUI.gui.text = _globals_['umlautDecoder'](text)
		## TargetInfo - GUI
		if hasattr(currentControl, 'XTargetInfoGUI') and currentControl.XTargetInfoGUI is not None:
			config2 = _config_['strategicAS']['targetLock']['gui']
			text = ''
			if hasattr(inputHandler, 'XTargetInfo') and inputHandler.XTargetInfo is not None:
				targetShortName = inputHandler.XTargetInfo.shortName
				targetSpeed = inputHandler.XTargetInfo.speed
				targetSpeed = targetSpeed * config2['speedMultiplier'] if targetSpeed is not None else 0.0
				text = _globals_['macrosFormatter'](config2['template'], targetShortName=targetShortName, targetSpeed=targetSpeed)
			currentControl.XTargetInfoGUI.gui.text = _globals_['umlautDecoder'](text)
		## AimingInfo - Update
		if hasattr(currentControl, 'XAimingInfo') and currentControl.XAimingInfo is not None:
			config3 = _config_['strategicAS']['aimingInfo']
			text = ''
			aimingInfo = currentControl.XAimingInfo.aquireAimingInfo()
			if aimingInfo is not None:
				text = _globals_['macrosFormatter'](config3['template'].decode('string_escape'), **aimingInfo)
			currentControl.XAimingInfo.window.gui.label.text = _globals_['umlautDecoder'](text)
	return
