# *************************
# Python
# *************************
import os
import math
import time
import marshal
import weakref
import zipfile
import functools

# *************************
# BigWorld
# *************************
import Math
import BigWorld

# *************************
# WoT Client
# *************************
import constants
import gui.battle_control
import gui.shared.personality
import AvatarInputHandler.cameras
import avatar_helpers.aim_global_binding

# *************************
# WoT Client GUI
# *************************
import gui.shared
import gui.shared.events
import gui.app_loader
import gui.app_loader.settings
import gui.Scaleform.framework
import gui.Scaleform.framework.ViewTypes
import gui.Scaleform.framework.package_layout
import gui.Scaleform.framework.ScopeTemplates
import gui.Scaleform.framework.entities.View
import gui.Scaleform.genConsts.BATTLE_VIEW_ALIASES
import gui.Scaleform.daapi.view.meta.BattleDisplayableMeta
import gui.Scaleform.daapi.settings.views

# *************************
# WoT Client Hooks
# *************************
import Avatar
import Account
import Vehicle
import AvatarInputHandler
import AvatarInputHandler.control_modes
import AvatarInputHandler.DynamicCameras.StrategicCamera
import AvatarInputHandler.AimingSystems.StrategicAimingSystem

# *************************
# WoT Client GUI Hooks
# *************************
import gui.Scaleform.daapi.view.battle.shared

# *************************
# X-Mod Library
# *************************
import XModLib.Callback
import XModLib.KeyBoard
import XModLib.Messages
import XModLib.ArenaInfo
import XModLib.Colliders
import XModLib.HookUtils
import XModLib.TextUtils
import XModLib.AGScanners
import XModLib.ClientInfo
import XModLib.ResMgrUtils
import XModLib.VehicleInfo
import XModLib.VehicleMath
import XModLib.XRayScanner
import XModLib.VehicleBounds
import XModLib.BallisticsMath
import XModLib.XMLConfigReader
