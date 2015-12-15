# *************************
# RadialMenu Hooks
# *************************
def new_RadialMenu_currentTarget_getter(self):
	if not hasattr(self, '_currentTarget'):
		self._currentTarget = None
	return self._currentTarget

def new_RadialMenu_currentTarget_setter(self, target):
	if target is None and _config_['commonAS']['radialMenu']['useXRay']:
		target = XModLib.XRayScanner.XRayScanner.getTarget()
	self._currentTarget = target
	return

_inject_hooks_ += functools.partial(setattr, gui.Scaleform.daapi.view.battle.RadialMenu.RadialMenu, '_RadialMenu__currentTarget', property(new_RadialMenu_currentTarget_getter, new_RadialMenu_currentTarget_setter))
