# *************************
# TargetScanner Class
# *************************
class TargetScanMode(tuple):
	__slots__ = ()

	_fields, _defaults = zip(
		('useStandardMode', True),
		('useXRayMode', False),
		('useBBoxMode', False),
		('useBEpsMode', False),
		('maxDistance', 720.0),
		('boundsScalar', 2.5),
		('autoScanInterval', 0.04),
		('autoScanExpiryTimeout', 10.0),
		('autoScanRelockTimeout', 0.16)
	)

	@staticmethod
	def filterID(vehicleID):
		return XModLib.ArenaInfo.isEnemy(vehicleID)

	@staticmethod
	def filterVehicle(vehicle):
		return XModLib.VehicleInfo.isAlive(vehicle)

	def __new__(cls, **kwargs):
		return super(TargetScanMode, cls).__new__(cls, itertools.imap(kwargs.get, cls._fields, cls._defaults))

	def __getattr__(self, name):
		if name not in self._fields:
			raise AttributeError('{!r} object has no attribute {!r}'.format(self.__class__.__name__, name))
		return operator.getitem(self, self._fields.index(name))

	def __repr__(self):
		args = itertools.imap('{!s}={!r}'.format, self._fields, self)
		return '{!s}({!s})'.format(self.__class__.__name__, ', '.join(args))

class TargetScanResultCategory(enum.Enum):
	NOTHING = 'nothing'
	PRIMARY = 'primary'
	SECONDARY = 'secondary'
	AMBIGUOUS = 'ambiguous'

class TargetScanResult(collections.namedtuple('TargetScanResult', ('category', 'target'))):
	__slots__ = ()

	@property
	def isNothing(self):
		return self.category == TargetScanResultCategory.NOTHING

	@property
	def isPrimary(self):
		return self.category == TargetScanResultCategory.PRIMARY

	@property
	def isSecondary(self):
		return self.category == TargetScanResultCategory.SECONDARY

	@property
	def isAmbiguous(self):
		return self.category == TargetScanResultCategory.AMBIGUOUS

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
		if self.isUpdateActive:
			raise RuntimeError('target scan mode could not be changed while scanner is running')
		self._targetScanMode = value
		# Recreate target scanners and callback loop.
		self._initInternalComponents()
		return

	def __init__(self, targetScanMode=TargetScanMode(), autoScanActivated=True):
		super(TargetScanner, self).__init__()
		self._targetScanMode = targetScanMode
		self.autoScanActivated = autoScanActivated
		# Initialize target scanners and callback loop.
		self._initInternalComponents()
		return

	def _initInternalComponents(self):
		self._standardScanner = XModLib.TargetScanners.StandardScanner(
			self._targetScanMode.filterID,
			self._targetScanMode.filterVehicle
		)
		self._xrayScanner = XModLib.TargetScanners.XRayScanner(
			self._targetScanMode.filterID,
			self._targetScanMode.filterVehicle,
			self._targetScanMode.maxDistance
		)
		self._bboxScanner = XModLib.TargetScanners.BBoxScanner(
			self._targetScanMode.filterID,
			self._targetScanMode.filterVehicle,
			self._targetScanMode.maxDistance,
			self._targetScanMode.boundsScalar
		)
		self._bepsScanner = XModLib.TargetScanners.BEllipseScanner(
			self._targetScanMode.filterID,
			self._targetScanMode.filterVehicle,
			self._targetScanMode.maxDistance,
			self._targetScanMode.boundsScalar
		)
		self._updateCallbackLoop = XModLib.CallbackUtils.CallbackLoop(
			self._targetScanMode.autoScanInterval,
			XModLib.CallbackUtils.getMethodProxy(self._updateTargetInfo)
		)
		return

	def _performScanningProcedure(self):
		collidableEntities = XModLib.TargetScanners.getCollidableEntities(
			self._targetScanMode.filterID,
			self._targetScanMode.filterVehicle
		)
		primaryTarget = (
			self._standardScanner.getTarget() if self._targetScanMode.useStandardMode else None
		) or (
			self._xrayScanner.getTarget(collidableEntities) if self._targetScanMode.useXRayMode else None
		)
		secondaryTargets = set(
			self._bboxScanner.getTargets(collidableEntities) if self._targetScanMode.useBBoxMode else []
		) | set(
			self._bepsScanner.getTargets(collidableEntities) if self._targetScanMode.useBEpsMode else []
		) if primaryTarget is None else set([])
		return primaryTarget, secondaryTargets

	def scanTarget(self):
		primaryTarget, secondaryTargets = self._performScanningProcedure()
		if primaryTarget is not None:
			return TargetScanResult(TargetScanResultCategory.PRIMARY, primaryTarget)
		if len(secondaryTargets) == 1:
			return TargetScanResult(TargetScanResultCategory.SECONDARY, secondaryTargets.pop())
		if secondaryTargets:
			return TargetScanResult(TargetScanResultCategory.AMBIGUOUS, None)
		return TargetScanResult(TargetScanResultCategory.NOTHING, None)

	def _updateTargetInfo(self):
		if self.isManualOverrideInEffect or not self.autoScanActivated:
			return
		primaryTarget, secondaryTargets = self._performScanningProcedure()
		if primaryTarget is not None:
			if self.targetInfo is not None and self.targetInfo.isAutoLocked and primaryTarget.id == self.targetInfo:
				self.targetInfo.lastLockTime = BigWorld.time()
			elif self.targetInfo is None or self.targetInfo.isAutoLocked:
				self.targetInfo = TargetInfo(
					primaryTarget,
					lastLockTime=BigWorld.time(),
					expiryTimeout=self._targetScanMode.autoScanExpiryTimeout,
					relockTimeout=self._targetScanMode.autoScanRelockTimeout
				)
		elif len(secondaryTargets) == 1 and (self.targetInfo is None or self.targetInfo.isExpired):
			self.targetInfo = TargetInfo(
				secondaryTargets.pop(),
				lastLockTime=BigWorld.time(),
				expiryTimeout=self._targetScanMode.autoScanExpiryTimeout,
				relockTimeout=self._targetScanMode.autoScanRelockTimeout
			)
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

	def __repr__(self):
		return '{!s}(targetScanMode={!r}, autoScanActivated={!r})'.format(
			self.__class__.__name__,
			self._targetScanMode, self.autoScanActivated
		)

	def __del__(self):
		self._updateCallbackLoop = None
		return
