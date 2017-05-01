# *************************
# Python
# *************************
# Nothing

# *************************
# BigWorld
# *************************
import BigWorld

# *************************
# WoT Client
# *************************
import AvatarInputHandler.aih_constants

# *************************
# WoT Client Hooks
# *************************
import AvatarInputHandler.control_modes

# *************************
# X-Mod Code Library
# *************************
import XModLib.HookUtils
import XModLib.KeyboardUtils

# *************************
# ArcadeControlMode Hooks
# *************************
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.ArcadeControlMode, 'handleKeyEvent')
def new_ArcadeControlMode_handleKeyEvent(self, isDown, key, mods, event=None):
	## Keyboard event parsing
	event = XModLib.KeyboardUtils.KeyboardEvent(event)
	## HotKeys - SPG Sniper Mode
	if self._aih.isSPG:
		config = _config_['commonAS']['sniperModeSPG']
		shortcutHandle = config['enabled'] and config['shortcut'](event)
		if shortcutHandle and shortcutHandle.pushed:
			if not BigWorld.player().isGunLocked and not BigWorld.player().isOwnBarrelUnderWater:
				self._aih.onControlModeChanged(
					AvatarInputHandler.aih_constants.CTRL_MODE_NAME.SNIPER,
					preferredPos=self.camera.aimingSystem.getDesiredShotPoint(),
					aimingMode=self.aimingMode,
					saveZoom=True,
					equipmentID=None
				)
	return

# *************************
# SniperControlMode Hooks
# *************************
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.SniperControlMode, 'handleKeyEvent')
def new_SniperControlMode_handleKeyEvent(self, isDown, key, mods, event=None):
	## Keyboard event parsing
	event = XModLib.KeyboardUtils.KeyboardEvent(event)
	## HotKeys - SPG Sniper Mode
	if self._aih.isSPG:
		config = _config_['commonAS']['sniperModeSPG']
		shortcutHandle = config['enabled'] and config['shortcut'](event)
		if shortcutHandle and shortcutHandle.pushed:
			if not BigWorld.player().isGunLocked and not BigWorld.player().isOwnBarrelUnderWater:
				self._aih.onControlModeChanged(
					AvatarInputHandler.aih_constants.CTRL_MODE_NAME.ARCADE,
					preferredPos=self.camera.aimingSystem.getDesiredShotPoint(),
					turretYaw=self.camera.aimingSystem.turretYaw,
					gunPitch=self.camera.aimingSystem.gunPitch,
					aimingMode=self.aimingMode,
					closesDist=False
				)
	return
