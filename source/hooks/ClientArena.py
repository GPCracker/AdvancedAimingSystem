# *************************
# ClientArena Hooks
# *************************
@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, ClientArena.ClientArena, 'collideWithSpaceBB', calltype=XModLib.HookUtils.HookFunction.CALL_ORIGIN_INSIDE_HOOK)
def new_ClientArena_collideWithSpaceBB(old_ClientArena_collideWithSpaceBB, self, start, end):
	return old_ClientArena_collideWithSpaceBB(self, start, end)
