# ------------------- #
#    Vehicle Hooks    #
# ------------------- #
@XModLib.HookUtils.methodHookExt(_inject_hooks_, Vehicle.Vehicle, 'startVisual', invoke=XModLib.HookUtils.HookInvoke.SECONDARY)
def new_Vehicle_startVisual(self, *args, **kwargs):
	if not hasattr(self, 'collisionBounds'):
		setattr(self, 'collisionBounds', XModLib.VehicleBounds.getVehicleBoundsMatrixProvider(self))
	return

@XModLib.HookUtils.methodHookExt(_inject_hooks_, Vehicle.Vehicle, 'stopVisual', invoke=XModLib.HookUtils.HookInvoke.PRIMARY)
def new_Vehicle_stopVisual(self, *args, **kwargs):
	if hasattr(self, 'collisionBounds'):
		delattr(self, 'collisionBounds')
	return

@XModLib.HookUtils.methodHookExt(_inject_hooks_, Vehicle.Vehicle, '_Vehicle__onVehicleDeath')
def new_Vehicle_onVehicleDeath(self, isDeadStarted=False):
	targetScanner = getattr(BigWorld.player().inputHandler, 'XTargetScanner', None)
	if targetScanner is not None:
		targetScanner.handleVehicleDeath(self)
	return
