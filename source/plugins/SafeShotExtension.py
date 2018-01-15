# ------------ #
#    Python    #
# ------------ #
# nothing

# -------------- #
#    BigWorld    #
# -------------- #
import BigWorld

# ---------------- #
#    WoT Client    #
# ---------------- #
import AvatarInputHandler.aih_constants

# ---------------------- #
#    WoT Client Hooks    #
# ---------------------- #
import Avatar
import Vehicle
import AvatarInputHandler.control_modes

# ------------------- #
#    X-Mod Library    #
# ------------------- #
import XModLib.ArenaInfo
import XModLib.HookUtils
import XModLib.KeyboardUtils
import XModLib.ClientMessages
import XModLib.TargetScanners

# ----------------------------------- #
#    Plug-in default configuration    #
# ----------------------------------- #
g_globals['appDefaultConfig']['plugins']['safeShot'] = {
	'enabled': ('Bool', False),
	'activated': ('Bool', True),
	'shortcut': ('AdvancedShortcut', {
		'sequence': ('String', 'KEY_LALT'),
		'switch': ('Bool', False),
		'invert': ('Bool', True)
	}),
	'message': {
		'onActivate': ('LocalizedWideString', u'[SafeShot] ENABLED.'),
		'onDeactivate': ('LocalizedWideString', u'[SafeShot] DISABLED.')
	},
	'useGunTarget': ('Bool', True),
	'considerBlueHostile': ('Bool', False),
	'fragExpirationTimeout': ('Float', 2.0),
	'template': ('LocalizedStandardTemplate', u'[{reason}] Shot has been blocked.'),
	'reasons': {
		'team': {
			'enabled': ('Bool', True),
			'chat': {
				'enabled': ('Bool', True),
				'message': ('LocalizedStandardTemplate', u'{player} ({vehicle}), you\'re in my line of fire!')
			},
			'template': ('LocalizedWideString', u'friendly')
		},
		'dead': {
			'enabled': ('Bool', True),
			'template': ('LocalizedWideString', u'corpse')
		},
		'waste': {
			'enabled': ('Bool', False),
			'template': ('LocalizedWideString', u'waste')
		}
	}
}

# ----------------------------------------- #
#    Plug-in configuration reading stage    #
# ----------------------------------------- #
g_config['plugins']['safeShot'] = g_globals['appConfigReader'](
	XModLib.XMLConfigReader.overrideOpenSubSection(g_globals['appConfigFile'], 'plugins/safeShot'),
	g_globals['appDefaultConfig']['plugins']['safeShot']
)

# ------------------------------------ #
#    Plug-in hooks injection events    #
# ------------------------------------ #
p_inject_hooks = XModLib.HookUtils.HookEvent()
p_inject_ovrds = XModLib.HookUtils.HookEvent()

# ------------------------ #
#    Plug-in init stage    #
# ------------------------ #
if g_config['applicationEnabled'] and g_config['plugins']['safeShot']['enabled']:
	p_inject_stage_main += p_inject_hooks
	p_inject_stage_init += p_inject_ovrds

# -------------------------- #
#    GunControlMode Hooks    #
# -------------------------- #
@XModLib.HookUtils.methodHookExt(p_inject_hooks, AvatarInputHandler.control_modes._GunControlMode, 'updateGunMarker')
def new_GunControlMode_updateGunMarker(self, markerType, pos, dir, size, relaxTime, collData):
	gunTarget = collData.entity if collData is not None else None
	if markerType == AvatarInputHandler.aih_constants.GUN_MARKER_TYPE.CLIENT:
		self._clientTarget = gunTarget
	elif markerType == AvatarInputHandler.aih_constants.GUN_MARKER_TYPE.SERVER:
		self._serverTarget = gunTarget
	return

# ------------------- #
#    Vehicle Hooks    #
# ------------------- #
@XModLib.HookUtils.methodHookExt(p_inject_hooks, Vehicle.Vehicle, '_Vehicle__onVehicleDeath')
def new_Vehicle_onVehicleDeath(self, isDeadStarted=False):
	if not isDeadStarted:
		self._deathTime = BigWorld.time()
	return

# ------------------------------- #
#    SafeShotControlMode Hooks    #
# ------------------------------- #
@XModLib.HookUtils.methodHookExt(p_inject_hooks, AvatarInputHandler.control_modes.ArcadeControlMode, 'handleKeyEvent')
@XModLib.HookUtils.methodHookExt(p_inject_hooks, AvatarInputHandler.control_modes.SniperControlMode, 'handleKeyEvent')
def new_SafeShotControlMode_handleKeyEvent(self, isDown, key, mods, event=None):
	## Keyboard event parsing
	kbevent = XModLib.KeyboardUtils.KeyboardEvent(event)
	## AvatarInputHandler started, not detached, control mode supported (for AvatarInputHandler shortcuts)
	if True:
		## HotKeys - SafeShot
		mconfig = g_config['plugins']['safeShot']
		if mconfig['enabled']:
			## HotKeys - SafeShot - Global
			fconfig = mconfig
			shortcutHandle = fconfig['enabled'] and fconfig['shortcut'](kbevent)
			if shortcutHandle and (not shortcutHandle.switch or shortcutHandle.pushed):
				fconfig['activated'] = shortcutHandle(fconfig['activated'])
				if shortcutHandle.switch and fconfig['activated']:
					XModLib.ClientMessages.showMessageOnPanel(
						'Player',
						None,
						fconfig['message']['onActivate'],
						'green'
					)
				elif shortcutHandle.switch:
					XModLib.ClientMessages.showMessageOnPanel(
						'Player',
						None,
						fconfig['message']['onDeactivate'],
						'red'
					)
				pass
	return

# ------------------------ #
#    PlayerAvatar Hooks    #
# ------------------------ #
@XModLib.HookUtils.methodHookExt(p_inject_hooks, Avatar.PlayerAvatar, 'shoot', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_PlayerAvatar_shoot(old_PlayerAvatar_shoot, self, *args, **kwargs):
	config = g_config['plugins']['safeShot']
	def isIgnoredCtrlMode(ctrlModeName):
		return ctrlModeName not in (AvatarInputHandler.aih_constants.CTRL_MODE_NAME.ARCADE, AvatarInputHandler.aih_constants.CTRL_MODE_NAME.SNIPER)
	if not config['enabled'] or not config['activated'] or isIgnoredCtrlMode(self.inputHandler.ctrlModeName):
		return old_PlayerAvatar_shoot(self, *args, **kwargs)
	gunTargetClient = getattr(self.inputHandler.ctrl, '_clientTarget', None)
	gunTargetServer = getattr(self.inputHandler.ctrl, '_serverTarget', None)
	gunTarget = gunTargetClient or gunTargetServer
	aimTarget = XModLib.TargetScanners.StandardScanner().getTarget()
	aimTarget = aimTarget or (gunTarget if config['useGunTarget'] else None)
	isEnemy = XModLib.ArenaInfo.isEnemy
	isTeamKiller = XModLib.ArenaInfo.isTeamKiller
	getShortName = XModLib.ArenaInfo.getShortName
	getPlayerName = XModLib.ArenaInfo.getPlayerName
	def isHostile(vehicleID):
		return isEnemy(vehicleID) or config['considerBlueHostile'] and isTeamKiller(vehicleID)
	def isFreshFrag(vehicle):
		return not vehicle.isAlive() and getattr(vehicle, '_deathTime', BigWorld.time()) + config['fragExpirationTimeout'] >= BigWorld.time()
	def isWasteCtrlMode(ctrlModeName):
		return ctrlModeName in (AvatarInputHandler.aih_constants.CTRL_MODE_NAME.ARCADE, )
	reason, target = None, None
	if config['reasons']['waste']['enabled'] and gunTarget is None and isWasteCtrlMode(self.inputHandler.ctrlModeName):
		reason, target = 'waste', gunTarget
	elif config['reasons']['team']['enabled'] and aimTarget is not None and aimTarget.isAlive() and not isHostile(aimTarget.id):
		reason, target = 'team', aimTarget
	elif config['reasons']['dead']['enabled'] and aimTarget is not None and isFreshFrag(aimTarget) and isHostile(aimTarget.id):
		reason, target = 'dead', aimTarget
	if reason is None:
		return old_PlayerAvatar_shoot(self, *args, **kwargs)
	rconfig = config['reasons'][reason]
	error = config['template'](reason=rconfig['template'])
	XModLib.ClientMessages.showMessageOnPanel('VehicleError', reason, error, 'red')
	if reason == 'team' and rconfig['chat']['enabled']:
		channel = XModLib.ClientMessages.getBattleChatControllers()[1]
		if channel is not None and channel.canSendMessage()[0]:
			message = rconfig['chat']['message'](player=getPlayerName(target.id), vehicle=getShortName(target.id))
			channel.sendMessage(message.encode('utf-8'))
	if self._PlayerAvatar__tryShootCallbackId is None:
		self._PlayerAvatar__tryShootCallbackId = BigWorld.callback(0.0, self._PlayerAvatar__tryShootCallback)
	return
