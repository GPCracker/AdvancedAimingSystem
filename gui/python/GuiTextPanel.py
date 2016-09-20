# *************************
# GuiTextPanel Class
# *************************
class GuiTextPanel(GuiTextPanelMeta):
	def __init__(self, *args, **kwargs):
		super(GuiTextPanel, self).__init__(*args, **kwargs)
		self._config = {
			'alpha': 1.0,
			'visible': True,
			'background': '',
			'tooltip': '',
			'text': '',
			'position': (0.0, 0.0),
			'size': (100.0, 50.0)
		}
		return

	@property
	def config(self):
		return self._config

	@config.setter
	def config(self, value):
		self._config.update(value)
		self.as_applyConfigS({key: value[key] for key in value if key != 'text'})
		return

	def py_onPanelDrag(self, x, y):
		return

	def py_onPanelDrop(self, x, y):
		return

	def _populate(self):
		super(GuiTextPanel, self)._populate()
		gui.shared.g_eventBus.addListener(gui.shared.events.GameEvent.SHOW_CURSOR, self._handleShowCursor, gui.shared.EVENT_BUS_SCOPE.GLOBAL)
		gui.shared.g_eventBus.addListener(gui.shared.events.GameEvent.HIDE_CURSOR, self._handleHideCursor, gui.shared.EVENT_BUS_SCOPE.GLOBAL)
		return

	def _dispose(self):
		gui.shared.g_eventBus.removeListener(gui.shared.events.GameEvent.SHOW_CURSOR, self._handleShowCursor, gui.shared.EVENT_BUS_SCOPE.GLOBAL)
		gui.shared.g_eventBus.removeListener(gui.shared.events.GameEvent.HIDE_CURSOR, self._handleHideCursor, gui.shared.EVENT_BUS_SCOPE.GLOBAL)
		super(GuiTextPanel, self)._dispose()
		return

	def _handleShowCursor(self, _):
		self.as_toggleCursorS(True)
		return

	def _handleHideCursor(self, _):
		self.as_toggleCursorS(False)
		return

	def updateText(self, text):
		self.as_setTextS(text)
		return
