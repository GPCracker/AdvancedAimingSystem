# *************************
# AvatarInputHandler Hooks
# *************************
@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.AvatarInputHandler, 'handleKeyEvent')
def new_AvatarInputHandler_handleKeyEvent(self, event):
	getShortcut = XModLib.KeyBoard.Shortcut.fromSequence
	## HotKeys - Common
	if self.ctrlModeName in ['arcade', 'sniper', 'strategic']:
		config0 = _config_['commonAS']['safeShot']
		## HotKeys - SafeShot
		shortcutHandle = config0['enabled'] and getShortcut(config0['key'], config0['switch'], config0['invert'])(event)
		if shortcutHandle and (not shortcutHandle.switch or shortcutHandle.pushed):
			config0['activated'] = shortcutHandle(config0['activated'])
			if config0['switch'] and config0['activated']:
				XModLib.Messages.Messenger.showMessageOnPanel('PlayerMessagesPanel', 0, config0['onActivate'], 'green')
			elif config0['switch']:
				XModLib.Messages.Messenger.showMessageOnPanel('PlayerMessagesPanel', 0, config0['onDeactivate'], 'red')
	## HotKeys - Arcade
	if self.ctrlModeName == 'arcade':
		config0 = _config_['arcadeAS']['aimCorrection']['manualMode']
		config1 = _config_['arcadeAS']['targetLock']['manualMode']
		config2 = _config_['commonAS']['sniperModeSPG']
		config3 = _config_['arcadeAS']['aimingInfo']
		## HotKeys - AimCorrection - ManualMode
		shortcutHandle = config0['enabled'] and getShortcut(config0['key'], False, False)(event)
		if shortcutHandle:
			if shortcutHandle.pushed:
				pass
		## HotKeys - TargetLock - ManualMode
		shortcutHandle = config1['enabled'] and getShortcut(config1['key'], True, False)(event)
		if shortcutHandle:
			if shortcutHandle.pushed:
				target = BigWorld.target()
				target = target if XModLib.VehicleInfo.VehicleInfo.isVehicle(target) else None
				if target is None and config1['useXRay']:
					target = XModLib.XRayScanner.XRayScanner.getTarget()
				self.XTargetInfo = TargetInfo(target, None) if target is not None else None
		## HotKeys - SPG Sniper Mode
		shortcutHandle = config2['enabled'] and getShortcut(config2['key'], True, False)(event)
		if shortcutHandle:
			if shortcutHandle.pushed and XModLib.ArenaInfo.ArenaInfo.getClass(BigWorld.player().playerVehicleID) == 'SPG':
				desiredShotPoint = self.ctrl.camera.aimingSystem.getDesiredShotPoint()
				self.onControlModeChanged('sniper', preferredPos=desiredShotPoint, aimingMode=self.ctrl.aimingMode, saveZoom=True, equipmentID=None)
		## HotKeys - AimingInfo
		shortcutHandle = config3['enabled'] and getShortcut(config3['key'], config3['switch'], config3['invert'])(event)
		if shortcutHandle and (not shortcutHandle.switch or shortcutHandle.pushed):
			config3['activated'] = shortcutHandle(config3['activated'])
			if hasattr(self.ctrl, 'XAimingInfo') and self.ctrl.XAimingInfo is not None:
				self.ctrl.XAimingInfo.window.gui.visible = config3['activated'] and BigWorld.player().isGuiVisible
	## HotKeys - Sniper
	elif self.ctrlModeName == 'sniper':
		config0 = _config_['sniperAS']['aimCorrection']['manualMode']
		config1 = _config_['sniperAS']['targetLock']['manualMode']
		config2 = _config_['commonAS']['sniperModeSPG']
		config3 = _config_['sniperAS']['aimingInfo']
		## HotKeys - AimCorrection - ManualMode
		shortcutHandle = config0['enabled'] and getShortcut(config0['key'], False, False)(event)
		if shortcutHandle:
			self.ctrl.XLockedDistance = None
			if shortcutHandle.pushed:
				cameraRay, cameraPoint = AvatarInputHandler.cameras.getWorldRayAndPoint(*self.ctrl.getAim().offset())
				shotPoint = self.ctrl.getDesiredShotPoint()
				if shotPoint is not None:
					self.ctrl.XLockedDistance = (shotPoint - cameraPoint).length
		## HotKeys - TargetLock - ManualMode
		shortcutHandle = config1['enabled'] and getShortcut(config1['key'], True, False)(event)
		if shortcutHandle:
			if shortcutHandle.pushed:
				target = BigWorld.target()
				target = target if XModLib.VehicleInfo.VehicleInfo.isVehicle(target) else None
				if target is None and config1['useXRay']:
					target = XModLib.XRayScanner.XRayScanner.getTarget()
				self.XTargetInfo = TargetInfo(target, None) if target is not None else None
		## HotKeys - SPG Sniper Mode
		shortcutHandle = config2['enabled'] and getShortcut(config2['key'], True, False)(event)
		if shortcutHandle:
			if shortcutHandle.pushed and XModLib.ArenaInfo.ArenaInfo.getClass(BigWorld.player().playerVehicleID) == 'SPG':
				desiredShotPoint = self.ctrl.camera.aimingSystem.getDesiredShotPoint()
				self.onControlModeChanged('arcade', preferredPos=desiredShotPoint, turretYaw=self.ctrl.camera.aimingSystem.turretYaw, gunPitch=self.ctrl.camera.aimingSystem.gunPitch, aimingMode=self.ctrl.aimingMode, closesDist=False)
		## HotKeys - AimingInfo
		shortcutHandle = config3['enabled'] and getShortcut(config3['key'], config3['switch'], config3['invert'])(event)
		if shortcutHandle and (not shortcutHandle.switch or shortcutHandle.pushed):
			config3['activated'] = shortcutHandle(config3['activated'])
			if hasattr(self.ctrl, 'XAimingInfo') and self.ctrl.XAimingInfo is not None:
				self.ctrl.XAimingInfo.window.gui.visible = config3['activated'] and BigWorld.player().isGuiVisible
	## HotKeys - Strategic
	elif self.ctrlModeName == 'strategic':
		config0 = _config_['strategicAS']['aimCorrection']['manualMode']
		config1 = _config_['strategicAS']['targetLock']['manualMode']
		config2 = _config_['strategicAS']['aimCorrection']['relativeMode']
		config3 = _config_['strategicAS']['aimingInfo']
		config4 = _config_['strategicAS']['strategicSniper']
		config5 = _config_['strategicAS']['strategicSniper']['basePitch']['adjustment']
		## HotKeys - AimCorrection - ManualMode
		shortcutHandle = config0['enabled'] and getShortcut(config0['key'], False, False)(event)
		if shortcutHandle:
			self.ctrl.XLockedHeight = None
			if shortcutHandle.pushed:
				shotPoint = self.ctrl.getDesiredShotPoint()
				if shotPoint is not None:
					self.ctrl.XLockedHeight = shotPoint.y
		## HotKeys - TargetLock - ManualMode
		shortcutHandle = config1['enabled'] and getShortcut(config1['key'], True, False)(event)
		if shortcutHandle:
			if shortcutHandle.pushed:
				target = BigWorld.target()
				target = target if XModLib.VehicleInfo.VehicleInfo.isVehicle(target) else None
				if target is None and config1['useXRay']:
					target = XModLib.XRayScanner.XRayScanner.getTarget()
				self.XTargetInfo = TargetInfo(target, None) if target is not None else None
		## HotKeys - AimCorrection - Relative Mode - Switch
		shortcutHandle = config2['enabled'] and getShortcut(config2['key'], config2['switch'], config2['invert'])(event)
		if shortcutHandle and (not shortcutHandle.switch or shortcutHandle.pushed):
			config2['activated'] = shortcutHandle(config2['activated'])
			if config2['switch'] and config2['activated']:
				XModLib.Messages.Messenger.showMessageOnPanel('PlayerMessagesPanel', 0, config2['onActivate'], 'green')
			elif config2['switch']:
				XModLib.Messages.Messenger.showMessageOnPanel('PlayerMessagesPanel', 0, config2['onDeactivate'], 'red')
		## HotKeys - AimingInfo
		shortcutHandle = config3['enabled'] and getShortcut(config3['key'], config3['switch'], config3['invert'])(event)
		if shortcutHandle and (not shortcutHandle.switch or shortcutHandle.pushed):
			config3['activated'] = shortcutHandle(config3['activated'])
			if hasattr(self.ctrl, 'XAimingInfo') and self.ctrl.XAimingInfo is not None:
				self.ctrl.XAimingInfo.window.gui.visible = config3['activated'] and BigWorld.player().isGuiVisible
		## HotKeys - Strategic Sniper - Switch
		shortcutHandle = config4['enabled'] and getShortcut(config4['key'], config4['switch'], config4['invert'])(event)
		if shortcutHandle and (not shortcutHandle.switch or shortcutHandle.pushed):
			config4['activated'] = shortcutHandle(config4['activated'])
			self.ctrl.camera.XSwitchMode(config4['activated'])
		## HotKeys - Strategic Sniper - Base Pitch - Increase
		shortcutHandle = config5['enabled'] and getShortcut(config5['increase'], True, False)(event)
		if shortcutHandle:
			if shortcutHandle.pushed:
				result = self.ctrl.camera.XIncreaseCameraBasePitch()
				if result is not None and result[1] and config5['message']['enabled']:
					message = _globals_['macrosFormatter'](config5['message']['template'], value=result[0], delta=result[1])
					XModLib.Messages.Messenger.showMessageOnPanel('PlayerMessagesPanel', 0, message, 'green')
		## HotKeys - Strategic Sniper - Base Pitch - Decrease
		shortcutHandle = config5['enabled'] and getShortcut(config5['decrease'], True, False)(event)
		if shortcutHandle:
			if shortcutHandle.pushed:
				result = self.ctrl.camera.XDecreaseCameraBasePitch()
				if result is not None and result[1] and config5['message']['enabled']:
					message = _globals_['macrosFormatter'](config5['message']['template'], value=result[0], delta=result[1])
					XModLib.Messages.Messenger.showMessageOnPanel('PlayerMessagesPanel', 0, message, 'red')
	return
