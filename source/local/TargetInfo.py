# ------------------------ #
#    TargetInfo Classes    #
# ------------------------ #
class TargetInfo(int):
	__slots__ = ('__weakref__', 'lastLockTime', 'expiryTimeout', 'relockTimeout', 'shortName', '_height', '_lastHeightVector', '_lastPosition')

	def __new__(cls, target, *args, **kwargs):
		return super(TargetInfo, cls).__new__(cls, target.id) if XModLib.VehicleInfo.isVehicle(target) else None

	def __init__(self, target, lastLockTime=None, expiryTimeout=10.0, relockTimeout=0.16):
		super(TargetInfo, self).__init__(target.id)
		self.lastLockTime = lastLockTime
		self.expiryTimeout = expiryTimeout
		self.relockTimeout = relockTimeout
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
		return self.lastLockTime is not None and self.lastLockTime + self.expiryTimeout <= BigWorld.time()

	@property
	def isInsight(self):
		return self.lastLockTime is None or self.lastLockTime + self.relockTimeout >= BigWorld.time()

	def getMacroData(self):
		speed = self.getSpeed() or 0.0
		return {
			'insight': self.isInsight,
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
		return '{!s}(target=BigWorld.entity({!s}), lastLockTime={!r}, expiryTimeout={!r}, relockTimeout={!r})'.format(
			self.__class__.__name__,
			int.__repr__(self), self.lastLockTime, self.expiryTimeout, self.relockTimeout
		)

	def __del__(self):
		return
