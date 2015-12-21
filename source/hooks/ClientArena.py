# *************************
# ClientArena Hooks
# *************************
@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, ClientArena.ClientArena, 'collideWithSpaceBB', XModLib.HookUtils.HookFunction.CALL_ORIGIN_INSIDE_HOOK)
def new_ClientArena_collideWithSpaceBB(old_ClientArena_collideWithSpaceBB, self, start, end):
	inputHandler = BigWorld.player().inputHandler
	controlMode = inputHandler.ctrlModeName
	currentControl = inputHandler.ctrl
	if controlMode == 'sniper':
		cameraRay, cameraPoint = AvatarInputHandler.cameras.getWorldRayAndPoint(*currentControl.getAim().offset())
		distance = None
		if hasattr(currentControl, 'XLockedDistance') and currentControl.XLockedDistance is not None:
			distance = currentControl.XLockedDistance
		elif _config_['sniperAS']['aimCorrection']['targetMode']['enabled'] and hasattr(inputHandler, 'XTargetInfo') and inputHandler.XTargetInfo is not None:
			targetPosition = inputHandler.XTargetInfo.position
			if targetPosition is not None:
				distance = (targetPosition - cameraPoint).length
		if distance is not None:
			# We use simplified linear algorithm instead of square
			# Here performance is the name of the game
			# Although, this collision test is used only for aiming point calculations
			# And test beam is almost parallel to camera-result
			cs = start - cameraPoint
			ce = end - cameraPoint
			se = end - start
			if cs.length <= distance <= ce.length:
				return start + se * (distance - cs.length) / se.length
	return old_ClientArena_collideWithSpaceBB(self, start, end)

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, ClientArena.ClientArena, '_ClientArena__onVehicleKilled')
def new_ClientArena__onVehicleKilled(self, argStr):
	import cPickle
	victimID, killerID, equipmentID, reason = cPickle.loads(argStr)
	inputHandler = BigWorld.player().inputHandler
	if hasattr(inputHandler, 'XTargetInfo') and inputHandler.XTargetInfo is not None:
		if victimID == inputHandler.XTargetInfo.id:
			inputHandler.XTargetInfo = None
	if not hasattr(self, 'XVehiclesDeathTime') or self.XVehiclesDeathTime is None:
		self.XVehiclesDeathTime = dict()
	if hasattr(self, 'XVehiclesDeathTime') and self.XVehiclesDeathTime is not None:
		self.XVehiclesDeathTime[victimID] = BigWorld.time()
	return
