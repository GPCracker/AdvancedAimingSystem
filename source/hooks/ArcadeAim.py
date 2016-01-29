# *************************
# ArcadeAim Hooks
# *************************
@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.aims.ArcadeAim, '_update', calltype=XModLib.HookUtils.HookFunction.CALL_ORIGIN_BEFORE_HOOK)
def new_ArcadeAim_update(self, *args, **kwargs):
	inputHandler = BigWorld.player().inputHandler
	controlMode = inputHandler.ctrlModeName
	currentControl = inputHandler.ctrl
	## Update - Arcade
	if controlMode == 'arcade':
		config0 = _config_['arcadeAS']['targetLock']['autoMode']
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
		# Not implemented yet
		## TargetInfo - GUI
		if hasattr(currentControl, 'XTargetInfoGUI') and currentControl.XTargetInfoGUI is not None:
			config2 = _config_['arcadeAS']['targetLock']['gui']
			text = ''
			if hasattr(inputHandler, 'XTargetInfo') and inputHandler.XTargetInfo is not None:
				targetShortName = inputHandler.XTargetInfo.shortName
				targetSpeed = inputHandler.XTargetInfo.speed
				targetSpeed = targetSpeed * config2['speedMultiplier'] if targetSpeed is not None else 0.0
				text = _globals_['macrosFormatter'](config2['template'], targetShortName=targetShortName, targetSpeed=targetSpeed)
			currentControl.XTargetInfoGUI.gui.text = _globals_['umlautDecoder'](text)
		## AimingInfo - Update
		if hasattr(currentControl, 'XAimingInfo') and currentControl.XAimingInfo is not None:
			config3 = _config_['arcadeAS']['aimingInfo']
			text = ''
			aimingInfo = currentControl.XAimingInfo.aquireAimingInfo()
			if aimingInfo is not None:
				text = _globals_['macrosFormatter'](config3['template'].decode('string_escape'), **aimingInfo)
			currentControl.XAimingInfo.window.gui.label.text = _globals_['umlautDecoder'](text)
	## Update - Sniper
	if controlMode == 'sniper':
		config0 = _config_['sniperAS']['targetLock']['autoMode']
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
			config1 = _config_['sniperAS']['aimCorrection']['gui']
			shotMaxDistance = BigWorld.player().vehicleTypeDescriptor.shot['maxDistance']
			distance = None
			if hasattr(currentControl, 'XLockedDistance') and currentControl.XLockedDistance is not None:
				distance = currentControl.XLockedDistance
			elif _config_['sniperAS']['aimCorrection']['targetMode']['enabled'] and hasattr(inputHandler, 'XTargetInfo') and inputHandler.XTargetInfo is not None:
				cameraRay, cameraPoint = AvatarInputHandler.cameras.getWorldRayAndPoint(*currentControl.getAim().offset())
				distance = (inputHandler.XTargetInfo.position - cameraPoint).length
			text = _globals_['macrosFormatter'](config1['template'], distance=distance) if distance is not None else ''
			currentControl.XAimCorrectionGUI.gui.text = _globals_['umlautDecoder'](text)
			currentControl.XAimCorrectionGUI.gui.colour = config1['affectedColour'] if distance is not None and distance < shotMaxDistance else config1['unaffectedColour']
		## TargetInfo - GUI
		if hasattr(currentControl, 'XTargetInfoGUI') and currentControl.XTargetInfoGUI is not None:
			config2 = _config_['sniperAS']['targetLock']['gui']
			text = ''
			if hasattr(inputHandler, 'XTargetInfo') and inputHandler.XTargetInfo is not None:
				targetShortName = inputHandler.XTargetInfo.shortName
				targetSpeed = inputHandler.XTargetInfo.speed
				targetSpeed = targetSpeed * config2['speedMultiplier'] if targetSpeed is not None else 0.0
				text = _globals_['macrosFormatter'](config2['template'], targetShortName=targetShortName, targetSpeed=targetSpeed)
			currentControl.XTargetInfoGUI.gui.text = _globals_['umlautDecoder'](text)
		## AimingInfo - Update
		if hasattr(currentControl, 'XAimingInfo') and currentControl.XAimingInfo is not None:
			config3 = _config_['sniperAS']['aimingInfo']
			text = ''
			aimingInfo = currentControl.XAimingInfo.aquireAimingInfo()
			if aimingInfo is not None:
				text = _globals_['macrosFormatter'](config3['template'].decode('string_escape'), **aimingInfo)
			currentControl.XAimingInfo.window.gui.label.text = _globals_['umlautDecoder'](text)
	return
