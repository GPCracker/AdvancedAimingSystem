# *************************
# ExpertPerk Class
# *************************
class ExpertRequest(int):
	def __new__(sclass, vehicleID, *args, **kwargs):
		return super(ExpertRequest, sclass).__new__(sclass, vehicleID)

	def __init__(self, vehicleID, replyTimeout=5.0):
		super(ExpertRequest, self).__init__(vehicleID)
		self.replyTimeout = replyTimeout
		self._requestTime = None
		self._cancelTime = None
		self._replyTime = None
		return

	@property
	def isRequested(self):
		return self._requestTime is not None

	@property
	def isCancelled(self):
		return self._cancelTime is not None

	@property
	def isReplied(self):
		return self._replyTime is not None

	@property
	def isActive(self):
		return self.isRequested and not self.isCancelled

	@property
	def isExpired(self):
		return self.isCancelled or self.isReplied or not self.isRequested or self._requestTime + self.replyTimeout <= BigWorld.time()

	def request(self, requestTime=None):
		if self.isRequested:
			raise RuntimeError('Request is already done.')
		self._requestTime = requestTime if requestTime is not None else BigWorld.time()
		BigWorld.player().cell.monitorVehicleDamagedDevices(self)
		return

	def cancel(self, cancelTime=None):
		if not self.isRequested:
			raise RuntimeError('Request is not done yet.')
		if self.isCancelled:
			raise RuntimeError('Request is already cancelled.')
		self._cancelTime = cancelTime if cancelTime is not None else BigWorld.time()
		BigWorld.player().cell.monitorVehicleDamagedDevices(0)
		return

	def markReplied(self, replyTime=None):
		self._replyTime = replyTime if replyTime is not None else BigWorld.time()
		return

	def __repr__(self):
		return 'ExpertRequest(vehicleID={}, replyTimeout={!r})'.format(super(ExpertRequest, self).__repr__(), self.replyTimeout)

	def __del__(self):
		if self.isActive:
			raise RuntimeError('Request is about to be removed in active state.')
		return

class ExtrasInfoCacheEntry(tuple):
	def __new__(sclass, extrasInfo, *args, **kwargs):
		return super(ExtrasInfoCacheEntry, sclass).__new__(sclass, extrasInfo)

	def __init__(self, extrasInfo, receiptTime=None, expiryTime=60.0):
		super(ExtrasInfoCacheEntry, self).__init__(extrasInfo)
		self.receiptTime = receiptTime if receiptTime is not None else BigWorld.time()
		self.expiryTime = expiryTime
		return

	@property
	def isExpired(self):
		return self.receiptTime + self.expiryTime <= BigWorld.time()

	def __repr__(self):
		return 'ExtrasInfoCacheEntry(extrasInfo={}, receiptTime={!r}, expiryTime={!r})'.format(
			super(ExtrasInfoCacheEntry, self).__repr__(),
			self.receiptTime,
			self.expiryTime
		)

class ExtrasInfoCache(dict):
	pass

class ExpertPerk(object):
	def __init__(self, statusFunction=None, cacheExtrasInfo=False, replyTimeout=5.0, cacheExpiryTime=60.0):
		self.statusFunction = statusFunction
		self.cacheExtrasInfo = cacheExtrasInfo
		self.replyTimeout = replyTimeout
		self.cacheExpiryTime = cacheExpiryTime
		self.extrasInfoCache = ExtrasInfoCache()
		self._activeRequest = None
		return

	def _getStatus(self):
		return self.statusFunction() if self.statusFunction is not None else False

	@property
	def activeRequest(self):
		return self._activeRequest

	@activeRequest.setter
	def activeRequest(self, request):
		if self._activeRequest is not None and self._activeRequest.isActive:
			self._activeRequest.cancel()
		self._activeRequest = request
		if self._activeRequest is not None and not self._activeRequest.isActive:
			self._activeRequest.request()
		return

	def request(self, vehicleID):
		# Entity must be alive vehicle
		if self._getStatus() and (vehicleID != self.activeRequest or self.activeRequest.isExpired):
			self.activeRequest = ExpertRequest(vehicleID, replyTimeout=self.replyTimeout)
		return

	def cancel(self, vehicleID=None):
		if vehicleID is None or vehicleID == self.activeRequest:
			self.activeRequest = None
		return

	def onExtrasInfoReceived(self, vehicleID, extrasInfo):
		if self.cacheExtrasInfo:
			self.extrasInfoCache[vehicleID] = ExtrasInfoCacheEntry(extrasInfo, expiryTime=self.cacheExpiryTime)
		if vehicleID == self.activeRequest:
			self.activeRequest.markReplied()
		return

	def __del__(self):
		self.activeRequest = None
		return
