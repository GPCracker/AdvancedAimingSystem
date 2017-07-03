# *************************
# AvatarInputHandler Hooks
# *************************
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.AvatarInputHandler, '__init__', invoke=XModLib.HookUtils.HookInvoke.SECONDARY)
def new_AvatarInputHandler_init(self, *args, **kwargs):
	config = _config_['modules']['targetScanner']
	self.XTargetScanner = TargetScanner(
		TargetScanMode(**config['scanMode']),
		config['autoScan']['enabled'] and config['autoScan']['activated']
	) if config['enabled'] else None
	config = _config_['gui']
	self.XGuiController = GuiController(_globals_['macrosFormatter'], config['updateInterval']) if config['enabled'] else None
	return

@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.AvatarInputHandler, 'handleKeyEvent')
def new_AvatarInputHandler_handleKeyEvent(self, event):
	if not self._AvatarInputHandler__isStarted or self.isDetached:
		return
	## Keyboard event parsing
	event = XModLib.KeyboardUtils.KeyboardEvent(event)
	## HotKeys - Common
	if self.ctrlModeName in (AvatarInputHandler.aih_constants.CTRL_MODE_NAME.ARCADE, AvatarInputHandler.aih_constants.CTRL_MODE_NAME.SNIPER, AvatarInputHandler.aih_constants.CTRL_MODE_NAME.STRATEGIC, AvatarInputHandler.aih_constants.CTRL_MODE_NAME.ARTY):
		## HotKeys - TargetScanner
		config = _config_['modules']['targetScanner']
		if config['enabled']:
			## HotKeys - TargetScanner - AutoScan
			config = _config_['modules']['targetScanner']['autoScan']
			shortcutHandle = config['enabled'] and config['shortcut'](event)
			if shortcutHandle and (not shortcutHandle.switch or shortcutHandle.pushed):
				config['activated'] = shortcutHandle(config['activated'])
				if shortcutHandle.switch and config['activated']:
					XModLib.ClientMessages.showMessageOnPanel(
						'Player',
						None,
						config['message']['onActivate'],
						'green'
					)
				elif shortcutHandle.switch:
					XModLib.ClientMessages.showMessageOnPanel(
						'Player',
						None,
						config['message']['onDeactivate'],
						'red'
					)
				targetScanner = getattr(self, 'XTargetScanner', None)
				if targetScanner is not None:
					targetScanner.autoScanActivated = config['activated']
			## HotKeys - TargetScanner - ManualOverride
			config = _config_['modules']['targetScanner']['manualOverride']
			shortcutHandle = config['enabled'] and config['shortcut'](event)
			if shortcutHandle and shortcutHandle.pushed:
				targetScanner = getattr(self, 'XTargetScanner', None)
				if targetScanner is not None:
					targetScanner.engageManualOverride()
	## HotKeys - Operating
	if self.ctrlModeName in (AvatarInputHandler.aih_constants.CTRL_MODE_NAME.ARCADE, AvatarInputHandler.aih_constants.CTRL_MODE_NAME.SNIPER, AvatarInputHandler.aih_constants.CTRL_MODE_NAME.STRATEGIC, AvatarInputHandler.aih_constants.CTRL_MODE_NAME.ARTY):
		## HotKeys - AimCorrection
		config = _config_['modules']['aimCorrection'][self.ctrlModeName]
		if True:
			## HotKeys - AimCorrection - ManualMode
			config = _config_['modules']['aimCorrection'][self.ctrlModeName]['manualMode']
			shortcutHandle = config['enabled'] and config['shortcut'](event)
			if shortcutHandle:
				self.ctrl.XAimCorrection.resetManualInfo()
				if shortcutHandle.pushed:
					self.ctrl.XAimCorrection.setManualInfo()
			## HotKeys - AimCorrection - Target Mode
			config = _config_['modules']['aimCorrection'][self.ctrlModeName]['targetMode']
			shortcutHandle = config['enabled'] and config['shortcut'](event)
			if shortcutHandle and (not shortcutHandle.switch or shortcutHandle.pushed):
				config['activated'] = shortcutHandle(config['activated'])
				if shortcutHandle.switch and config['activated']:
					XModLib.ClientMessages.showMessageOnPanel(
						'Player',
						None,
						config['message']['onActivate'],
						'green'
					)
				elif shortcutHandle.switch:
					XModLib.ClientMessages.showMessageOnPanel(
						'Player',
						None,
						config['message']['onDeactivate'],
						'red'
					)
				self.ctrl.XAimCorrection.targetEnabled = config['activated']
	return
