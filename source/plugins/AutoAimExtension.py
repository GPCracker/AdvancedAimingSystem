# ------------ #
#    Python    #
# ------------ #
# nothing

# -------------- #
#    BigWorld    #
# -------------- #
import Math
import BigWorld

# ---------------- #
#    WoT Client    #
# ---------------- #
import CommandMapping

# ---------------------- #
#    WoT Client Hooks    #
# ---------------------- #
import AvatarInputHandler.control_modes

# ------------------- #
#    X-Mod Library    #
# ------------------- #
import XModLib.HookUtils

# ----------------------------------- #
#    Plug-in default configuration    #
# ----------------------------------- #
g_globals['appDefaultConfig']['plugins']['autoAim'] = {
	'enabled': ('Bool', False),
	'useTargetScan': ('Bool', False),
	'useTargetInfo': ('Bool', False)
}

# ----------------------------------------- #
#    Plug-in configuration reading stage    #
# ----------------------------------------- #
g_config['plugins']['autoAim'] = g_globals['appConfigReader'](
	XModLib.XMLConfigReader.overrideOpenSubSection(g_globals['appConfigFile'], 'plugins/autoAim'),
	g_globals['appDefaultConfig']['plugins']['autoAim']
)

# ------------------------------------ #
#    Plug-in hooks injection events    #
# ------------------------------------ #
p_inject_hooks = XModLib.HookUtils.HookEvent()
p_inject_ovrds = XModLib.HookUtils.HookEvent()

# ------------------------ #
#    Plug-in init stage    #
# ------------------------ #
if g_config['applicationEnabled'] and g_config['plugins']['autoAim']['enabled']:
	p_inject_stage_main += p_inject_hooks
	p_inject_stage_init += p_inject_ovrds

# -------------------------- #
#    CommandMapping Hooks    #
# -------------------------- #
@XModLib.HookUtils.methodHookExt(p_inject_hooks, CommandMapping.CommandMapping, 'isFired', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_CommandMapping_isFired(old_CommandMapping_isFired, self, command, key):
	return command != CommandMapping.CMD_CM_LOCK_TARGET and old_CommandMapping_isFired(self, command, key)

# ------------------------------ #
#    AutoAimControlMode Hooks    #
# ------------------------------ #
@XModLib.HookUtils.methodHookExt(p_inject_hooks, AvatarInputHandler.control_modes.ArcadeControlMode, 'handleKeyEvent', invoke=XModLib.HookUtils.HookInvoke.MASTER)
@XModLib.HookUtils.methodHookExt(p_inject_hooks, AvatarInputHandler.control_modes.SniperControlMode, 'handleKeyEvent', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_AutoAimControlMode_handleKeyEvent(old_AutoAimControlMode_handleKeyEvent, self, isDown, key, mods, event=None):
	result = old_AutoAimControlMode_handleKeyEvent(self, isDown, key, mods, event)
	if not result and CommandMapping.g_instance.get('CMD_CM_LOCK_TARGET') == key and isDown:
		target = BigWorld.target()
		# Target substitution begins.
		if target is None and g_config['plugins']['autoAim']['useTargetScan']:
			targetScanner = getattr(self._aih, 'XTargetScanner', None)
			if targetScanner is not None:
				target = targetScanner.scanTarget().target
		if target is None and g_config['plugins']['autoAim']['useTargetInfo']:
			targetInfo = getattr(self._aih, 'XTargetInfo', None)
			if targetInfo is not None and not targetInfo.isExpired:
				target = targetInfo.getVehicle()
		# Target substitution ends.
		BigWorld.player().autoAim(target)
	return result
