# *************************
# AvatarInputHandler Hooks
# *************************
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.AvatarInputHandler, '__init__', invoke=XModLib.HookUtils.HookInvoke.SECONDARY)
def new_AvatarInputHandler_init(self, *args, **kwargs):
	config = _config_['commonAS']['targetScanner']
	self.XTargetScanner = TargetScanner(
		TargetScanMode(config['scanMode']),
		config['autoScan']['enabled'] and config['autoScan']['activated']
	) if config['enabled'] else None
	config = _config_['gui']
	self.XGuiController = GuiController(_globals_['macrosFormatter'], config['updateInterval']) if config['enabled'] else None
	return

@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.AvatarInputHandler, 'handleKeyEvent')
def new_AvatarInputHandler_handleKeyEvent(self, event):
	event = XModLib.KeyboardUtils.KeyboardEvent(event)
	## HotKeys - Common
	if self.ctrlModeName in ('arcade', 'sniper', 'strategic'):
		## HotKeys - TargetScanner
		config = _config_['commonAS']['targetScanner']
		if config['enabled']:
			## HotKeys - TargetScanner - AutoScan
			config = _config_['commonAS']['targetScanner']['autoScan']
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
			config = _config_['commonAS']['targetScanner']['manualOverride']
			shortcutHandle = config['enabled'] and config['shortcut'](event)
			if shortcutHandle and shortcutHandle.pushed:
				targetScanner = getattr(self, 'XTargetScanner', None)
				if targetScanner is not None:
					targetScanner.engageManualOverride()
	## HotKeys - Arcade
	if self.ctrlModeName == 'arcade':
		## HotKeys - AimCorrection
		config = _config_['arcadeAS']['aimCorrection']
		if True:
			## HotKeys - AimCorrection - ManualMode
			config = _config_['arcadeAS']['aimCorrection']['manualMode']
			shortcutHandle = config['enabled'] and config['shortcut'](event)
			if shortcutHandle:
				self.ctrl.XAimCorrection.resetManualInfo()
				if shortcutHandle.pushed:
					self.ctrl.XAimCorrection.setManualInfo()
			## HotKeys - AimCorrection - Target Mode
			config = _config_['arcadeAS']['aimCorrection']['targetMode']
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
		## HotKeys - SPG Sniper Mode
		config = _config_['commonAS']['sniperModeSPG']
		shortcutHandle = config['enabled'] and config['shortcut'](event)
		if shortcutHandle and XModLib.ArenaInfo.getClass(BigWorld.player().playerVehicleID) == 'SPG':
			if shortcutHandle.pushed:
				self.onControlModeChanged(
					'sniper',
					preferredPos=self.ctrl.camera.aimingSystem.getDesiredShotPoint(),
					aimingMode=self.ctrl.aimingMode,
					saveZoom=True,
					equipmentID=None
				)
	## HotKeys - Sniper
	elif self.ctrlModeName == 'sniper':
		## HotKeys - AimCorrection
		config = _config_['sniperAS']['aimCorrection']
		if True:
			## HotKeys - AimCorrection - ManualMode
			config = _config_['sniperAS']['aimCorrection']['manualMode']
			shortcutHandle = config['enabled'] and config['shortcut'](event)
			if shortcutHandle:
				self.ctrl.XAimCorrection.resetManualInfo()
				if shortcutHandle.pushed:
					self.ctrl.XAimCorrection.setManualInfo()
			## HotKeys - AimCorrection - Target Mode
			config = _config_['sniperAS']['aimCorrection']['targetMode']
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
		## HotKeys - SPG Sniper Mode
		config = _config_['commonAS']['sniperModeSPG']
		shortcutHandle = config['enabled'] and config['shortcut'](event)
		if shortcutHandle and XModLib.ArenaInfo.getClass(BigWorld.player().playerVehicleID) == 'SPG':
			if shortcutHandle.pushed:
				self.onControlModeChanged(
					'arcade',
					preferredPos=self.ctrl.camera.aimingSystem.getDesiredShotPoint(),
					turretYaw=self.ctrl.camera.aimingSystem.turretYaw,
					gunPitch=self.ctrl.camera.aimingSystem.gunPitch,
					aimingMode=self.ctrl.aimingMode,
					closesDist=False
				)
	## HotKeys - Strategic
	elif self.ctrlModeName == 'strategic':
		## HotKeys - AimCorrection
		config = _config_['strategicAS']['aimCorrection']
		if True:
			## HotKeys - AimCorrection - ManualMode
			config = _config_['strategicAS']['aimCorrection']['manualMode']
			shortcutHandle = config['enabled'] and config['shortcut'](event)
			if shortcutHandle:
				self.ctrl.XAimCorrection.resetManualInfo()
				if shortcutHandle.pushed:
					self.ctrl.XAimCorrection.setManualInfo()
			## HotKeys - AimCorrection - Target Mode
			config = _config_['strategicAS']['aimCorrection']['targetMode']
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
