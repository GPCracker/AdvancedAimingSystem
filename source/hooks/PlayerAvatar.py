# *************************
# PlayerAvatar Hooks
# *************************
@XModLib.HookUtils.methodHookExt(_inject_hooks_, Avatar.PlayerAvatar, 'updateVehicleMiscStatus')
def new_PlayerAvatar_updateVehicleMiscStatus(self, vehicleID, code, intArg, floatArg):
	if vehicleID == self.playerVehicleID and code == constants.VEHICLE_MISC_STATUS.OTHER_VEHICLE_DAMAGED_DEVICES_VISIBLE:
		if intArg and not hasattr(self, 'XExpertPerk'):
			config = _config_['commonAS']['expertPerk']
			self.XExpertPerk = ExpertPerk(
				lambda: getattr(BigWorld.player(), '_maySeeOtherVehicleDamagedDevices', False),
				config['cacheExtrasInfo'],
				config['replyTimeout'],
				config['cacheExpiryTime']
			) if config['enabled'] else None
	return

@XModLib.HookUtils.methodHookExt(_inject_hooks_, Avatar.PlayerAvatar, 'showOtherVehicleDamagedDevices')
def new_PlayerAvatar_showOtherVehicleDamagedDevices(self, vehicleID, damagedExtras, destroyedExtras):
	expertPerk = getattr(self, 'XExpertPerk', None)
	if expertPerk is not None and getattr(self, '_maySeeOtherVehicleDamagedDevices', False):
		expertPerk.onExtrasInfoReceived(vehicleID, (damagedExtras, destroyedExtras))
		target = BigWorld.target()
		if XModLib.VehicleInfo.isVehicle(target) and target.id == vehicleID:
			self.guiSessionProvider.shared.feedback.showVehicleDamagedDevices(vehicleID, damagedExtras, destroyedExtras)
	return

@XModLib.HookUtils.methodHookExt(_inject_hooks_, Avatar.PlayerAvatar, 'targetBlur')
def new_PlayerAvatar_targetBlur(self, prevEntity):
	expertPerk = getattr(self, 'XExpertPerk', None)
	if expertPerk is not None and getattr(self, '_maySeeOtherVehicleDamagedDevices', False):
		if XModLib.VehicleInfo.isVehicle(prevEntity):
			self.guiSessionProvider.shared.feedback.hideVehicleDamagedDevices()
	return

@XModLib.HookUtils.methodHookExt(_inject_hooks_, Avatar.PlayerAvatar, 'targetFocus')
def new_PlayerAvatar_targetFocus(self, entity):
	expertPerk = getattr(self, 'XExpertPerk', None)
	if expertPerk is not None and getattr(self, '_maySeeOtherVehicleDamagedDevices', False):
		if XModLib.VehicleInfo.isVehicle(entity) and entity.publicInfo['team'] is not self.team and entity.isAlive():
			expertPerk.request(entity.id)
			cacheEntry = expertPerk.extrasInfoCache.get(entity.id, None)
			if cacheEntry is not None and not cacheEntry.isExpired:
				self.guiSessionProvider.shared.feedback.showVehicleDamagedDevices(entity.id, *cacheEntry.extrasInfo)
	return

@XModLib.HookUtils.methodHookExt(_inject_hooks_, Avatar.PlayerAvatar, 'autoAim')
def new_PlayerAvatar_autoAim(self, target):
	expertPerk = getattr(self, 'XExpertPerk', None)
	if expertPerk is not None and getattr(self, '_maySeeOtherVehicleDamagedDevices', False):
		if XModLib.VehicleInfo.isVehicle(target) and target.publicInfo['team'] is not self.team and target.isAlive():
			expertPerk.request(target.id)
	return

@XModLib.HookUtils.propertyHookExt(_inject_hooks_, Avatar.PlayerAvatar, '_PlayerAvatar__maySeeOtherVehicleDamagedDevices', XModLib.HookUtils.PropertyAction.GET, '_maySeeOtherVehicleDamagedDevices', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_PlayerAvatar_MSOVDD_getter(old_PlayerAvatar_MSOVDD_getter, self):
	try:
		result = old_PlayerAvatar_MSOVDD_getter(self)
	except AttributeError:
		result = False
	return result and getattr(self, 'XExpertPerk', None) is None
