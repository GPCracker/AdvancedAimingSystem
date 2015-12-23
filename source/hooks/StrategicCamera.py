# *************************
# StrategicCamera Hooks
# *************************
@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.DynamicCameras.StrategicCamera.StrategicCamera, 'enable')
def new_StrategicCamera_enable(self, *args, **kwargs):
	if BigWorld.player().inputHandler.ctrlModeName != 'strategic':
		return
	config0 = _config_['strategicAS']['strategicSniper']
	if config0['enabled'] and (not hasattr(self.aimingSystem, 'XStrategicSniper') or self.aimingSystem.XStrategicSniper is None):
		self.aimingSystem.XStrategicSniper = StrategicSniper(
			isSniperMode=False,
			correctMaxDistance=config0['correctMaxDistance'],
			criticalDistance=32.0,
			cameraPitchLimits=(0.05, 1.57),
			cameraBasePitch=config0['basePitch']['value'],
			cameraBasePitchLimits=(-0.50, 0.50),
			cameraBasePitchDelta=config0['basePitch']['adjustment']['delta'],
			cameraControlPlaneLevel=config0['controlLevel']
		)
	if hasattr(self.aimingSystem, 'XStrategicSniper') and self.aimingSystem.XStrategicSniper is not None:
		config0['activated'] = False
		self.aimingSystem.XStrategicSniper.isSniperMode = False
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.DynamicCameras.StrategicCamera.StrategicCamera, 'disable', XModLib.HookUtils.HookFunction.CALL_HOOK_BEFORE_ORIGIN)
def new_StrategicCamera_disable(self, *args, **kwargs):
	if BigWorld.player().inputHandler.ctrlModeName != 'strategic':
		return
	config0 = _config_['strategicAS']['strategicSniper']
	if hasattr(self.aimingSystem, 'XStrategicSniper') and self.aimingSystem.XStrategicSniper is not None:
		config0['activated'] = False
		self.aimingSystem.XStrategicSniper.isSniperMode = False
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.DynamicCameras.StrategicCamera.StrategicCamera, '_StrategicCamera__cameraUpdate')
def new_StrategicCamera_cameraUpdate(self):
	if BigWorld.player().inputHandler.ctrlModeName != 'strategic':
		return
	if hasattr(self.aimingSystem, 'XStrategicSniper') and self.aimingSystem.XStrategicSniper is not None:
		if self.aimingSystem.XStrategicSniper.isSniperMode:
			self.camera.source = self.aimingSystem.XStrategicSniper.cameraSourceDMP
			self.camera.pivotPosition = self.aimingSystem.XStrategicSniper.getCameraPivotPosition(self.aimingSystem.height, self._StrategicCamera__camDist)
		else:
			import math
			self.camera.source = XModLib.ExtraMath.ExtraMath.rotationMatrix(0, -math.pi * 0.499, 0)
	return

def new_StrategicCamera_XSwitchMode(self, isSniperMode=False, shotPoint=None):
	if BigWorld.player().inputHandler.ctrlModeName != 'strategic':
		return
	if shotPoint is None:
		shotPoint = self.aimingSystem.getDesiredShotPoint()
	if shotPoint is not None and hasattr(self.aimingSystem, 'XStrategicSniper') and self.aimingSystem.XStrategicSniper is not None:
		self.aimingSystem.XStrategicSniper.isSniperMode = isSniperMode
		self.aimingSystem.updateTargetPos(shotPoint)
		## Minimap Strategic Cell
		minimapStrategicCellMP = BigWorld.camera().invViewMatrix
		if isSniperMode:
			minimapStrategicCellMP = Math.WGCombinedMP()
			minimapStrategicCellMP.translationSrc = self.aimingSystem.matrix
			minimapStrategicCellMP.rotationSrc = BigWorld.camera().invViewMatrix
		XModLib.AppLoader.AppLoader.getBattleApp().minimap._Minimap__cameraMatrix.source = minimapStrategicCellMP
	return

_inject_hooks_ += functools.partial(setattr, AvatarInputHandler.DynamicCameras.StrategicCamera.StrategicCamera, 'XSwitchMode', new_StrategicCamera_XSwitchMode)

def new_StrategicCamera_XIncreaseCameraBasePitch(self):
	if BigWorld.player().inputHandler.ctrlModeName != 'strategic':
		return None
	shotPoint = self.aimingSystem.getDesiredShotPoint()
	if shotPoint is not None and hasattr(self.aimingSystem, 'XStrategicSniper') and self.aimingSystem.XStrategicSniper is not None and self.aimingSystem.XStrategicSniper.isSniperMode:
		result = self.aimingSystem.XStrategicSniper.increaseCameraBasePitch()
		self.aimingSystem.updateTargetPos(shotPoint)
		return result
	return None

_inject_hooks_ += functools.partial(setattr, AvatarInputHandler.DynamicCameras.StrategicCamera.StrategicCamera, 'XIncreaseCameraBasePitch', new_StrategicCamera_XIncreaseCameraBasePitch)

def new_StrategicCamera_XDecreaseCameraBasePitch(self):
	if BigWorld.player().inputHandler.ctrlModeName != 'strategic':
		return None
	shotPoint = self.aimingSystem.getDesiredShotPoint()
	if shotPoint is not None and hasattr(self.aimingSystem, 'XStrategicSniper') and self.aimingSystem.XStrategicSniper is not None and self.aimingSystem.XStrategicSniper.isSniperMode:
		result = self.aimingSystem.XStrategicSniper.decreaseCameraBasePitch()
		self.aimingSystem.updateTargetPos(shotPoint)
		return result
	return None

_inject_hooks_ += functools.partial(setattr, AvatarInputHandler.DynamicCameras.StrategicCamera.StrategicCamera, 'XDecreaseCameraBasePitch', new_StrategicCamera_XDecreaseCameraBasePitch)
