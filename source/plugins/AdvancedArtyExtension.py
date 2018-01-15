# ------------ #
#    Python    #
# ------------ #
import math

# -------------- #
#    BigWorld    #
# -------------- #
import Math
import BigWorld

# ---------------- #
#    WoT Client    #
# ---------------- #
import AvatarInputHandler.cameras

# ---------------------- #
#    WoT Client Hooks    #
# ---------------------- #
import gui.battle_control.matrix_factory
import AvatarInputHandler.control_modes
import AvatarInputHandler.DynamicCameras.ArtyCamera

# ------------------- #
#    X-Mod Library    #
# ------------------- #
import XModLib.HookUtils
import XModLib.MathUtils
import XModLib.KeyboardUtils
import XModLib.ClientMessages

# ----------------------------------- #
#    Plug-in default configuration    #
# ----------------------------------- #
g_globals['appDefaultConfig']['plugins']['advancedArty'] = {
	'enabled': ('Bool', False),
	'cameraAdjustment': {
		'enabled': ('Bool', True),
		'interpolationSpeed': ('Float', 5.0),
		'disableInterpolation': ('Bool', True),
		'disableHighPitchLevel': ('Bool', True)
	},
	'orthogonalView': {
		'enabled': ('Bool', True),
		'activated': ('Bool', False),
		'shortcut': ('AdvancedShortcut', {
			'sequence': ('String', 'KEY_LALT+KEY_MIDDLEMOUSE'),
			'switch': ('Bool', True),
			'invert': ('Bool', False)
		}),
		'cameraDistance': ('Float', 700.0),
		'preserveLastView': ('Bool', True)
	}
}

# ----------------------------------------- #
#    Plug-in configuration reading stage    #
# ----------------------------------------- #
g_config['plugins']['advancedArty'] = g_globals['appConfigReader'](
	XModLib.XMLConfigReader.overrideOpenSubSection(g_globals['appConfigFile'], 'plugins/advancedArty'),
	g_globals['appDefaultConfig']['plugins']['advancedArty']
)

# ------------------------------------ #
#    Plug-in hooks injection events    #
# ------------------------------------ #
p_inject_hooks = XModLib.HookUtils.HookEvent()
p_inject_ovrds = XModLib.HookUtils.HookEvent()

# ------------------------ #
#    Plug-in init stage    #
# ------------------------ #
if g_config['applicationEnabled'] and g_config['plugins']['advancedArty']['enabled']:
	p_inject_stage_main += p_inject_hooks
	p_inject_stage_init += p_inject_ovrds

# ---------------------- #
#    ArtyCamera Hooks    #
# ---------------------- #
@XModLib.HookUtils.methodHookExt(p_inject_hooks, AvatarInputHandler.DynamicCameras.ArtyCamera.ArtyCamera, '__init__')
def new_ArtyCamera_init(self, *args, **kwargs):
	config = g_config['plugins']['advancedArty']
	if config['enabled']:
		if config['cameraAdjustment']['enabled']:
			self._ArtyCamera__cfg['interpolationSpeed'] = config['cameraAdjustment']['interpolationSpeed']
		if config['orthogonalView']['enabled']:
			self._ArtyCamera__strategicAreaViewScaleMatrix = XModLib.MathUtils.getIdentityMatrix()
	return

@XModLib.HookUtils.methodHookExt(p_inject_hooks, AvatarInputHandler.DynamicCameras.ArtyCamera.ArtyCamera, '_ArtyCamera__interpolateStates', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_ArtyCamera_interpolateStates(old_ArtyCamera_interpolateStates, self, deltaTime, translation, rotation):
	config = g_config['plugins']['advancedArty']
	if config['enabled'] and config['cameraAdjustment']['enabled'] and config['cameraAdjustment']['disableInterpolation']:
		self._ArtyCamera__sourceMatrix = rotation
		self._ArtyCamera__targetMatrix.translation = translation
		return self._ArtyCamera__sourceMatrix, self._ArtyCamera__targetMatrix
	return old_ArtyCamera_interpolateStates(self, deltaTime, translation, rotation)

@XModLib.HookUtils.methodHookExt(p_inject_hooks, AvatarInputHandler.DynamicCameras.ArtyCamera.ArtyCamera, '_ArtyCamera__choosePitchLevel', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_ArtyCamera_choosePitchLevel(old_ArtyCamera_choosePitchLevel, self, *args, **kwargs):
	result = old_ArtyCamera_choosePitchLevel(self, *args, **kwargs)
	config = g_config['plugins']['advancedArty']
	if config['enabled'] and config['cameraAdjustment']['enabled']:
		return result and not config['cameraAdjustment']['disableHighPitchLevel']
	return result

@XModLib.HookUtils.propertyAddExt(p_inject_ovrds, AvatarInputHandler.DynamicCameras.ArtyCamera.ArtyCamera, 'strategicAreaViewScaleMatrix', XModLib.HookUtils.PropertyAction.GET)
def new_ArtyCamera_strategicAreaViewScaleMatrix_getter(self):
	return getattr(self, '_ArtyCamera__strategicAreaViewScaleMatrix', XModLib.MathUtils.getIdentityMatrix())

@XModLib.HookUtils.methodHookExt(p_inject_hooks, AvatarInputHandler.DynamicCameras.ArtyCamera.ArtyCamera, '_ArtyCamera__calculateIdealState', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_ArtyCamera_calculateIdealState(old_ArtyCamera_calculateIdealState, self, *args, **kwargs):
	translation, rotation = old_ArtyCamera_calculateIdealState(self, *args, **kwargs)
	config = g_config['plugins']['advancedArty']
	if config['enabled'] and config['orthogonalView']['enabled'] and config['orthogonalView']['activated']:
		translation = self.aimingSystem.aimPoint - self._ArtyCamera__getCameraDirection().scale(config['orthogonalView']['cameraDistance'])
	return translation, rotation

@XModLib.HookUtils.methodHookExt(p_inject_hooks, AvatarInputHandler.DynamicCameras.ArtyCamera.ArtyCamera, '_ArtyCamera__cameraUpdate')
def new_ArtyCamera_cameraUpdate(self, *args, **kwargs):
	config = g_config['plugins']['advancedArty']
	if config['enabled'] and config['orthogonalView']['enabled']:
		cameraDistanceRate = self._ArtyCamera__desiredCamDist / self._ArtyCamera__camDist
		verticalFovHalf = AvatarInputHandler.cameras.FovExtended.instance().actualDefaultVerticalFov * 0.5
		fovCorrectionMultiplier = math.atan(math.tan(verticalFovHalf) * cameraDistanceRate) / verticalFovHalf
		AvatarInputHandler.cameras.FovExtended.instance().setFovByMultiplier(fovCorrectionMultiplier)
		self._ArtyCamera__strategicAreaViewScaleMatrix.setScale(Math.Vector3(1.0, 1.0, 1.0).scale(cameraDistanceRate))
	return

@XModLib.HookUtils.methodHookExt(p_inject_hooks, AvatarInputHandler.DynamicCameras.ArtyCamera.ArtyCamera, 'enable', invoke=XModLib.HookUtils.HookInvoke.SECONDARY)
def new_ArtyCamera_enable(self, *args, **kwargs):
	config = g_config['plugins']['advancedArty']
	if config['enabled'] and config['orthogonalView']['enabled']:
		AvatarInputHandler.cameras.FovExtended.instance().resetFov()
		config['orthogonalView']['activated'] = config['orthogonalView']['activated'] and config['orthogonalView']['preserveLastView']
	return

@XModLib.HookUtils.methodHookExt(p_inject_hooks, AvatarInputHandler.DynamicCameras.ArtyCamera.ArtyCamera, 'disable', invoke=XModLib.HookUtils.HookInvoke.PRIMARY)
def new_ArtyCamera_disable(self, *args, **kwargs):
	config = g_config['plugins']['advancedArty']
	if config['enabled'] and config['orthogonalView']['enabled']:
		AvatarInputHandler.cameras.FovExtended.instance().resetFov()
		config['orthogonalView']['activated'] = config['orthogonalView']['activated'] and config['orthogonalView']['preserveLastView']
	return

# ------------------------- #
#    MatrixFactory Hooks    #
# ------------------------- #
@XModLib.HookUtils.staticMethodHookExt(p_inject_hooks, gui.battle_control.matrix_factory, 'makeArtyAimPointMatrix', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_MatrixFactory_makeArtyAimPointMatrix(old_MatrixFactory_makeArtyAimPointMatrix, *args, **kwargs):
	result = old_MatrixFactory_makeArtyAimPointMatrix(*args, **kwargs)
	config = g_config['plugins']['advancedArty']
	if config['enabled'] and config['orthogonalView']['enabled']:
		return XModLib.MathUtils.getMatrixProduct(BigWorld.player().inputHandler.ctrl.camera.strategicAreaViewScaleMatrix, result)
	return result

# --------------------------- #
#    ArtyControlMode Hooks    #
# --------------------------- #
@XModLib.HookUtils.methodHookExt(p_inject_hooks, AvatarInputHandler.control_modes.ArtyControlMode, 'handleKeyEvent', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_ArtyControlMode_handleKeyEvent(old_ArtyControlMode_handleKeyEvent, self, isDown, key, mods, event=None):
	result = old_ArtyControlMode_handleKeyEvent(self, isDown, key, mods, event=event)
	## Keyboard event parsing
	kbevent = XModLib.KeyboardUtils.KeyboardEvent(event)
	## AvatarInputHandler started, not detached, control mode supported, event not handled by game (for AvatarInputHandler core switches)
	if not result:
		## HotKeys - AdvancedArty
		mconfig = g_config['plugins']['advancedArty']
		if mconfig['enabled']:
			## HotKeys - AdvancedArty - OrthogonalView
			fconfig = mconfig['orthogonalView']
			shortcutHandle = fconfig['enabled'] and fconfig['shortcut'](kbevent)
			if shortcutHandle and (not shortcutHandle.switch or shortcutHandle.pushed):
				fconfig['activated'] = shortcutHandle(fconfig['activated'])
	return result
