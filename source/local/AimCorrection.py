# *************************
# AimCorrection Class
# *************************
class BaseAimCorrection(object):
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

	def __del__(self):
		return

class ArcadeAimCorrection(BaseAimCorrection):
	def setManualInfo(self):
		if self.manualEnabled:
			self.manualInfo = None
		return

	def _getManualDesiredShotPoint(self, shotPoint):
		if self.manualEnabled and shotPoint is not None:
			if self.manualInfo is not None:
				pass
		return None

	def _getTargetDesiredShotPoint(self, shotPoint):
		if self.targetEnabled and shotPoint is not None:
			if self.targetInfo is not None and not self.targetInfo.isExpired:
				pass
		return None

class SniperAimCorrection(BaseAimCorrection):
	def setManualInfo(self):
		if self.manualEnabled:
			shotPoint = BigWorld.player().inputHandler.ctrl.getDesiredShotPoint()
			if shotPoint is not None:
				cameraRay, cameraPoint = AvatarInputHandler.cameras.getWorldRayAndPoint(*BigWorld.player().inputHandler.ctrl._aimOffset)
				self.manualInfo = (shotPoint - cameraPoint).length
		return

	def _getManualDesiredShotPoint(self, shotPoint):
		if self.manualEnabled and shotPoint is not None:
			if self.manualInfo is not None:
				cameraRay, cameraPoint = AvatarInputHandler.cameras.getWorldRayAndPoint(*BigWorld.player().inputHandler.ctrl._aimOffset)
				cameraRay.normalise()
				return cameraPoint + cameraRay.scale(self.manualInfo)
		return None

	def _getTargetDesiredShotPoint(self, shotPoint):
		if self.targetEnabled and shotPoint is not None:
			if self.targetInfo is not None and not self.targetInfo.isExpired:
				target = BigWorld.target()
				if target is None or target.id != self.targetInfo:
					cameraRay, cameraPoint = AvatarInputHandler.cameras.getWorldRayAndPoint(*BigWorld.player().inputHandler.ctrl._aimOffset)
					cameraRay.normalise()
					return cameraPoint + cameraRay.scale((self.targetInfo.getPosition() - cameraPoint).length)
		return None

class StrategicAimCorrection(BaseAimCorrection):
	def __init__(self, manualEnabled=False, targetEnabled=False, ignoreVehicles=False, heightMultiplier=0.5):
		super(StrategicAimCorrection, self).__init__(manualEnabled, targetEnabled)
		self.ignoreVehicles = ignoreVehicles
		self.heightMultiplier = heightMultiplier
		return

	def setManualInfo(self):
		if self.manualEnabled:
			shotPoint = BigWorld.player().inputHandler.ctrl.getDesiredShotPoint()
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
			cameraRay, cameraPoint = AvatarInputHandler.cameras.getWorldRayAndPoint(*BigWorld.player().inputHandler.ctrl._aimOffset)
			result = XModLib.Colliders.Colliders.collideStatic(cameraPoint, cameraPoint + cameraRay.scale(10000.0))
			return result[0] if result is not None else None
		return None

	def getDesiredShotPoint(self, shotPoint):
		return super(StrategicAimCorrection, self).getDesiredShotPoint(self._getGroundDesiredShotPoint(shotPoint) or shotPoint)
