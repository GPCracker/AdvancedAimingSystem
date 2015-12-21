# *************************
# StrategicAimingSystem Hooks
# *************************
@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.AimingSystems.StrategicAimingSystem.StrategicAimingSystem, 'handleMovement', XModLib.HookUtils.HookFunction.CALL_ORIGIN_INSIDE_HOOK)
def new_StrategicAimingSystem_handleMovement(old_StrategicAimingSystem_handleMovement, self, dx, dy):
	if BigWorld.player().inputHandler.ctrlModeName != 'strategic':
		return old_StrategicAimingSystem_handleMovement(self, dx, dy)
	if not hasattr(self, 'XStrategicSniper') or self.XStrategicSniper is None or not self.XStrategicSniper.isSniperMode:
		return old_StrategicAimingSystem_handleMovement(self, dx, dy)
	pointFixed = False
	shiftVector = self.XStrategicSniper.getCameraShift(Math.Vector3(dx, 0.0, dy))
	movementDirection = shiftVector.dot(self.XStrategicSniper.getCameraShift(Math.Vector3(0, 0, 1)))
	cameraControlPosition = self.XStrategicSniper.cameraControlPosition + shiftVector
	landPoint, landVector, dummy = self.XStrategicSniper.computeLPbyCP(cameraControlPosition)
	if movementDirection < 0:
		# Player tries to move camera to himself. We need to check distance.
		playerVehiclePosition = BigWorld.player().getOwnVehiclePosition()
		if playerVehiclePosition.flatDistSqrTo(landPoint) < self.XStrategicSniper.criticalDistance ** 2:
			# Player tries to move camera too close to himself. Player position is a critical point - transform matrix could not be calculated.
			if pointFixed:
				# We already fixed something. We can not fix twice.
				# We block.
				return
			# We need to block this movement smoothly.
			# Calculating land point on minimal distance/ It could not be on land at all.
			landPoint = playerVehiclePosition + XModLib.ExtraMath.ExtraMath.normalisedVector(landPoint - playerVehiclePosition).scale(self.XStrategicSniper.criticalDistance)
			# Getting real land point (projecting it on land).
			landPoint, landVector, dummy = self.XStrategicSniper.computeLPbyMP(landPoint)
			# Now we need to recalculate points and then we are partially sure that issue was removed.
			cameraControlPosition, dummy, dummy = self.XStrategicSniper.computeCPbyLP(landPoint)
			landPoint, landVector, dummy = self.XStrategicSniper.computeLPbyCP(cameraControlPosition)
			# Setting a flag for future use.
			pointFixed = True
			# But if player stands before a wall, it will not succeed. Checking it.
			# Remember that float numbers does not have exact values. Use one meter less distance.
			if playerVehiclePosition.flatDistSqrTo(landPoint) < (self.XStrategicSniper.criticalDistance - 1.0) ** 2:
				# Now we are sure correction failed. Blocking movement by one coordinate.
				shiftVector = self.XStrategicSniper.getCameraShift(Math.Vector3(dx, 0.0, 0.0))
				cameraControlPosition = self.XStrategicSniper.cameraControlPosition + shiftVector
				movementDirection = shiftVector.dot(self.XStrategicSniper.getCameraShift(Math.Vector3(0, 0, 1)))
				landPoint, landVector, dummy = self.XStrategicSniper.computeLPbyCP(cameraControlPosition)
	# Now we are sure that distance to player is correct or blocked. Going ahead.
	# We already have calculated points.
	if movementDirection > 0:
		# Player tries to move camera from himself.
		# If player vehicle has low-distance gun we can "slide down" when maximum distance is reached.
		# This movements should be partially blocked.
		# This takes computational time, but not required for long range guns, so it has a property.
		if self.XStrategicSniper.correctMaxDistance and self.XStrategicSniper.computeCPbyLP(landPoint)[0].flatDistSqrTo(cameraControlPosition) > 1.0:
			# Backward calculated control point does not match a calculated control point after movement. It means maximum distance reached.
			if pointFixed:
				# We already fixed something. We can not fix twice.
				# We block.
				return
			# We need to block it. We could not find a distance correct, but we ignore it - we slowly "slide down".
			# So we block it all.
			pointFixed = True
			return
	# Now we are partially sure that distance is okay and we going ahead.
	# Now we need to check that we are inside arena.
	# Exiting arena could cause an critical error.
	if not self.XStrategicSniper.arenaBoundingBox.isPointInsideBox(landPoint):
		if pointFixed:
			# We already fixed something. We can not fix twice.
			# We block.
			return
		# Player are tried to leave arena. We should return him back.
		# Projecting point on arena box and on land next.
		landPoint, landVector, dummy = self.XStrategicSniper.computeLPbyMP(self.XStrategicSniper.arenaBoundingBox.projectExternalPointOnBox(landPoint))
		# Now we should recalculate all points.
		cameraControlPosition, dummy, dummy = self.XStrategicSniper.computeCPbyLP(landPoint)
		landPoint, landVector, dummy = self.XStrategicSniper.computeLPbyCP(cameraControlPosition)
	# Now we are sure that player is inside arena and we accepting this movement.
	self.XStrategicSniper.cameraControlPosition = cameraControlPosition
	self.matrix.translation = landPoint + Math.Vector3(0, self.height, 0)
	self.XStrategicSniper.updateCameraYaw(landVector.yaw)
	self.XStrategicSniper.updateCameraPitch(landVector.pitch)
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.AimingSystems.StrategicAimingSystem.StrategicAimingSystem, 'updateTargetPos', XModLib.HookUtils.HookFunction.CALL_ORIGIN_INSIDE_HOOK)
def new_StrategicAimingSystem_updateTargetPos(old_StrategicAimingSystem_updateTargetPos, self, targetPos):
	if BigWorld.player().inputHandler.ctrlModeName != 'strategic':
		return old_StrategicAimingSystem_updateTargetPos(self, targetPos)
	if not hasattr(self, 'XStrategicSniper') or self.XStrategicSniper is None or not self.XStrategicSniper.isSniperMode:
		return old_StrategicAimingSystem_updateTargetPos(self, targetPos)
	# Target position is a 2D point inside arena.
	# In this method we should pass any request, we could change it but could not block.
	# So we just recalculating points, fixing maximum distance automatically.
	# Anyway, player will not be able to make situation worst by movement.
	# It will be corrected or blocked.
	# This situation is not good for user, but better than camera control losses
	# aka "camera quake" or game unexpected termination.
	# User should understand this situation and not do something like this.
	# I think several attempts for normal player will be enough.
	# We project point on the land.
	landPoint, landVector, dummy = self.XStrategicSniper.computeLPbyMP(targetPos)
	# And recalculating points.
	cameraControlPosition, dummy, dummy = self.XStrategicSniper.computeCPbyLP(landPoint)
	landPoint, landVector, dummy = self.XStrategicSniper.computeLPbyCP(cameraControlPosition)
	# Accepting this
	self.XStrategicSniper.cameraControlPosition = cameraControlPosition
	self.matrix.translation = landPoint + Math.Vector3(0, self.height, 0)
	self.XStrategicSniper.updateCameraYaw(landVector.yaw)
	self.XStrategicSniper.updateCameraPitch(landVector.pitch)
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.AimingSystems.StrategicAimingSystem.StrategicAimingSystem, 'getDesiredShotPoint', XModLib.HookUtils.HookFunction.CALL_ORIGIN_INSIDE_HOOK)
def new_StrategicAimingSystem_getDesiredShotPoint(old_StrategicAimingSystem_getDesiredShotPoint, self, terrainOnlyCheck = False):
	if BigWorld.player().inputHandler.ctrlModeName != 'strategic':
		return old_StrategicAimingSystem_getDesiredShotPoint(self, terrainOnlyCheck)
	if hasattr(self, 'XStrategicSniper') and self.XStrategicSniper is not None and self.XStrategicSniper.isSniperMode:
		cameraRay, cameraPoint = AvatarInputHandler.cameras.getWorldRayAndPoint(*BigWorld.player().inputHandler.aim.offset())
		return AvatarInputHandler.AimingSystems.getDesiredShotPoint(cameraPoint, cameraRay, True, False)
	## AimCorrection
	config0 = _config_['strategicAS']['aimCorrection']['relativeMode']
	result = old_StrategicAimingSystem_getDesiredShotPoint(self, terrainOnlyCheck or (config0['enabled'] and config0['ignoreVehicles']))
	if result is not None:
		inputHandler = BigWorld.player().inputHandler
		currentControl = inputHandler.ctrl
		## AimCorrection - ManualMode
		if hasattr(currentControl, 'XLockedHeight') and currentControl.XLockedHeight is not None:
			result.y = currentControl.XLockedHeight
		## AimCorrection - TargetMode
		elif config0['enabled'] and config0['activated']:
			if hasattr(inputHandler, 'XTargetInfo') and inputHandler.XTargetInfo is not None:
				target = BigWorld.target()
				if target is None or target.id != inputHandler.XTargetInfo.id or config0['ignoreVehicles']:
					result += inputHandler.XTargetInfo.heightVector.scale(config0['heightMultiplier'])
	return result
