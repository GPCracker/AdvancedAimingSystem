# *************************
# Hooks injector chain
# *************************
class InjectorChain(list):
	def __call__(self, *args, **kwargs):
		return [injector(*args, **kwargs) for injector in self]

# *************************
# Hooks injector events
# *************************
_inject_inits_ = XModLib.HookUtils.HookEvent()
_inject_loads_ = XModLib.HookUtils.HookEvent()
_inject_hooks_ = XModLib.HookUtils.HookEvent()
_inject_chain_ = InjectorChain()
