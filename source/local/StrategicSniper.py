# *************************
# StrategicSniper Class
# *************************
class StrategicSniper(object):
	def __init__(self, isSniperMode=False, correctMaxDistance=False, criticalDistance=32.0, cameraPitchLimits=(0.05, 1.57), cameraBasePitch=0.0, cameraBasePitchLimits=(-0.50, 0.50), cameraBasePitchDelta=0.05, cameraControlPlaneLevel=-150.0):
		self.isSniperMode = isSniperMode
		self.correctMaxDistance = correctMaxDistance
		self.criticalDistance = criticalDistance
		self.cameraPitchLimits = cameraPitchLimits
		self.cameraBasePitch = cameraBasePitch
		self.cameraBasePitchLimits = cameraBasePitchLimits
		self.cameraBasePitchDelta = cameraBasePitchDelta
		self.cameraSourceDYMatrix = Math.Matrix()
		self.cameraSourceIPMatrix = Math.Matrix()
		self.cameraSourceDMP = Math.MatrixProduct()
		self.cameraSourceDMP.a =  Math.MatrixInverse(self.cameraSourceIPMatrix)
		self.cameraSourceDMP.b = self.cameraSourceDYMatrix
		self.spaceBoundingBox = XModLib.Geometry.BoundingBox.getSpaceBoundingBox()
		self.arenaBoundingBox = XModLib.Geometry.BoundingBox.getArenaBoundingBox()
		self.cameraControlPlane = XModLib.Geometry.Plane(Math.Vector3(0.0, cameraControlPlaneLevel, 0.0), Math.Vector3(0.0, 1.0, 0.0))
		self.cameraControlPosition = None
		return

	def getCameraShift(self, shiftVector):
		return self.cameraSourceDYMatrix.applyVector(shiftVector)

	def getCameraPivotPosition(self, aimingSystemHeight, cameraDistance):
		return (-self.cameraSourceIPMatrix.applyToAxis(2)).scale(aimingSystemHeight + cameraDistance) - Math.Vector3(0.0, aimingSystemHeight, 0.0)

	def updateCameraYaw(self, yaw):
		self.cameraSourceDYMatrix.setRotateYPR((yaw, 0.0, 0.0))
		return

	def updateCameraPitch(self, pitch):
		pitch = min(max(pitch + self.cameraBasePitch, self.cameraPitchLimits[0]), self.cameraPitchLimits[1])
		self.cameraSourceIPMatrix.setRotateYPR((0.0, pitch, 0.0))
		return

	def setCameraBasePitch(self, pitch):
		pitch = min(max(pitch, self.cameraBasePitchLimits[0]), self.cameraBasePitchLimits[1])
		result = pitch, pitch - self.cameraBasePitch
		self.cameraBasePitch = pitch
		return result

	def increaseCameraBasePitch(self):
		return self.setCameraBasePitch(self.cameraBasePitch + self.cameraBasePitchDelta)

	def decreaseCameraBasePitch(self):
		return self.setCameraBasePitch(self.cameraBasePitch - self.cameraBasePitchDelta)

	def computeLPbyMP(self, mapPoint):
		scanResult = XModLib.Colliders.Colliders.collideStatic(
			Math.Vector3(mapPoint.x, 1000.0, mapPoint.z),
			Math.Vector3(mapPoint.x, -250.0, mapPoint.z)
		)
		return (scanResult[0], None, scanResult) if scanResult is not None else None

	def computeLPbyCP(self, cameraControlPosition, externalColliders = []):
		vehicleTypeDescriptor = BigWorld.player().vehicleTypeDescriptor
		vehicleMP = BigWorld.player().getOwnVehicleMatrix()
		turretYaw, gunPitch = XModLib.VehicleMath.VehicleMath.getShotAngles(vehicleTypeDescriptor, vehicleMP, cameraControlPosition)
		return XModLib.Colliders.Colliders.computeProjectileTrajectoryEnd(
			vehicleTypeDescriptor,
			Math.Matrix(vehicleMP),
			turretYaw,
			gunPitch,
			externalColliders + [
				XModLib.Colliders.Colliders.collideStatic,
				functools.partial(XModLib.Colliders.Colliders.collideGeometry, self.spaceBoundingBox.intersectSegment)
			]
		)

	def computeCPbyLP(self, landPoint, externalColliders = []):
		vehicleTypeDescriptor = BigWorld.player().vehicleTypeDescriptor
		vehicleMP = BigWorld.player().getOwnVehicleMatrix()
		turretYaw, gunPitch = XModLib.VehicleMath.VehicleMath.getShotAngles(vehicleTypeDescriptor, vehicleMP, landPoint)
		return XModLib.Colliders.Colliders.computeProjectileTrajectoryEnd(
			vehicleTypeDescriptor,
			Math.Matrix(vehicleMP),
			turretYaw,
			gunPitch,
			externalColliders + [
				functools.partial(XModLib.Colliders.Colliders.collideGeometry, self.cameraControlPlane.intersectSegment)
			]
		)

	def __del__(self):
		return
