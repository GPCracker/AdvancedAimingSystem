# ------------ #
#    Python    #
# ------------ #
import weakref
import operator
import collections

# -------------- #
#    BigWorld    #
# -------------- #
import BigWorld

# ---------------- #
#    WoT Client    #
# ---------------- #
# nothing

# ---------------------- #
#    WoT Client Hooks    #
# ---------------------- #
import Avatar
import Vehicle

# ------------------- #
#    X-Mod Library    #
# ------------------- #
import XModLib.HookUtils
import XModLib.VehicleInfo

# ----------------------------------- #
#    Plug-in default configuration    #
# ----------------------------------- #
g_globals['appDefaultConfig']['plugins']['expertPerk'] = {
	'enabled': ('Bool', False),
	'cacheExtrasInfo': ('Bool', False),
	'cacheExpiryTimeout': ('Float', 30.0),
	'responseTimeout': ('Float', 5.0)
}

# ----------------------------------------- #
#    Plug-in configuration reading stage    #
# ----------------------------------------- #
g_config['plugins']['expertPerk'] = g_globals['appConfigReader'](
	XModLib.XMLConfigReader.overrideOpenSubSection(g_globals['appConfigFile'], 'plugins/expertPerk'),
	g_globals['appDefaultConfig']['plugins']['expertPerk']
)

# ------------------------------------ #
#    Plug-in hooks injection events    #
# ------------------------------------ #
p_inject_hooks = XModLib.HookUtils.HookEvent()
p_inject_ovrds = XModLib.HookUtils.HookEvent()

# ------------------------ #
#    Plug-in init stage    #
# ------------------------ #
if g_config['applicationEnabled'] and g_config['plugins']['expertPerk']['enabled']:
	p_inject_stage_main += p_inject_hooks
	p_inject_stage_init += p_inject_ovrds

# ------------------------ #
#    ExpertPerk Classes    #
# ------------------------ #
class ExtrasInfoEntry(collections.namedtuple('ExtrasInfoEntry', ('criticalExtras', 'destroyedExtras'))):
	__slots__ = ()

	def __new__(cls, criticalExtras=(), destroyedExtras=()):
		return super(ExtrasInfoEntry, cls).__new__(cls, criticalExtras, destroyedExtras)

class ExtrasInfoCacheEntry(collections.namedtuple('ExtrasInfoCacheEntry', ('extrasInfoEntry', 'receiptTime', 'expiryTimeout'))):
	__slots__ = ()

	def __new__(cls, extrasInfoEntry, receiptTime=None, expiryTimeout=30.0):
		if receiptTime is None:
			receiptTime = BigWorld.time()
		return super(ExtrasInfoCacheEntry, cls).__new__(cls, extrasInfoEntry, receiptTime, expiryTimeout)

	@property
	def isExpired(self):
		return self.receiptTime + self.expiryTimeout <= BigWorld.time()

class ExtrasInfoCache(dict):
	__slots__ = ()

	def cleanup(self):
		vehicleIDs = tuple(vehicleID for vehicleID, cacheEntry in self.viewitems() if cacheEntry.isExpired)
		return tuple((vehicleID, self.pop(vehicleID)) for vehicleID in vehicleIDs)

class ExtrasInfoRequest(collections.namedtuple('ExtrasInfoRequest', ('vehicleID', 'requestTime', 'responseTimeout'))):
	__slots__ = ()

	def __new__(cls, vehicleID, requestTime=None, responseTimeout=5.0):
		if requestTime is None:
			requestTime = BigWorld.time()
		return super(ExtrasInfoRequest, cls).__new__(cls, vehicleID, requestTime, responseTimeout)

	@property
	def isExpired(self):
		return self.requestTime + self.responseTimeout <= BigWorld.time()

class ExtrasInfoResponse(collections.namedtuple('ExtrasInfoResponse', ('vehicleID', 'extrasInfoEntry', 'responseTime'))):
	__slots__ = ()

	def __new__(cls, vehicleID, extrasInfoEntry, responseTime=None):
		if responseTime is None:
			responseTime = BigWorld.time()
		return super(ExtrasInfoResponse, cls).__new__(cls, vehicleID, extrasInfoEntry, responseTime)

class ExtrasInfoRequester(object):
	__slots__ = ('__weakref__', '_avatar', '_activeRequest', '_lastResponse')

	def __init__(self, avatar):
		super(ExtrasInfoRequester, self).__init__()
		self._avatar = weakref.proxy(avatar)
		self._activeRequest = None
		self._lastResponse = None
		return

	@property
	def _maySeeOtherVehicleDamagedDevices(self):
		return self._avatar._maySeeOtherVehicleDamagedDevices

	@property
	def isRequested(self):
		return self._activeRequest is not None

	@property
	def isExpired(self):
		return self._activeRequest is not None and self._activeRequest.isExpired

	@property
	def isResponded(self):
		result = self._activeRequest is not None and self._lastResponse is not None
		result = result and self._activeRequest.vehicleID == self._lastResponse.vehicleID
		return result and self._activeRequest.requestTime <= self._lastResponse.responseTime

	@property
	def lastResponse(self):
		return self._lastResponse

	@property
	def activeRequest(self):
		return self._activeRequest

	@activeRequest.setter
	def activeRequest(self, value):
		if self._maySeeOtherVehicleDamagedDevices:
			if self._activeRequest.vehicleID != value.vehicleID:
				# Monitoring is actually activated only four seconds after sending request.
				# Monitoring means that we immediately receive all updates about vehicle modules.
				# After monitoring is successfully activated, we also receive initial data to show.
				# Monitoring could be maintained only if player's target is in direct visibility area.
				# So for most effective usage we should cancel request only when player changes his target.
				# Server may not respond if target has no critical or destroyed extras or is invisible for player.
				# This situations should be ignored, because server will keep us posted anyway when data will be available.
				if self._activeRequest is not None:
					self._avatar.cell.monitorVehicleDamagedDevices(0)
				self._activeRequest = value
				if self._activeRequest is not None:
					self._avatar.cell.monitorVehicleDamagedDevices(self._activeRequest.vehicleID)
		return

	def onExtrasInfoReceived(self, extrasInfoResponse):
		self._lastResponse = extrasInfoResponse
		return

	def __del__(self):
		if self._activeRequest is not None:
			raise RuntimeError('ExtrasInfoRequester is about to be removed with an active request')
		return

class ExtrasInfoController(object):
	__slots__ = ('__weakref__', '_cache', '_requester', '_cacheExtrasInfo', '_cacheExpiryTimeout', '_responseTimeout')

	def __init__(self, avatar, cacheExtrasInfo=False, cacheExpiryTimeout=30.0, responseTimeout=5.0):
		super(ExtrasInfoController, self).__init__()
		self._cache = ExtrasInfoCache()
		self._requester = ExtrasInfoRequester(avatar)
		self._cacheExtrasInfo = cacheExtrasInfo
		self._cacheExpiryTimeout = cacheExpiryTimeout
		self._responseTimeout = responseTimeout
		return

	cacheExtrasInfo = property(operator.attrgetter('_cacheExtrasInfo'))

	def isMonitored(self, vehicleID):
		return self._requester.isResponded and self._requester.activeRequest.vehicleID == vehicleID

	@property
	def activeRequestVehicleID(self):
		return self._requester.activeRequest.vehicleID if self._requester.activeRequest is not None else 0

	@activeRequestVehicleID.setter
	def activeRequestVehicleID(self, value):
		self._requester.activeRequest = ExtrasInfoRequest(value, responseTimeout=self._responseTimeout) if value != 0 else None
		return

	def cancelExtrasInfoRequest(self, vehicleID=None):
		if vehicleID is None or self.activeRequestVehicleID == vehicleID:
			self.activeRequestVehicleID = 0
		return

	def getCachedExtrasInfoEntry(self, vehicleID):
		# Cache provides access to information about modules of vehicles that were monitored before.
		# Cache entries lifetime may expire, but they are still considered actual if target is being monitored now.
		# Monitored vehicle means that active request is related to requested vehicle and has already been replied.
		# For correct operating when caching is disabled we return data about actually monitored vehicles, but only about them.
		cacheEntry = self._cache.get(vehicleID, None)
		if cacheEntry is not None and (self._cacheExtrasInfo and not cacheEntry.isExpired or self.isMonitored(vehicleID)):
			return cacheEntry.extrasInfoEntry
		return None

	def onExtrasInfoReceived(self, vehicleID, criticalExtras, destroyedExtras):
		extrasInfoEntry = ExtrasInfoEntry(criticalExtras, destroyedExtras)
		self._requester.onExtrasInfoReceived(ExtrasInfoResponse(vehicleID, extrasInfoEntry))
		self._cache[vehicleID] = ExtrasInfoCacheEntry(extrasInfoEntry, expiryTimeout=self._cacheExpiryTimeout)
		return

	def __del__(self):
		if self._requester.activeRequest is not None:
			raise RuntimeError('ExtrasInfoController is about to be removed with an active request')
		return

# ------------------------ #
#    PlayerAvatar Hooks    #
# ------------------------ #
@XModLib.HookUtils.methodHookExt(p_inject_hooks, Avatar.PlayerAvatar, '__init__')
def new_PlayerAvatar_init(self, *args, **kwargs):
	config = g_config['plugins']['expertPerk']
	self.XExtrasInfoController = ExtrasInfoController(
		self,
		cacheExtrasInfo=config['cacheExtrasInfo'],
		cacheExpiryTimeout=config['cacheExpiryTimeout'],
		responseTimeout=config['responseTimeout']
	) if config['enabled'] else None
	return

@XModLib.HookUtils.methodHookExt(p_inject_hooks, Avatar.PlayerAvatar, 'showOtherVehicleDamagedDevices')
def new_PlayerAvatar_showOtherVehicleDamagedDevices(self, vehicleID, damagedExtras, destroyedExtras):
	extrasInfoController = getattr(self, 'XExtrasInfoController', None)
	if extrasInfoController is not None and getattr(self, '_maySeeOtherVehicleDamagedDevices', False):
		extrasInfoController.onExtrasInfoReceived(vehicleID, damagedExtras, destroyedExtras)
		# This code is executed when server sends data and advanced expert handler is activated.
		# First action we should do here is to cache data received from server for use in future.
		# Target scanner is useless here because expert works only on vehicles in direct visibility area.
		# If received data is about current target, and it is alive, we should show this information to player at once.
		target = BigWorld.target()
		if XModLib.VehicleInfo.isVehicle(target) and target.isAlive() and target.id == vehicleID:
			self.guiSessionProvider.shared.feedback.showVehicleDamagedDevices(vehicleID, damagedExtras, destroyedExtras)
	return

@XModLib.HookUtils.methodHookExt(p_inject_hooks, Avatar.PlayerAvatar, 'targetBlur')
def new_PlayerAvatar_targetBlur(self, prevEntity):
	extrasInfoController = getattr(self, 'XExtrasInfoController', None)
	if extrasInfoController is not None and getattr(self, '_maySeeOtherVehicleDamagedDevices', False):
		# Default handler cancels expert request here, forcing player to hold crosshairs over target for some time.
		# We moved this code to vehicle visual stop handler, so request will be cancelled only when target disappears.
		# Also request is automatically cancelled before new request is sent or when target dies (all modules break).
		# Code below just hides expert information panel because data is useless when no target is specified.
		if XModLib.VehicleInfo.isVehicle(prevEntity) and prevEntity.isAlive():
			self.guiSessionProvider.shared.feedback.hideVehicleDamagedDevices()
	return

@XModLib.HookUtils.methodHookExt(p_inject_hooks, Avatar.PlayerAvatar, 'targetFocus')
def new_PlayerAvatar_targetFocus(self, entity):
	extrasInfoController = getattr(self, 'XExtrasInfoController', None)
	if extrasInfoController is not None and getattr(self, '_maySeeOtherVehicleDamagedDevices', False):
		# Like default handler does, we send a request if focused target is an alive vehicle.
		# Unless request is cancelled, actual data will be shown just after client receives it.
		# But for now we check if we have actual cached data that will be displayed until the server sends an update.
		if XModLib.VehicleInfo.isVehicle(entity) and entity.isAlive():
			extrasInfoController.activeRequestVehicleID = entity.id
			extrasInfoEntry = extrasInfoController.getCachedExtrasInfoEntry(entity.id)
			if extrasInfoEntry is not None:
				self.guiSessionProvider.shared.feedback.showVehicleDamagedDevices(entity.id, *extrasInfoEntry)
	return

@XModLib.HookUtils.propertyHookExt(p_inject_hooks, Avatar.PlayerAvatar, '_PlayerAvatar__maySeeOtherVehicleDamagedDevices', XModLib.HookUtils.PropertyAction.GET, '_maySeeOtherVehicleDamagedDevices', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_PlayerAvatar_maySeeOtherVehicleDamagedDevices_getter(old_PlayerAvatar_maySeeOtherVehicleDamagedDevices_getter, self):
	return old_PlayerAvatar_maySeeOtherVehicleDamagedDevices_getter(self) and getattr(self, 'XExtrasInfoController', None) is None

# ------------------- #
#    Vehicle Hooks    #
# ------------------- #
@XModLib.HookUtils.methodHookExt(p_inject_hooks, Vehicle.Vehicle, 'stopVisual', invoke=XModLib.HookUtils.HookInvoke.PRIMARY)
def new_Vehicle_stopVisual(self, *args, **kwargs):
	# When vehicle disappears we should cancel an active request related to it.
	extrasInfoController = getattr(BigWorld.player(), 'XExtrasInfoController', None)
	if extrasInfoController is not None:
		extrasInfoController.cancelExtrasInfoRequest(self.id)
	return

@XModLib.HookUtils.methodHookExt(p_inject_hooks, Vehicle.Vehicle, '_Vehicle__onVehicleDeath')
def new_Vehicle_onVehicleDeath(self, isDeadStarted=False):
	# This method is also called when dead target appears (player enters its drawing area).
	if isDeadStarted:
		return
	# When vehicle dies we should cancel an active request related to it.
	extrasInfoController = getattr(BigWorld.player(), 'XExtrasInfoController', None)
	if extrasInfoController is not None:
		extrasInfoController.cancelExtrasInfoRequest(self.id)
	return
