# *************************
# Vehicle Hooks
# *************************
@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, Vehicle.Vehicle, 'showDamageFromShot', calltype=XModLib.HookUtils.HookFunction.CALL_ORIGIN_BEFORE_HOOK)
def new_Vehicle_showDamageFromShot(self, attackerID, *args, **kwargs):
	if _config_['commonAS']['expert']['enabled']:
		player = BigWorld.player()
		if hasattr(player, 'XExpertPerk') and player.XExpertPerk is not None and self.publicInfo['team'] is not player.team:
			if attackerID == player.playerVehicleID:
				player.XExpertPerk.enqueue(self.id, True)
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, Vehicle.Vehicle, 'showDamageFromExplosion', calltype=XModLib.HookUtils.HookFunction.CALL_ORIGIN_BEFORE_HOOK)
def new_Vehicle_showDamageFromExplosion(self, attackerID, *args, **kwargs):
	if _config_['commonAS']['expert']['enabled']:
		player = BigWorld.player()
		if hasattr(player, 'XExpertPerk') and player.XExpertPerk is not None and self.publicInfo['team'] is not player.team:
			if attackerID == player.playerVehicleID:
				player.XExpertPerk.enqueue(self.id, True)
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, Vehicle.Vehicle, 'startVisual', calltype=XModLib.HookUtils.HookFunction.CALL_ORIGIN_BEFORE_HOOK)
def new_Vehicle_startVisual(self, *args, **kwargs):
	if _config_['commonAS']['expert']['enabled']:
		player = BigWorld.player()
		if hasattr(player, 'XExpertPerk') and player.XExpertPerk is not None and self.publicInfo['team'] is not player.team:
			pass
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, Vehicle.Vehicle, 'stopVisual', calltype=XModLib.HookUtils.HookFunction.CALL_HOOK_BEFORE_ORIGIN)
def new_Vehicle_stopVisual(self, *args, **kwargs):
	if _config_['commonAS']['expert']['enabled']:
		player = BigWorld.player()
		if hasattr(player, 'XExpertPerk') and player.XExpertPerk is not None and self.publicInfo['team'] is not player.team:
			player.XExpertPerk.cancel(self.id)
	return
