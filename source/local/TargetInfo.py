# *************************
# TargetInfo Class
# *************************
class TargetInfo(object):
	def __init__(self, target, lockTime = None):
		assert XModLib.VehicleInfo.VehicleInfo.isVehicle(target)
		self.id = target.id
		self.lockTime = lockTime
		self.physics = target.typeDescriptor.physics
		self.shortName = XModLib.ArenaInfo.ArenaInfo.getShortName(target.id)
		self.__position = target.position
		self.__heightVector = XModLib.VehicleMath.VehicleMath.getVehicleHeightVector(target)
		return

	@property
	def isAutoLocked(self):
		return self.lockTime is not None

	@property
	def isVisible(self):
		return XModLib.VehicleInfo.VehicleInfo.isVisible(self.id)

	@property
	def speed(self):
		vehicle = BigWorld.entity(self.id)
		if vehicle is not None:
			return abs(vehicle.filter.speedInfo.value[0])#2
		return None

	@property
	def velocity(self):
		vehicle = BigWorld.entity(self.id)
		if vehicle is not None:
			return vehicle.velocity
		return None

	@property
	def position(self):
		vehicle = BigWorld.entity(self.id)
		if vehicle is not None:
			self.__position = vehicle.position
		return self.__position

	@property
	def savedPosition(self):
		return self.__position

	@property
	def heightVector(self):
		vehicle = BigWorld.entity(self.id)
		if vehicle is not None:
			self.__heightVector = XModLib.VehicleMath.VehicleMath.getVehicleHeightVector(vehicle)
		return self.__heightVector

	@property
	def savedHeightVector(self):
		return self.__heightVector

	def __del__(self):
		return
