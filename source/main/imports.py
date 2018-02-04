# ------------ #
#    Python    #
# ------------ #
import os
import sys
import enum
import math
import time
import marshal
import weakref
import zipfile
import operator
import functools
import itertools
import collections

# -------------- #
#    BigWorld    #
# -------------- #
import Math
import BigWorld

# ---------------- #
#    WoT Client    #
# ---------------- #
import constants
import gui.shared.personality
import AvatarInputHandler.cameras
import AvatarInputHandler.aih_constants
import AvatarInputHandler.aih_global_binding

# -------------------- #
#    WoT Client GUI    #
# -------------------- #
import gui.shared
import gui.shared.events
import gui.app_loader.settings
import gui.Scaleform.framework.package_layout

# ---------------------- #
#    WoT Client Hooks    #
# ---------------------- #
import Avatar
import Account
import Vehicle
import AvatarInputHandler
import AvatarInputHandler.control_modes
import AvatarInputHandler.DynamicCameras.StrategicCamera
import AvatarInputHandler.AimingSystems.StrategicAimingSystem

# -------------------------- #
#    WoT Client GUI Hooks    #
# -------------------------- #
import gui.Scaleform.battle_entry
import gui.Scaleform.daapi.view.battle.shared

# ------------------- #
#    X-Mod Library    #
# ------------------- #
import XModLib.ArenaInfo
import XModLib.HookUtils
import XModLib.MathUtils
import XModLib.TextUtils
import XModLib.ClientUtils
import XModLib.EngineUtils
import XModLib.VehicleInfo
import XModLib.VehicleMath
import XModLib.VehicleBounds
import XModLib.CallbackUtils
import XModLib.KeyboardUtils
import XModLib.BallisticsMath
import XModLib.ClientMessages
import XModLib.CollisionUtils
import XModLib.IngameSettings
import XModLib.TargetScanners
import XModLib.XMLConfigReader

# ----------------------- #
#    X-Mod GUI Library    #
# ----------------------- #
import XModLib.pygui.battle.library
import XModLib.pygui.battle.views.handlers.ContextMenuHandler
import XModLib.pygui.battle.views.components.panels.TextPanel
