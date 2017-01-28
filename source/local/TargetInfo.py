# *************************
# TargetInfo Class
# *************************
class TargetInfo(int):
	def __new__(sclass, target, *args, **kwargs):
		return super(TargetInfo, sclass).__new__(sclass, target.id) if XModLib.VehicleInfo.isVehicle(target) else None

	def __init__(self, target, lastLockTime=None, expiryTime=10.0):
		super(TargetInfo, self).__init__(target.id)
		self.lastLockTime = lastLockTime
		self.expiryTime = expiryTime
		self.shortName = XModLib.ArenaInfo.getShortName(target.id)
		self._height = XModLib.VehicleMath.getVehicleHeight(target)
		self._lastHeightVector = XModLib.VehicleMath.getVehicleHeightVector(target, self._height)
		self._lastPosition = target.position
		return

	@property
	def isAutoLocked(self):
		return self.lastLockTime is not None

	@property
	def isExpired(self):
		return self.isAutoLocked and self.lastLockTime + self.expiryTime <= BigWorld.time()

	def getMacroData(self):
		speed = self.getSpeed() or 0.0
		return {
			'shortName': self.shortName,
			'distance': self.getDistance() or 0.0,
			'speedMS': speed,
			'speedMH': speed * 2.24,
			'speedKMH': speed * 3.6
		} if not self.isExpired else None

	def getVehicle(self):
		return BigWorld.entity(self)

	def getSpeed(self):
		vehicle = self.getVehicle()
		return abs(vehicle.filter.speedInfo.value[0]) if vehicle is not None else None

	def getVelocity(self):
		# This method is obsolete and can not longer be used.
		# New vehicle filter does not provide velocity vector value.
		vehicle = self.getVehicle()
		return vehicle.velocity if vehicle is not None else None

	def getPosition(self, actualOnly=False):
		vehicle = self.getVehicle()
		if vehicle is not None:
			self._lastPosition = vehicle.position
			return self._lastPosition
		return self._lastPosition if not actualOnly else None

	def getDistance(self, actualOnly=False):
		position = self.getPosition(actualOnly)
		return position.distTo(BigWorld.player().position) if position is not None else None

	def getHeightVector(self, actualOnly=False):
		vehicle = self.getVehicle()
		if vehicle is not None:
			self._lastHeightVector = XModLib.VehicleMath.getVehicleHeightVector(vehicle, self._height)
			return self._lastHeightVector
		return self._lastHeightVector if not actualOnly else None

	def __repr__(self):
		return 'TargetInfo(target={}, lastLockTime={!r}, expiryTime={!r})'.format(super(TargetInfo, self).__repr__(), self.lastLockTime, self.expiryTime)

	def __del__(self):
		return
