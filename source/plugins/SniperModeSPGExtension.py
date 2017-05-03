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
import gui.Scaleform.daapi.view.battle.shared.crosshair.gm_factory

# *************************
# X-Mod Code Library
# *************************
import XModLib.HookUtils
import XModLib.KeyboardUtils

# *************************
# ControlMarkersFactory Hooks
# *************************
@XModLib.HookUtils.methodHookExt(_inject_hooks_, gui.Scaleform.daapi.view.battle.shared.crosshair.gm_factory._ControlMarkersFactory, '_createSPGMarkers', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_ControlMarkersFactory_createSPGMarkers(old_ControlMarkersFactory_createSPGMarkers, self, markersInfo, components=None):
	result = old_ControlMarkersFactory_createSPGMarkers(self, markersInfo, components=components)
	if markersInfo.isServerMarkerActivated:
		dataProvider = markersInfo.serverMarkerDataProvider
		markerType = AvatarInputHandler.aih_constants.GUN_MARKER_TYPE.SERVER
	elif markersInfo.isClientMarkerActivated:
		dataProvider = markersInfo.clientMarkerDataProvider
		markerType = AvatarInputHandler.aih_constants.GUN_MARKER_TYPE.CLIENT
	else:
		dataProvider = None
		markerType = AvatarInputHandler.aih_constants.GUN_MARKER_TYPE.UNDEFINED
	return result + (self._createSniperMarker(markerType, dataProvider, components=components), )

# *************************
# ArcadeControlMode Hooks
# *************************
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.ArcadeControlMode, '_ArcadeControlMode__activateAlternateMode')
def new_ArcadeControlMode_activateAlternateMode(self, pos=None, bByScroll=False):
	if not BigWorld.player().isGunLocked and not BigWorld.player().isOwnBarrelUnderWater:
		if self._aih.isSPG and bByScroll:
			self._aih.onControlModeChanged(
				AvatarInputHandler.aih_constants.CTRL_MODE_NAME.SNIPER,
				preferredPos=self.camera.aimingSystem.getDesiredShotPoint(),
				aimingMode=self.aimingMode,
				saveZoom=False,
				equipmentID=None
			)
	return

@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes.ArcadeControlMode, 'handleKeyEvent')
def new_ArcadeControlMode_handleKeyEvent(self, isDown, key, mods, event=None):
	## Keyboard event parsing
	event = XModLib.KeyboardUtils.KeyboardEvent(event)
	## HotKeys - SPG Sniper Mode
	if self._aih.isSPG:
		config = _config_['plugins']['sniperModeSPG']
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
		config = _config_['plugins']['sniperModeSPG']
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
