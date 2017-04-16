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
import collections

# *************************
# BigWorld
# *************************
import Math
import BigWorld

# *************************
# WoT Client
# *************************
import constants
import gui.shared.personality
import AvatarInputHandler.cameras
import AvatarInputHandler.aih_constants

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
import gui.Scaleform.genConsts.BATTLE_VIEW_ALIASES
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
import XModLib.ArenaInfo
import XModLib.HookUtils
import XModLib.MathUtils
import XModLib.TextUtils
import XModLib.EngineUtils
import XModLib.VehicleInfo
import XModLib.VehicleMath
import XModLib.VehicleBounds
import XModLib.CallbackUtils
import XModLib.KeyboardUtils
import XModLib.BallisticsMath
import XModLib.ClientMessages
import XModLib.CollisionUtils
import XModLib.TargetScanners
import XModLib.XMLConfigReader

# *************************
# X-Mod GUI Library
# *************************
import XModLib.pygui.battle.views.PanelsLoaderView
import XModLib.pygui.battle.views.components.panels.TextPanel
