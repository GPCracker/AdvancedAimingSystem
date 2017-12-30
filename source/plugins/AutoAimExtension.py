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

# -------------------------- #
#    CommandMapping Hooks    #
# -------------------------- #
@XModLib.HookUtils.methodHookExt(_inject_hooks_, CommandMapping.CommandMapping, 'isFired', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_CommandMapping_isFired(old_CommandMapping_isFired, self, command, key):
	return command != CommandMapping.CMD_CM_LOCK_TARGET and old_CommandMapping_isFired(self, command, key)

# ------------------------------ #
#    AutoAimControlMode Hooks    #
# ------------------------------ #
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.ArcadeControlMode, 'handleKeyEvent', invoke=XModLib.HookUtils.HookInvoke.MASTER)
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.SniperControlMode, 'handleKeyEvent', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_AutoAimControlMode_handleKeyEvent(old_AutoAimControlMode_handleKeyEvent, self, isDown, key, mods, event=None):
	result = old_AutoAimControlMode_handleKeyEvent(self, isDown, key, mods, event)
	if not result and CommandMapping.g_instance.get('CMD_CM_LOCK_TARGET') == key and isDown:
		target = BigWorld.target()
		# Target substitution begins.
		if target is None and _config_['plugins']['autoAim']['useTargetScan']:
			targetScanner = getattr(self._aih, 'XTargetScanner', None)
			if targetScanner is not None:
				target = targetScanner.scanTarget().target
		if target is None and _config_['plugins']['autoAim']['useTargetInfo']:
			targetInfo = getattr(self._aih, 'XTargetInfo', None)
			if targetInfo is not None and not targetInfo.isExpired:
				target = targetInfo.getVehicle()
		# Target substitution ends.
		BigWorld.player().autoAim(target)
	return result
