# *************************
# AimCorrection Class
# *************************
class BaseAimCorrection(object):
	@classmethod
	def getInputHandlerCtrl(sclass):
		return BigWorld.player().inputHandler.ctrl

	def __init__(self, manualEnabled=False, targetEnabled=False):
		self.manualEnabled = manualEnabled
		self.targetEnabled = targetEnabled
		self.manualInfo = None
		return

	@property
	def targetInfo(self):
		return getattr(BigWorld.player().inputHandler, 'XTargetInfo', None)

	def getMacroData(self):
		return {
			'manualInfo': self.manualInfo
		} if self.manualEnabled and self.manualInfo is not None else None

	def setManualInfo(self):
		if self.manualEnabled:
			self.manualInfo = None
		return

	def resetManualInfo(self):
		if self.manualEnabled:
			self.manualInfo = None
		return

	def handleControlModeEnable(self):
		self.manualInfo = None
		return

	def handleControlModeDisable(self):
		self.manualInfo = None
		return

	def _getManualDesiredShotPoint(self, shotPoint):
		return None

	def _getTargetDesiredShotPoint(self, shotPoint):
		return None

	def getDesiredShotPoint(self, shotPoint):
		return self._getManualDesiredShotPoint(shotPoint) or self._getTargetDesiredShotPoint(shotPoint) or shotPoint

	def getGunMarkerCollisionPoint(self, start, end):
		return None

	def __del__(self):
		return

class ArcadeAimCorrection(BaseAimCorrection):
	@classmethod
	def getScanRayAndPoint(sclass):
		aimingSystemMatrix = sclass.getInputHandlerCtrl().camera.aimingSystem.matrix
		return aimingSystemMatrix.applyToAxis(2), aimingSystemMatrix.applyToOrigin()

	@classmethod
	def getPositionAboveVehicle(sclass):
		return sclass.getInputHandlerCtrl().camera.aimingSystem.positionAboveVehicleProv.value[0:3]

	def setManualInfo(self):
		if self.manualEnabled:
			shotPoint = self.getInputHandlerCtrl().getDesiredShotPoint()
			if shotPoint is not None:
				self.manualInfo = self.getPositionAboveVehicle().flatDistTo(shotPoint)
		return

	def _getManualDesiredShotPoint(self, shotPoint):
		if self.manualEnabled and shotPoint is not None:
			if self.manualInfo is not None:
				scanRay, scanPoint = self.getScanRayAndPoint()
				flatDistance = scanPoint.flatDistTo(self.getPositionAboveVehicle()) + self.manualInfo
				flatScanRayLength = scanRay.flatDistTo(Math.Vector3(0.0, 0.0, 0.0))
				return scanPoint + scanRay.scale(flatDistance / flatScanRayLength)
		return None

	def _getTargetDesiredShotPoint(self, shotPoint):
		if self.targetEnabled and shotPoint is not None:
			if self.targetInfo is not None and not self.targetInfo.isExpired:
				target = BigWorld.target()
				if target is None or target.id != self.targetInfo:
					scanRay, scanPoint = self.getScanRayAndPoint()
					flatDistance = scanPoint.flatDistTo(self.targetInfo.getPosition())
					flatScanRayLength = scanRay.flatDistTo(Math.Vector3(0.0, 0.0, 0.0))
					return scanPoint + scanRay.scale(flatDistance / flatScanRayLength)
		return None

	def getGunMarkerCollisionPoint(self, start, end):
		flatDistance = None
		positionAboveVehicle = self.getPositionAboveVehicle()
		if self.manualEnabled and self.manualInfo is not None:
			flatDistance = self.manualInfo
		elif self.targetEnabled and self.targetInfo is not None and not self.targetInfo.isExpired:
			flatDistance = positionAboveVehicle.flatDistTo(self.targetInfo.getPosition())
		if flatDistance is not None:
			if positionAboveVehicle.flatDistSqrTo(start) <= flatDistance * flatDistance <= positionAboveVehicle.flatDistSqrTo(end):
				return start + (end - start).scale((flatDistance - positionAboveVehicle.flatDistTo(start)) / start.flatDistTo(end))
		return None

class SniperAimCorrection(BaseAimCorrection):
	@classmethod
	def getScanRayAndPoint(sclass):
		inputHandlerCtrl = sclass.getInputHandlerCtrl()
		aimingSystemMatrix = inputHandlerCtrl.camera.aimingSystem.matrix
		return aimingSystemMatrix.applyToAxis(2), aimingSystemMatrix.applyToOrigin()

	def setManualInfo(self):
		if self.manualEnabled:
			shotPoint = self.getInputHandlerCtrl().getDesiredShotPoint()
			if shotPoint is not None:
				scanRay, scanPoint = self.getScanRayAndPoint()
				self.manualInfo = (shotPoint - scanPoint).length
		return

	def _getManualDesiredShotPoint(self, shotPoint):
		if self.manualEnabled and shotPoint is not None:
			if self.manualInfo is not None:
				scanRay, scanPoint = self.getScanRayAndPoint()
				return scanPoint + scanRay.scale(self.manualInfo)
		return None

	def _getTargetDesiredShotPoint(self, shotPoint):
		if self.targetEnabled and shotPoint is not None:
			if self.targetInfo is not None and not self.targetInfo.isExpired:
				target = BigWorld.target()
				if target is None or target.id != self.targetInfo:
					scanRay, scanPoint = self.getScanRayAndPoint()
					return scanPoint + scanRay.scale((self.targetInfo.getPosition() - scanPoint).length)
		return None

	def getGunMarkerCollisionPoint(self, start, end):
		distance = None
		scanRay, scanPoint = self.getScanRayAndPoint()
		if self.manualEnabled and self.manualInfo is not None:
			distance = self.manualInfo
		elif self.targetEnabled and self.targetInfo is not None and not self.targetInfo.isExpired:
			distance = scanPoint.distTo(self.targetInfo.getPosition())
		if distance is not None:
			if scanPoint.distSqrTo(start) <= distance * distance <= scanPoint.distSqrTo(end):
				# Scan point is generally far from small segment of collision test.
				# In that case we can consider that vectors from scan point to start and end is parallel.
				# So we can use linear algorithm instead of square one to get some calculation speed.
				baseDistance = scanPoint.distTo(start)
				return start + (end - start).scale((distance - baseDistance) / (scanPoint.distTo(end) - baseDistance))
		return None

class StrategicAimCorrection(BaseAimCorrection):
	@classmethod
	def getScanRayAndPoint(sclass):
		inputHandlerCtrl = sclass.getInputHandlerCtrl()
		aimingSystemMatrix = inputHandlerCtrl.camera.aimingSystem.matrix
		return Math.Vector3(0.0, -1.0, 0.0), aimingSystemMatrix.applyToOrigin()

	def __init__(self, manualEnabled=False, targetEnabled=False, ignoreVehicles=False, heightMultiplier=0.5):
		super(StrategicAimCorrection, self).__init__(manualEnabled, targetEnabled)
		self.ignoreVehicles = ignoreVehicles
		self.heightMultiplier = heightMultiplier
		return

	def setManualInfo(self):
		if self.manualEnabled:
			shotPoint = sclass.getInputHandlerCtrl().getDesiredShotPoint()
			if shotPoint is not None:
				self.manualInfo = shotPoint.y
		return

	def _getManualDesiredShotPoint(self, shotPoint):
		if self.manualEnabled and shotPoint is not None:
			if self.manualInfo is not None:
				result = Math.Vector3(shotPoint)
				result.y = self.manualInfo
				return result
		return None

	def _getTargetDesiredShotPoint(self, shotPoint):
		if self.targetEnabled and shotPoint is not None:
			if self.targetInfo is not None and not self.targetInfo.isExpired:
				target = BigWorld.target()
				if target is None or target.id != self.targetInfo or self.ignoreVehicles:
					return shotPoint + self.targetInfo.getHeightVector().scale(self.heightMultiplier)
		return None

	def _getGroundDesiredShotPoint(self, shotPoint):
		if self.ignoreVehicles and shotPoint is not None:
			scanRay, scanPoint = self.getScanRayAndPoint()
			result = XModLib.CollisionUtils.collideStatic(scanPoint, scanPoint + scanRay.scale(10000.0))
			return result[0] if result is not None else None
		return None

	def getDesiredShotPoint(self, shotPoint):
		return super(StrategicAimCorrection, self).getDesiredShotPoint(self._getGroundDesiredShotPoint(shotPoint) or shotPoint)

	def getGunMarkerCollisionPoint(self, start, end):
		# This is not required in strategic mode - gun marker is always on ground.
		return None
