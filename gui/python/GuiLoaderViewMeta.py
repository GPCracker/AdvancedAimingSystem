# *************************
# GuiLoaderViewMeta Class
# *************************
class GuiLoaderViewMeta(gui.Scaleform.framework.entities.View.View):
	def as_createBattlePagePanelS(self, panelAlias, panelClass, panelIndex):
		if self._isDAAPIInited():
			return self.flashObject.as_createBattlePagePanel(panelAlias, panelClass, panelIndex)
		return
