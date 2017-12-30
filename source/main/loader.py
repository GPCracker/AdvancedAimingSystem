# ------------------------ #
#    Application loader    #
# ------------------------ #
@XModLib.HookUtils.staticMethodHookExt(_inject_inits_, gui.shared.personality, 'start', invoke=XModLib.HookUtils.HookInvoke.PRIMARY)
def new_Personality_start(*args, **kwargs):
	_inject_chain_()
	return
