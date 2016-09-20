# *************************
# GuiLoaderViewMeta Class
# *************************
class GuiLoaderViewMeta(gui.Scaleform.framework.entities.View.View):
	def as_createBattlePageComponentS(self, componentAlias, componentClass, componentIndex):
		if self._isDAAPIInited():
			return self.flashObject.as_createBattlePageComponent(componentAlias, componentClass, componentIndex)
		return
