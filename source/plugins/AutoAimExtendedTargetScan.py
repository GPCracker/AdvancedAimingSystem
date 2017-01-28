# *************************
# Python
# *************************
# Nothing

# *************************
# BigWorld
# *************************
import Math
import BigWorld

# *************************
# WoT Client
# *************************
import CommandMapping

# *************************
# WoT Client Hooks
# *************************
import AvatarInputHandler.control_modes

# *************************
# X-Mod Code Library
# *************************
import XModLib.HookUtils

# *************************
# AutoAimControlMode Hooks
# *************************
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.ArcadeControlMode, 'handleKeyEvent', invoke=XModLib.HookUtils.HookInvoke.MASTER)
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.SniperControlMode, 'handleKeyEvent', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_AutoAimControlMode_handleKeyEvent(old_AutoAimControlMode_handleKeyEvent, self, isDown, key, mods, event=None):
	if CommandMapping.g_instance.isFired(CommandMapping.CMD_CM_LOCK_TARGET, key) and isDown:
		target = BigWorld.target()
		if target is None and _config_['commonAS']['autoAim']['useTargetScan']:
			targetScanner = getattr(self._aih, 'XTargetScanner', None)
			if targetScanner is not None:
				target = targetScanner.scanTarget().target
		if target is None and _config_['commonAS']['autoAim']['useTargetInfo']:
			targetInfo = getattr(self._aih, 'XTargetInfo', None)
			if targetInfo is not None and not targetInfo.isExpired:
				target = targetInfo.getVehicle()
		BigWorld.player().autoAim(target)
		return True
	if CommandMapping.g_instance.isFired(CommandMapping.CMD_CM_LOCK_TARGET_OFF, key) and isDown:
		BigWorld.player().autoAim(None)
		return True
	return old_AutoAimControlMode_handleKeyEvent(self, isDown, key, mods, event)
