# *************************
# ExpertPerk Class
# *************************
class ExpertRequest(object):
	def __init__(self, vehicleID, time=None):
		self.vehicleID = vehicleID
		self.time = time if time is not None else BigWorld.time()
		BigWorld.player().cell.monitorVehicleDamagedDevices(vehicleID)
		return

	def __del__(self):
		BigWorld.player().cell.monitorVehicleDamagedDevices(0)
		return

class ExpertPerk(object):
	def __init__(self, statusFunction, cacheExtrasInfo=False, enableQueue=False, replyTimeout=5.0, requestDelay=5.0):
		self.statusFunction = statusFunction
		self.cacheExtrasInfo = cacheExtrasInfo
		self.enableQueue = enableQueue
		self.replyTimeout = replyTimeout
		self.requestDelay = requestDelay
		self.cache = dict()
		self.queue = XModLib.Helpers.Queue()
		self.activeRequest = None
		self.callback = None
		self.updateCallback()
		return

	@property
	def status(self):
		return self.statusFunction() if self.statusFunction is not None else False

	def request(self, vehicleID):
		entity = BigWorld.entity(vehicleID)
		if self.status and XModLib.VehicleInfo.VehicleInfo.isVehicle(entity):
			if self.activeRequest is None or self.activeRequest.vehicleID != vehicleID:
				self.activeRequest = ExpertRequest(vehicleID)
				self.updateCallback()
		return

	def cancel(self, vehicleID=None):
		if self.activeRequest is not None and (vehicleID is None or self.activeRequest.vehicleID == vehicleID):
			self.activeRequest = None
			self.updateCallback()
		return

	def enqueue(self, vehicleID, priority=False):
		if vehicleID in self.queue:
			self.queue.cancel(vehicleID)
		if vehicleID not in self.queue:
			if priority:
				self.queue.insert(0, vehicleID)
			else:
				self.queue.append(vehicleID)
		return

	def discard(self, vehicleID):
		if vehicleID in self.queue:
			self.queue.cancel(vehicleID)
		return

	def onExtrasInfoReceived(self, vehicleID, damagedExtras, destroyedExtras):
		if self.cacheExtrasInfo and XModLib.ArenaInfo.ArenaInfo.isAlive(vehicleID):
			self.cache[vehicleID] = (damagedExtras, destroyedExtras)
		self.discard(vehicleID)
		self.cancel(vehicleID)
		return

	def replyCallback(self, vehicleID):
		if self.activeRequest is not None and self.activeRequest.vehicleID == vehicleID and self.activeRequest.time + self.replyTimeout <= BigWorld.time() + 0.5:
			self.cancel(vehicleID)
		return

	def requestCallback(self):
		if self.activeRequest is None:
			vehicle = None
			while vehicle is None and self.queue:
				vehicle = BigWorld.entity(self.queue.dequeue())
				vehicle = vehicle if XModLib.VehicleInfo.VehicleInfo.isVehicle(vehicle) and vehicle.isAlive() else None
			if vehicle is not None:
				self.request(vehicle.id)
			else:
				self.updateCallback()
		return

	def updateCallback(self):
		if self.activeRequest is not None:
			self.callback = XModLib.Callback.Callback(self.replyTimeout, XModLib.Callback.Callback.getMethodProxy(self.replyCallback, self.activeRequest.vehicleID))
		else:
			self.callback = XModLib.Callback.Callback(self.requestDelay, XModLib.Callback.Callback.getMethodProxy(self.requestCallback))
		return

	def __del__(self):
		return
