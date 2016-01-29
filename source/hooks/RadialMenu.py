# *************************
# RadialMenu Hooks
# *************************
@XModLib.HookUtils.HookFunction.propertyHookOnEvent(_inject_hooks_, gui.Scaleform.daapi.view.battle.RadialMenu.RadialMenu, '_RadialMenu__currentTarget', '_currentTarget', action=XModLib.HookUtils.HookFunction.PROPERTY_ACTION_GET, calltype=XModLib.HookUtils.HookFunction.CALL_ORIGIN_INSIDE_HOOK)
def new_RadialMenu_currentTarget_getter(old_RadialMenu_currentTarget_getter, self):
	try:
		result = old_RadialMenu_currentTarget_getter(self)
	except AttributeError:
		result = None
	return result

@XModLib.HookUtils.HookFunction.propertyHookOnEvent(_inject_hooks_, gui.Scaleform.daapi.view.battle.RadialMenu.RadialMenu, '_RadialMenu__currentTarget', '_currentTarget', action=XModLib.HookUtils.HookFunction.PROPERTY_ACTION_SET, calltype=XModLib.HookUtils.HookFunction.CALL_ORIGIN_INSIDE_HOOK)
def new_RadialMenu_currentTarget_setter(old_RadialMenu_currentTarget_setter, self, target):
	if target is None and _config_['commonAS']['radialMenu']['useXRay']:
		target = XModLib.XRayScanner.XRayScanner.getTarget()
	return old_RadialMenu_currentTarget_setter(self, target)
