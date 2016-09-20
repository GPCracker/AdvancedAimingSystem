# *************************
# GuiSettings Class
# *************************
class GuiSettings(object):
	@staticmethod
	def getViewSettings(viewAlias, viewClass, viewSwf):
		return gui.Scaleform.framework.ViewSettings(viewAlias, viewClass, viewSwf, gui.Scaleform.framework.ViewTypes.WINDOW, None, gui.Scaleform.framework.ScopeTemplates.DEFAULT_SCOPE)

	@staticmethod
	def getComponentSettings(componentAlias, componentClass):
		return gui.Scaleform.framework.ViewSettings(componentAlias, componentClass, None, gui.Scaleform.framework.ViewTypes.COMPONENT, None, gui.Scaleform.framework.ScopeTemplates.DEFAULT_SCOPE)
