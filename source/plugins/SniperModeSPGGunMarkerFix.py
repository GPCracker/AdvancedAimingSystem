# *************************
# Python
# *************************
# Nothing

# *************************
# BigWorld
# *************************
# Nothing

# *************************
# WoT Client
# *************************
import AvatarInputHandler.aih_constants

# *************************
# WoT Client Hooks
# *************************
import gui.Scaleform.daapi.view.battle.shared.crosshair.gm_factory

# *************************
# X-Mod Code Library
# *************************
import XModLib.HookUtils

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
