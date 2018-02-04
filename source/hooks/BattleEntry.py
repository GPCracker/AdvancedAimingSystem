# ----------------------- #
#    BattleEntry Hooks    #
# ----------------------- #
@XModLib.HookUtils.methodHookExt(g_inject_hooks, gui.Scaleform.battle_entry.BattleEntry, '_getRequiredLibraries', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_BattleEntry_getRequiredLibraries(old_BattleEntry_getRequiredLibraries, self, *args, **kwargs):
	return old_BattleEntry_getRequiredLibraries(self, *args, **kwargs) + ('{0[1]}.swf'.format(__application__), )
