# *************************
# Vehicle Hooks
# *************************
@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, Vehicle.Vehicle, 'showDamageFromShot')
def new_Vehicle_showDamageFromShot(self, attackerID, *args, **kwargs):
	if _config_['commonAS']['expert']['enabled']:
		player = BigWorld.player()
		if hasattr(player, 'XExpertPerk') and player.XExpertPerk is not None and self.publicInfo['team'] is not player.team:
			if attackerID == player.playerVehicleID:
				player.XExpertPerk.enqueue(self.id, True)
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, Vehicle.Vehicle, 'showDamageFromExplosion')
def new_Vehicle_showDamageFromExplosion(self, attackerID, *args, **kwargs):
	if _config_['commonAS']['expert']['enabled']:
		player = BigWorld.player()
		if hasattr(player, 'XExpertPerk') and player.XExpertPerk is not None and self.publicInfo['team'] is not player.team:
			if attackerID == player.playerVehicleID:
				player.XExpertPerk.enqueue(self.id, True)
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, Vehicle.Vehicle, 'startVisual')
def new_Vehicle_startVisual(self, *args, **kwargs):
	if _config_['commonAS']['expert']['enabled']:
		player = BigWorld.player()
		if hasattr(player, 'XExpertPerk') and player.XExpertPerk is not None and self.publicInfo['team'] is not player.team:
			pass
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, Vehicle.Vehicle, 'stopVisual')
def new_Vehicle_stopVisual(self, *args, **kwargs):
	if _config_['commonAS']['expert']['enabled']:
		player = BigWorld.player()
		if hasattr(player, 'XExpertPerk') and player.XExpertPerk is not None and self.publicInfo['team'] is not player.team:
			player.XExpertPerk.cancel(self.id)
	return
