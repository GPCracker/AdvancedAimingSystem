# *************************
# TargetScanner Class
# *************************
class TargetScanMode(dict):
	__slots__ = ()

	defaults = {
		'useStandardMode': True,
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
	__slots__ = ('__weakref__', 'autoScanActivated', '_targetScanMode', '_standardScanner', '_xrayScanner', '_bboxScanner', '_bepsScanner', '_updateCallbackLoop')

	@property
	def targetInfo(self):
		return getattr(BigWorld.player().inputHandler, 'XTargetInfo', None)

	@targetInfo.setter
	def targetInfo(self, value):
		setattr(BigWorld.player().inputHandler, 'XTargetInfo', value)
		return

	@property
	def targetScanMode(self):
		return self._targetScanMode

	@targetScanMode.setter
	def targetScanMode(self, value):
		self._targetScanMode = value
		self._standardScanner = XModLib.TargetScanners.StandardScanner(
			self._targetScanMode['filterID'],
			self._targetScanMode['filterVehicle']
		)
		self._xrayScanner = XModLib.TargetScanners.XRayScanner(
			self._targetScanMode['filterID'],
			self._targetScanMode['filterVehicle'],
			self._targetScanMode['maxDistance']
		)
		self._bboxScanner = XModLib.TargetScanners.BBoxScanner(
			self._targetScanMode['filterID'],
			self._targetScanMode['filterVehicle'],
			self._targetScanMode['maxDistance'],
			self._targetScanMode['boundsScalar']
		)
		self._bepsScanner = XModLib.TargetScanners.BEllipseScanner(
			self._targetScanMode['filterID'],
			self._targetScanMode['filterVehicle'],
			self._targetScanMode['maxDistance'],
			self._targetScanMode['boundsScalar']
		)
		self._updateCallbackLoop = XModLib.CallbackUtils.CallbackLoop(
			self._targetScanMode['autoScanInterval'],
			XModLib.CallbackUtils.getMethodProxy(self._updateTargetInfo)
		)
		return

	def __init__(self, targetScanMode=TargetScanMode(), autoScanActivated=True):
		super(TargetScanner, self).__init__()
		# Init scanners and callback loop.
		self.targetScanMode = targetScanMode
		self.autoScanActivated = autoScanActivated
		return

	def _performScanningProcedure(self):
		collidableEntities = XModLib.TargetScanners.getCollidableEntities(
			self._targetScanMode['filterID'],
			self._targetScanMode['filterVehicle']
		)
		primaryTarget = (
			self._standardScanner.getTarget() if self._targetScanMode['useStandardMode'] else None
		) or (
			self._xrayScanner.getTarget(collidableEntities) if self._targetScanMode['useXRayMode'] else None
		)
		secondaryTargets = set(
			self._bboxScanner.getTargets(collidableEntities) if self._targetScanMode['useBBoxMode'] else []
		) | set(
			self._bepsScanner.getTargets(collidableEntities) if self._targetScanMode['useBEpsMode'] else []
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
				self.targetInfo = TargetInfo(primaryTarget, BigWorld.time(), self._targetScanMode['autoScanExpiryTime'])
		elif len(secondaryTargets) == 1 and (self.targetInfo is None or self.targetInfo.isExpired):
			self.targetInfo = TargetInfo(secondaryTargets.pop(), BigWorld.time(), self._targetScanMode['autoScanExpiryTime'])
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
