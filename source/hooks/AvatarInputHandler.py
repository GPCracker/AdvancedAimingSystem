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

@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.AvatarInputHandler, 'handleKeyEvent', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_AvatarInputHandler_handleKeyEvent(old_AvatarInputHandler_handleKeyEvent, self, event):
	result = old_AvatarInputHandler_handleKeyEvent(self, event)
	## Keyboard event parsing
	kbevent = XModLib.KeyboardUtils.KeyboardEvent(event)
	## Operating control modes
	operatingControlModes = (
		AvatarInputHandler.aih_constants.CTRL_MODE_NAME.ARCADE,
		AvatarInputHandler.aih_constants.CTRL_MODE_NAME.SNIPER,
		AvatarInputHandler.aih_constants.CTRL_MODE_NAME.STRATEGIC,
		AvatarInputHandler.aih_constants.CTRL_MODE_NAME.ARTY
	)
	## AvatarInputHandler started, control mode supported, event not handled by game (for AvatarInputHandler switches)
	if self._AvatarInputHandler__isStarted and self.ctrlModeName in operatingControlModes and not result:
		## HotKeys - TargetScanner
		mconfig = _config_['modules']['targetScanner']
		if mconfig['enabled']:
			## HotKeys - TargetScanner - AutoScan
			fconfig = mconfig['autoScan']
			shortcutHandle = fconfig['enabled'] and fconfig['shortcut'](kbevent)
			if shortcutHandle and (not shortcutHandle.switch or shortcutHandle.pushed):
				fconfig['activated'] = shortcutHandle(fconfig['activated'])
				if shortcutHandle.switch and fconfig['activated']:
					XModLib.ClientMessages.showMessageOnPanel(
						'Player',
						None,
						fconfig['message']['onActivate'],
						'green'
					)
				elif shortcutHandle.switch:
					XModLib.ClientMessages.showMessageOnPanel(
						'Player',
						None,
						fconfig['message']['onDeactivate'],
						'red'
					)
				targetScanner = getattr(self, 'XTargetScanner', None)
				if targetScanner is not None:
					targetScanner.autoScanActivated = fconfig['activated']
			## HotKeys - TargetScanner - ManualOverride
			fconfig = mconfig['manualOverride']
			shortcutHandle = fconfig['enabled'] and fconfig['shortcut'](kbevent)
			if shortcutHandle and shortcutHandle.pushed:
				targetScanner = getattr(self, 'XTargetScanner', None)
				if targetScanner is not None:
					targetScanner.engageManualOverride()
		## HotKeys - AimCorrection
		mconfig = _config_['modules']['aimCorrection'][self.ctrlModeName]
		if mconfig['enabled']:
			## HotKeys - AimCorrection - Target Mode
			fconfig = mconfig['targetMode']
			shortcutHandle = fconfig['enabled'] and fconfig['shortcut'](kbevent)
			if shortcutHandle and (not shortcutHandle.switch or shortcutHandle.pushed):
				fconfig['activated'] = shortcutHandle(fconfig['activated'])
				if shortcutHandle.switch and fconfig['activated']:
					XModLib.ClientMessages.showMessageOnPanel(
						'Player',
						None,
						fconfig['message']['onActivate'],
						'green'
					)
				elif shortcutHandle.switch:
					XModLib.ClientMessages.showMessageOnPanel(
						'Player',
						None,
						fconfig['message']['onDeactivate'],
						'red'
					)
				aimCorrection = getattr(self.ctrl, 'XAimCorrection', None)
				if aimCorrection is not None:
					aimCorrection.targetEnabled = fconfig['activated']
	## AvatarInputHandler started, not detached, control mode supported (for AvatarInputHandler shortcuts)
	if self._AvatarInputHandler__isStarted and not self.isDetached and self.ctrlModeName in operatingControlModes:
		## HotKeys - AimCorrection
		mconfig = _config_['modules']['aimCorrection'][self.ctrlModeName]
		if mconfig['enabled']:
			## HotKeys - AimCorrection - ManualMode
			fconfig = mconfig['manualMode']
			shortcutHandle = fconfig['enabled'] and fconfig['shortcut'](kbevent)
			if shortcutHandle:
				aimCorrection = getattr(self.ctrl, 'XAimCorrection', None)
				if aimCorrection is not None:
					aimCorrection.updateManualInfo(shortcutHandle.pushed)
	## AvatarInputHandler started, event not handled by game (for avatar switches)
	if self._AvatarInputHandler__isStarted and not result:
		pass
	## AvatarInputHandler started (for avatar shortcuts)
	if self._AvatarInputHandler__isStarted:
		pass
	return result
