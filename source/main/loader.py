# *************************
# Application loader
# *************************
@XModLib.HookUtils.HookFunction.staticMethodHookOnEvent(_inject_inits_, gui.shared.personality, 'start', calltype=XModLib.HookUtils.HookFunction.CALL_HOOK_BEFORE_ORIGIN)
def new_Personality_start(*args, **kwargs):
	_inject_chain_()
	return
