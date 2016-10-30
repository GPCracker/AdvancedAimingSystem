# *************************
# AvatarInputHandler Hooks
# *************************
@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.AvatarInputHandler, '__init__', calltype=XModLib.HookUtils.HookFunction.CALL_ORIGIN_BEFORE_HOOK)
def new_AvatarInputHandler_init(self, *args, **kwargs):
	config = _config_['commonAS']['targetScanner']
	self.XTargetScanner = TargetScanner(TargetScanMode(config['scanMode'])) if config['enabled'] else None
	config = _config_['gui']
	self.XGuiController = GuiController(_globals_['macrosFormatter'], config['updateInterval']) if config['enabled'] else None
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.AvatarInputHandler, 'handleKeyEvent')
def new_AvatarInputHandler_handleKeyEvent(self, event):
	getShortcut = XModLib.KeyBoard.Shortcut.fromSequence
	## HotKeys - Common
	if self.ctrlModeName in ['arcade', 'sniper', 'strategic']:
		## HotKeys - TargetScanner - ManualOverride
		config = _config_['commonAS']['targetScanner']['manualOverride']
		shortcutHandle = config['enabled'] and getShortcut(config['key'], True, False)(event)
		if shortcutHandle:
			if shortcutHandle.pushed:
				targetScanner = getattr(self, 'XTargetScanner', None)
				if targetScanner is not None:
					targetScanner.engageManualOverride()
	## HotKeys - Arcade
	if self.ctrlModeName == 'arcade':
		## HotKeys - AimCorrection - ManualMode
		config = _config_['arcadeAS']['aimCorrection']['manualMode']
		shortcutHandle = config['enabled'] and getShortcut(config['key'], False, False)(event)
		if shortcutHandle:
			self.ctrl.XAimCorrection.resetManualInfo()
			if shortcutHandle.pushed:
				self.ctrl.XAimCorrection.setManualInfo()
		## HotKeys - AimCorrection - Target Mode - Switch
		config = _config_['arcadeAS']['aimCorrection']['targetMode']
		shortcutHandle = config['enabled'] and getShortcut(
			config['shortcut']['key'],
			config['shortcut']['switch'],
			config['shortcut']['invert']
		)(event)
		if shortcutHandle and (not shortcutHandle.switch or shortcutHandle.pushed):
			config['activated'] = shortcutHandle(config['activated'])
			if shortcutHandle.switch and config['activated']:
				XModLib.Messages.Messenger.showMessageOnPanel(
					'Player',
					None,
					config['message']['onActivate'],
					'green'
				)
			elif shortcutHandle.switch:
				XModLib.Messages.Messenger.showMessageOnPanel(
					'Player',
					None,
					config['message']['onDeactivate'],
					'red'
				)
			self.ctrl.XAimCorrection.targetEnabled = config['activated']
		## HotKeys - SPG Sniper Mode
		config = _config_['commonAS']['sniperModeSPG']
		shortcutHandle = config['enabled'] and getShortcut(config['key'], True, False)(event)
		if shortcutHandle and XModLib.ArenaInfo.ArenaInfo.getClass(BigWorld.player().playerVehicleID) == 'SPG':
			if shortcutHandle.pushed:
				desiredShotPoint = self.ctrl.camera.aimingSystem.getDesiredShotPoint()
				self.onControlModeChanged(
					'sniper',
					preferredPos=desiredShotPoint,
					aimingMode=self.ctrl.aimingMode,
					saveZoom=True,
					equipmentID=None
				)
	## HotKeys - Sniper
	elif self.ctrlModeName == 'sniper':
		## HotKeys - AimCorrection - ManualMode
		config = _config_['sniperAS']['aimCorrection']['manualMode']
		shortcutHandle = config['enabled'] and getShortcut(config['key'], False, False)(event)
		if shortcutHandle:
			self.ctrl.XAimCorrection.resetManualInfo()
			if shortcutHandle.pushed:
				self.ctrl.XAimCorrection.setManualInfo()
		## HotKeys - AimCorrection - Target Mode - Switch
		config = _config_['sniperAS']['aimCorrection']['targetMode']
		shortcutHandle = config['enabled'] and getShortcut(
			config['shortcut']['key'],
			config['shortcut']['switch'],
			config['shortcut']['invert']
		)(event)
		if shortcutHandle and (not shortcutHandle.switch or shortcutHandle.pushed):
			config['activated'] = shortcutHandle(config['activated'])
			if shortcutHandle.switch and config['activated']:
				XModLib.Messages.Messenger.showMessageOnPanel(
					'Player',
					None,
					config['message']['onActivate'],
					'green'
				)
			elif shortcutHandle.switch:
				XModLib.Messages.Messenger.showMessageOnPanel(
					'Player',
					None,
					config['message']['onDeactivate'],
					'red'
				)
			self.ctrl.XAimCorrection.targetEnabled = config['activated']
		## HotKeys - SPG Sniper Mode
		config = _config_['commonAS']['sniperModeSPG']
		shortcutHandle = config['enabled'] and getShortcut(config['key'], True, False)(event)
		if shortcutHandle and XModLib.ArenaInfo.ArenaInfo.getClass(BigWorld.player().playerVehicleID) == 'SPG':
			if shortcutHandle.pushed:
				desiredShotPoint = self.ctrl.camera.aimingSystem.getDesiredShotPoint()
				self.onControlModeChanged(
					'arcade',
					preferredPos=desiredShotPoint,
					turretYaw=self.ctrl.camera.aimingSystem.turretYaw,
					gunPitch=self.ctrl.camera.aimingSystem.gunPitch,
					aimingMode=self.ctrl.aimingMode,
					closesDist=False
				)
	## HotKeys - Strategic
	elif self.ctrlModeName == 'strategic':
		## HotKeys - AimCorrection - ManualMode
		config = _config_['strategicAS']['aimCorrection']['manualMode']
		shortcutHandle = config['enabled'] and getShortcut(config['key'], False, False)(event)
		if shortcutHandle:
			self.ctrl.XAimCorrection.resetManualInfo()
			if shortcutHandle.pushed:
				self.ctrl.XAimCorrection.setManualInfo()
		## HotKeys - AimCorrection - Target Mode - Switch
		config = _config_['strategicAS']['aimCorrection']['targetMode']
		shortcutHandle = config['enabled'] and getShortcut(
			config['shortcut']['key'],
			config['shortcut']['switch'],
			config['shortcut']['invert']
		)(event)
		if shortcutHandle and (not shortcutHandle.switch or shortcutHandle.pushed):
			config['activated'] = shortcutHandle(config['activated'])
			if shortcutHandle.switch and config['activated']:
				XModLib.Messages.Messenger.showMessageOnPanel(
					'Player',
					None,
					config['message']['onActivate'],
					'green'
				)
			elif shortcutHandle.switch:
				XModLib.Messages.Messenger.showMessageOnPanel(
					'Player',
					None,
					config['message']['onDeactivate'],
					'red'
				)
			self.ctrl.XAimCorrection.targetEnabled = config['activated']
	return
