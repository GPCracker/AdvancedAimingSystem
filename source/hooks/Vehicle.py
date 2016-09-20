# *************************
# Vehicle Hooks
# *************************
@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, Vehicle.Vehicle, 'startVisual', calltype=XModLib.HookUtils.HookFunction.CALL_ORIGIN_BEFORE_HOOK)
def new_Vehicle_startVisual(self, *args, **kwargs):
	if not hasattr(self, 'collisionBounds'):
		setattr(self, 'collisionBounds', XModLib.VehicleBounds.VehicleBounds.getVehicleBoundsMatrixProvider(self))
	expertPerk = getattr(BigWorld.player(), 'XExpertPerk', None)
	if expertPerk is not None and self.publicInfo['team'] is not BigWorld.player().team:
		pass
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, Vehicle.Vehicle, 'stopVisual', calltype=XModLib.HookUtils.HookFunction.CALL_HOOK_BEFORE_ORIGIN)
def new_Vehicle_stopVisual(self, *args, **kwargs):
	expertPerk = getattr(BigWorld.player(), 'XExpertPerk', None)
	if expertPerk is not None and self.publicInfo['team'] is not BigWorld.player().team:
		expertPerk.cancel(self.id)
	if hasattr(self, 'collisionBounds'):
		delattr(self, 'collisionBounds')
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, Vehicle.Vehicle, '_Vehicle__onVehicleDeath')
def new_Vehicle_onVehicleDeath(self, isDeadStarted=False):
	expertPerk = getattr(BigWorld.player(), 'XExpertPerk', None)
	if expertPerk is not None and self.publicInfo['team'] is not BigWorld.player().team:
		expertPerk.cancel(self.id)
	targetScanner = getattr(BigWorld.player().inputHandler, 'XTargetScanner', None)
	if targetScanner is not None:
		targetScanner.handleVehicleDeath(self)
	return
