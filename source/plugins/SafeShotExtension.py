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
import Avatar
import Vehicle
import AvatarInputHandler
import AvatarInputHandler.control_modes

# *************************
# X-Mod Code Library
# *************************
import XModLib.ArenaInfo
import XModLib.HookUtils
import XModLib.KeyboardUtils
import XModLib.ClientMessages
import XModLib.TargetScanners

# *************************
# GunControlMode Hooks
# *************************
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.control_modes._GunControlMode, 'updateGunMarker')
def new_GunControlMode_updateGunMarker(self, markerType, pos, dir, size, relaxTime, collData):
	gunTarget = collData.entity if collData is not None else None
	if markerType == AvatarInputHandler.aih_constants.GUN_MARKER_TYPE.CLIENT:
		self._clientTarget = gunTarget
	elif markerType == AvatarInputHandler.aih_constants.GUN_MARKER_TYPE.SERVER:
		self._serverTarget = gunTarget
	return

# *************************
# Vehicle Hooks
# *************************
@XModLib.HookUtils.methodHookExt(_inject_hooks_, Vehicle.Vehicle, '_Vehicle__onVehicleDeath')
def new_Vehicle_onVehicleDeath(self, isDeadStarted=False):
	if not isDeadStarted:
		self._deathTime = BigWorld.time()
	return

# *************************
# AvatarInputHandler Hooks
# *************************
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.AvatarInputHandler, 'handleKeyEvent')
def new_AvatarInputHandler_handleKeyEvent(self, event):
	if not self._AvatarInputHandler__isStarted or self.isDetached:
		return
	## Keyboard event parsing
	event = XModLib.KeyboardUtils.KeyboardEvent(event)
	## HotKeys - Common
	if self.ctrlModeName in (AvatarInputHandler.aih_constants.CTRL_MODE_NAME.ARCADE, AvatarInputHandler.aih_constants.CTRL_MODE_NAME.SNIPER, AvatarInputHandler.aih_constants.CTRL_MODE_NAME.STRATEGIC):
		## HotKeys - SafeShot
		config = _config_['plugins']['safeShot']
		if config['enabled']:
			## HotKeys - SafeShot - Global
			config = _config_['plugins']['safeShot']
			shortcutHandle = config['enabled'] and config['shortcut'](event)
			if shortcutHandle and (not shortcutHandle.switch or shortcutHandle.pushed):
				config['activated'] = shortcutHandle(config['activated'])
				if shortcutHandle.switch and config['activated']:
					XModLib.ClientMessages.showMessageOnPanel(
						'Player',
						None,
						config['message']['onActivate'],
						'green'
					)
				elif shortcutHandle.switch:
					XModLib.ClientMessages.showMessageOnPanel(
						'Player',
						None,
						config['message']['onDeactivate'],
						'red'
					)
				pass
	return

# *************************
# PlayerAvatar Hooks
# *************************
@XModLib.HookUtils.methodHookExt(_inject_hooks_, Avatar.PlayerAvatar, 'shoot', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_PlayerAvatar_shoot(old_PlayerAvatar_shoot, self, *args, **kwargs):
	config = _config_['plugins']['safeShot']
	if not config['enabled'] or not config['activated']:
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
	error = _globals_['macrosFormatter'](config['template'], reason=rconfig['template'])
	XModLib.ClientMessages.showMessageOnPanel('VehicleError', reason, error, 'red')
	if reason == 'team' and rconfig['chat']['enabled']:
		channel = XModLib.ClientMessages.getBattleChatControllers()[1]
		if channel is not None and channel.canSendMessage()[0]:
			message = _globals_['macrosFormatter'](rconfig['chat']['message'], player=getPlayerName(target.id), vehicle=getShortName(target.id))
			channel.sendMessage(message.encode('utf-8'))
	if self._PlayerAvatar__tryShootCallbackId is None:
		self._PlayerAvatar__tryShootCallbackId = BigWorld.callback(0.0, self._PlayerAvatar__tryShootCallback)
	return
