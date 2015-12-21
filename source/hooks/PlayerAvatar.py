# *************************
# PlayerAvatar Hooks
# *************************
@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, Avatar.PlayerAvatar, 'shoot', XModLib.HookUtils.HookFunction.CALL_ORIGIN_INSIDE_HOOK)
def new_PlayerAvatar_shoot(old_PlayerAvatar_shoot, self, *args, **kwargs):
	config0 = _config_['commonAS']['safeShot']
	if not config0['enabled'] or not config0['activated']:
		return old_PlayerAvatar_shoot(self, *args, **kwargs)
	deaths = self.arena.XVehiclesDeathTime if hasattr(self.arena, 'XVehiclesDeathTime') and self.arena.XVehiclesDeathTime is not None else dict()
	target, reason = None, None
	aimTarget = BigWorld.target()
	aimTarget = aimTarget if XModLib.VehicleInfo.VehicleInfo.isVehicle(aimTarget) else None
	gunTarget = XModLib.Colliders.Colliders.computePlayerProjectileTrajectoryEnd((
		XModLib.Colliders.Colliders.collideStatic,
		XModLib.Colliders.Colliders.collideSpaceBB,
		functools.partial(XModLib.Colliders.Colliders.collideVehicles, XModLib.Colliders.Colliders.getVisibleVehicles())
	))
	gunTarget = gunTarget[2][1] if gunTarget[2] is not None and len(gunTarget[2]) >= 2 and XModLib.VehicleInfo.VehicleInfo.isVehicle(gunTarget[2][1]) else None
	if config0['waste']['enabled'] and gunTarget is None and config0['waste']['arcade'] and self.inputHandler.ctrlModeName == 'arcade':
		reason = 'waste'
		target = gunTarget
	elif config0['team']['enabled'] and config0['team']['checkGun'] and gunTarget is not None and gunTarget.isAlive() and gunTarget.publicInfo['team'] is self.team and (config0['team']['blue'] if XModLib.ArenaInfo.ArenaInfo.isTeamKiller(gunTarget.id) else config0['team']['normal']):
		reason = 'team'
		target = gunTarget
	elif config0['team']['enabled'] and aimTarget is not None and aimTarget.isAlive() and aimTarget.publicInfo['team'] is self.team and (config0['team']['blue'] if XModLib.ArenaInfo.ArenaInfo.isTeamKiller(aimTarget.id) else config0['team']['normal']):
		reason = 'team'
		target = aimTarget
	elif config0['dead']['enabled'] and aimTarget is not None and not aimTarget.isAlive() and aimTarget.publicInfo['team'] is not self.team and aimTarget.id in deaths and deaths[aimTarget.id] + config0['dead']['timeout'] > BigWorld.time():
		reason = 'dead'
		target = aimTarget
	if reason is None:
		return old_PlayerAvatar_shoot(self, *args, **kwargs)
	message = _globals_['macrosFormatter'](config0['template'], reason=config0['reasons'][reason])
	XModLib.Messages.Messenger.showMessageOnPanel('VehicleErrorsPanel', reason, message, 'red')
	if reason is 'team' and config0['team']['chat']['enabled']:
		channel = XModLib.Messages.Messenger.getBattleChatControllers()[1]
		if channel is not None and (not hasattr(self, 'XSafeShotLastChatVehicleID') or self.XSafeShotLastChatVehicleID is None or self.XSafeShotLastChatVehicleID != target.id or not hasattr(self, 'XSafeShotLastChatTime') or self.XSafeShotLastChatTime + config0['team']['chat']['timeout'] < BigWorld.time()):
			self.XSafeShotLastChatVehicleID = target.id
			self.XSafeShotLastChatTime = BigWorld.time()
			name = self.arena.vehicles[target.id]['name']
			vehicle = self.arena.vehicles[target.id]['vehicleType'].type.shortUserString
			message = _globals_['macrosFormatter'](config0['team']['chat']['template'], name=name, vehicle=vehicle)
			channel.sendMessage(message.encode('utf-8'))
	if self._PlayerAvatar__tryShootCallbackId is None:
		self._PlayerAvatar__tryShootCallbackId = BigWorld.callback(0.0, self._PlayerAvatar__tryShootCallback)
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, Avatar.PlayerAvatar, 'updateVehicleMiscStatus')
def new_PlayerAvatar_updateVehicleMiscStatus(self, vehicleID, code, intArg, floatArg):
	import constants
	config0 = _config_['commonAS']['expert']
	if config0['enabled'] and vehicleID == self.playerVehicleID and code == constants.VEHICLE_MISC_STATUS.OTHER_VEHICLE_DAMAGED_DEVICES_VISIBLE:
		self.XMaySeeOtherVehicleDamagedDevices = bool(intArg)
		if self.XMaySeeOtherVehicleDamagedDevices and (not hasattr(self, 'XExpertPerk') or self.XExpertPerk is None):
			self.XExpertPerk = ExpertPerk(
				lambda: BigWorld.player().XMaySeeOtherVehicleDamagedDevices,
				config0['cache'],
				config0['queue'],
				config0['reply'],
				config0['request']
			)
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, Avatar.PlayerAvatar, 'showOtherVehicleDamagedDevices')
def new_PlayerAvatar_showOtherVehicleDamagedDevices(self, vehicleID, damagedExtras, destroyedExtras):
	if _config_['commonAS']['expert']['enabled']:
		if hasattr(self, 'XExpertPerk') and self.XExpertPerk is not None:
			self.XExpertPerk.onExtrasInfoReceived(vehicleID, damagedExtras, destroyedExtras)
		target = BigWorld.target()
		if XModLib.VehicleInfo.VehicleInfo.isVehicle(target) and target.id == vehicleID:
			XModLib.AppLoader.AppLoader.getBattleApp().damageInfoPanel.show(vehicleID, damagedExtras, destroyedExtras)
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, Avatar.PlayerAvatar, 'targetBlur')
def new_PlayerAvatar_targetBlur(self, prevEntity):
	if _config_['commonAS']['expert']['enabled']:
		if XModLib.VehicleInfo.VehicleInfo.isVehicle(prevEntity) and hasattr(self, 'XMaySeeOtherVehicleDamagedDevices') and self.XMaySeeOtherVehicleDamagedDevices:
			XModLib.AppLoader.AppLoader.getBattleApp().damageInfoPanel.hide()
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, Avatar.PlayerAvatar, 'targetFocus')
def new_PlayerAvatar_targetFocus(self, entity):
	if _config_['commonAS']['expert']['enabled']:
		if XModLib.VehicleInfo.VehicleInfo.isVehicle(entity) and entity.publicInfo['team'] is not self.team and entity.isAlive():
			if hasattr(self, 'XExpertPerk') and self.XExpertPerk is not None:
				self.XExpertPerk.request(entity.id)
				cachedData = self.XExpertPerk.cache.get(entity.id, None)
				if cachedData is not None:
					damagedExtras, destroyedExtras = cachedData
					XModLib.AppLoader.AppLoader.getBattleApp().damageInfoPanel.show(entity.id, damagedExtras, destroyedExtras)
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, Avatar.PlayerAvatar, 'autoAim', XModLib.HookUtils.HookFunction.CALL_ORIGIN_INSIDE_HOOK)
def new_PlayerAvatar_autoAim(old_PlayerAvatar_autoAim, self, target):
	if _config_['commonAS']['expert']['enabled']:
		if XModLib.VehicleInfo.VehicleInfo.isVehicle(target) and target.publicInfo['team'] is not self.team and target.isAlive():
			if hasattr(self, 'XExpertPerk') and self.XExpertPerk is not None:
				self.XExpertPerk.request(target.id)
	if self.inputHandler.ctrlModeName in ['arcade', 'sniper']:
		if target is None and BigWorld.target() is None and _config_['commonAS']['autoAim']['useXRay']:
			target = XModLib.XRayScanner.XRayScanner.getTarget()
		if target is None and BigWorld.target() is None and _config_['commonAS']['autoAim']['useBBox']['enabled']:
			target = XModLib.BBoxScanner.BBoxScanner.getTarget(
				scalar=_config_['commonAS']['autoAim']['useBBox']['scalar'],
				filterVehicle=lambda vehicle: vehicle.publicInfo['team'] is not self.team and vehicle.isAlive()
			)
	return old_PlayerAvatar_autoAim(self, target)

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, Avatar.PlayerAvatar, '_PlayerAvatar__setVisibleGUI')
def new_PlayerAvatar_setVisibleGUI(self, flag):
	currentControl = self.inputHandler.ctrl
	if hasattr(currentControl, 'XAimCorrectionGUI') and currentControl.XAimCorrectionGUI is not None:
		currentControl.XAimCorrectionGUI.gui.visible = True and flag
	if hasattr(currentControl, 'XTargetInfoGUI') and currentControl.XTargetInfoGUI is not None:
		currentControl.XTargetInfoGUI.gui.visible = True and flag
	if hasattr(currentControl, 'XAimingInfo') and currentControl.XAimingInfo is not None:
		ctrlModeName = self.inputHandler.ctrlModeName
		if ctrlModeName in ['arcade', 'sniper', 'strategic']:
			if ctrlModeName == 'arcade':
				config0 = _config_['arcadeAS']['aimingInfo']
			elif ctrlModeName == 'sniper':
				config0 = _config_['sniperAS']['aimingInfo']
			elif ctrlModeName == 'strategic':
				config0 = _config_['strategicAS']['aimingInfo']
			currentControl.XAimingInfo.window.gui.visible = config0['activated'] and flag
	return

def new_PlayerAvatar_isGuiVisible_getter(self):
	if not hasattr(self, '_PlayerAvatar__isGuiVisible'):
		self._PlayerAvatar__isGuiVisible = True
	return self._PlayerAvatar__isGuiVisible

_inject_hooks_ += functools.partial(setattr, Avatar.PlayerAvatar, 'isGuiVisible', property(new_PlayerAvatar_isGuiVisible_getter))

def new_PlayerAvatar_MSOVDD_getter(self):
	if not hasattr(self, '_maySeeOtherVehicleDamagedDevices'):
		self._maySeeOtherVehicleDamagedDevices = False
	return not _config_['commonAS']['expert']['enabled'] and self._maySeeOtherVehicleDamagedDevices

def new_PlayerAvatar_MSOVDD_setter(self, value):
	self._maySeeOtherVehicleDamagedDevices = value
	return

_inject_hooks_ += functools.partial(setattr, Avatar.PlayerAvatar, '_PlayerAvatar__maySeeOtherVehicleDamagedDevices', property(new_PlayerAvatar_MSOVDD_getter, new_PlayerAvatar_MSOVDD_setter))
