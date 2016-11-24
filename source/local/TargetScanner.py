# *************************
# TargetScanner Class
# *************************
class TargetScanMode(dict):
	defaults = {
		'useNormalMode': True,
		'useXRayMode': False,
		'useBBoxMode': False,
		'useBEpsMode': False,
		'maxDistance': 720.0,
		'boundsScalar': 1.0,
		'autoScanInterval': 0.04,
		'autoScanExpiryTime': 10.0,
		'filterID': None,
		'filterVehicle': lambda vehicle: vehicle.isAlive() and vehicle.publicInfo['team'] is not BigWorld.player().team
	}

	def __init__(self, *args, **kwargs):
		super(TargetScanMode, self).__init__(*args, **kwargs)
		for key in self.defaults:
			self.setdefault(key, self.defaults.get(key))
		return

class TargetScanResult(collections.namedtuple('TargetScanResult', ('result', 'target'))):
	__slots__ = ()

	NOTHING = 'nothing'
	PRIMARY = 'primary'
	SECONDARY = 'secondary'
	AMBIGUOUS = 'ambiguous'

	@property
	def isPrimary(self):
		return self.result == TargetScanResult.PRIMARY

	@property
	def isSecondary(self):
		return self.result == TargetScanResult.SECONDARY

	@property
	def isAmbiguous(self):
		return self.result == TargetScanResult.AMBIGUOUS

class TargetScanner(object):
	@staticmethod
	def _getNormalTarget(filterID=None, filterVehicle=None):
		target = BigWorld.target()
		return target if XModLib.VehicleInfo.VehicleInfo.isVehicle(target) and (filterID is None or filterID(target.id)) and (filterVehicle is None or filterVehicle(target)) else None

	@staticmethod
	def _getXRayTarget(filterID=None, filterVehicle=None, maxDistance=720.0, entities=None):
		return XModLib.XRayScanner.XRayScanner.getTarget(filterID, filterVehicle, maxDistance, entities=entities)

	@staticmethod
	def _getBBoxTargets(filterID=None, filterVehicle=None, maxDistance=720.0, scalar=1.0, entities=None):
		return XModLib.AGScanners.BBoxScanner.getTargets(filterID, filterVehicle, maxDistance, scalar, entities=entities)

	@staticmethod
	def _getBEpsTargets(filterID=None, filterVehicle=None, maxDistance=720.0, scalar=1.0, entities=None):
		return XModLib.AGScanners.BEllipseScanner.getTargets(filterID, filterVehicle, maxDistance, scalar, entities=entities)

	@property
	def targetInfo(self):
		return getattr(BigWorld.player().inputHandler, 'XTargetInfo', None)

	@targetInfo.setter
	def targetInfo(self, value):
		setattr(BigWorld.player().inputHandler, 'XTargetInfo', value)
		return

	def __init__(self, targetScanMode=TargetScanMode(), autoScanActivated=True):
		self.targetScanMode = targetScanMode
		self.autoScanActivated = autoScanActivated
		self._updateCallbackLoop = XModLib.Callback.CallbackLoop(
			self.targetScanMode['autoScanInterval'],
			XModLib.Callback.Callback.getMethodProxy(self._updateTargetInfo)
		)
		return

	def _performScanningProcedure(self):
		visibleVehicles = XModLib.Colliders.Colliders.getVisibleVehicles(
			self.targetScanMode['filterID'],
			self.targetScanMode['filterVehicle'],
			skipPlayer=True
		)
		primaryTarget = (
			self._getNormalTarget(
				self.targetScanMode['filterID'],
				self.targetScanMode['filterVehicle']
			) if self.targetScanMode['useNormalMode'] else None
		) or (
			self._getXRayTarget(
				self.targetScanMode['filterID'],
				self.targetScanMode['filterVehicle'],
				self.targetScanMode['maxDistance'],
				visibleVehicles
			) if self.targetScanMode['useXRayMode'] else None
		)
		secondaryTargets = set(
			self._getBBoxTargets(
				self.targetScanMode['filterID'],
				self.targetScanMode['filterVehicle'],
				self.targetScanMode['maxDistance'],
				self.targetScanMode['boundsScalar'],
				visibleVehicles
			) if self.targetScanMode['useBBoxMode'] else []
		) | set(
			self._getBEpsTargets(
				self.targetScanMode['filterID'],
				self.targetScanMode['filterVehicle'],
				self.targetScanMode['maxDistance'],
				self.targetScanMode['boundsScalar'],
				visibleVehicles
			) if self.targetScanMode['useBEpsMode'] else []
		) if primaryTarget is None else set([])
		return primaryTarget, secondaryTargets

	def scanTarget(self):
		primaryTarget, secondaryTargets = self._performScanningProcedure()
		if primaryTarget is not None:
			return TargetScanResult(TargetScanResult.PRIMARY, primaryTarget)
		if len(secondaryTargets) == 1:
			return TargetScanResult(TargetScanResult.SECONDARY, secondaryTargets.pop())
		if secondaryTargets:
			return TargetScanResult(TargetScanResult.AMBIGUOUS, None)
		return TargetScanResult(TargetScanResult.NOTHING, None)

	def _updateTargetInfo(self):
		if self.isManualOverrideInEffect or not self.autoScanActivated:
			return
		primaryTarget, secondaryTargets = self._performScanningProcedure()
		if primaryTarget is not None:
			if self.targetInfo is not None and self.targetInfo.isAutoLocked and primaryTarget.id == self.targetInfo:
				self.targetInfo.lastLockTime = BigWorld.time()
			elif self.targetInfo is None or self.targetInfo.isAutoLocked:
				self.targetInfo = TargetInfo(primaryTarget, BigWorld.time(), self.targetScanMode['autoScanExpiryTime'])
		elif len(secondaryTargets) == 1 and (self.targetInfo is None or self.targetInfo.isExpired):
			self.targetInfo = TargetInfo(secondaryTargets.pop(), BigWorld.time(), self.targetScanMode['autoScanExpiryTime'])
		elif self.targetInfo is not None and self.targetInfo.isAutoLocked and not self.targetInfo.isExpired and self.targetInfo.getVehicle() in secondaryTargets:
			self.targetInfo.lastLockTime = BigWorld.time()
		return

	def handleVehicleDeath(self, vehicle):
		if vehicle.id == self.targetInfo:
			self.targetInfo = None
		return

	@property
	def isManualOverrideInEffect(self):
		return self.targetInfo is not None and not self.targetInfo.isAutoLocked

	def engageManualOverride(self):
		primaryTarget, secondaryTargets = self._performScanningProcedure()
		if primaryTarget is not None:
			self.targetInfo = TargetInfo(primaryTarget)
		elif len(secondaryTargets) == 1:
			self.targetInfo = TargetInfo(secondaryTargets.pop())
		elif not secondaryTargets:
			self.targetInfo = None
		return

	def disengageManualOverride(self):
		self.targetInfo = None
		return

	@property
	def isUpdateActive(self):
		return self._updateCallbackLoop.isActive

	def start(self, delay=None):
		self._updateCallbackLoop.start(delay)
		return

	def stop(self):
		self._updateCallbackLoop.stop()
		return

	def __del__(self):
		self._updateCallbackLoop = None
		return
