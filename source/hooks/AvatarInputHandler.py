# *************************
# AvatarInputHandler Hooks
# *************************
@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.AvatarInputHandler, 'handleKeyEvent')
def new_AvatarInputHandler_handleKeyEvent(self, event):
	parseSequence = XModLib.KeyBoard.KeyBoard.parseSequence
	key, isDown, isRepeat, modifiers = XModLib.KeyBoard.KeyBoard.parseEvent(event)
	if isRepeat:
		return
	## HotKeys - Common
	if self.ctrlModeName in ['arcade', 'sniper', 'strategic']:
		config0 = _config_['commonAS']['safeShot']
		## HotKeys - SafeShot
		if config0['enabled'] and (key, modifiers) == parseSequence(config0['key']):
			if isDown and config0['switch']:
				config0['activated'] = not config0['activated']
				if config0['activated']:
					XModLib.Messages.Messenger.showMessageOnPanel('PlayerMessagesPanel', 0, config0['onActivate'], 'green')
				else:
					XModLib.Messages.Messenger.showMessageOnPanel('PlayerMessagesPanel', 0, config0['onDeactivate'], 'red')
			elif not config0['switch']:
				config0['activated'] = not isDown
	## HotKeys - Arcade
	if self.ctrlModeName is 'arcade':
		config0 = _config_['arcadeAS']['aimCorrection']['manualMode']
		config1 = _config_['arcadeAS']['targetLock']['manualMode']
		config2 = _config_['commonAS']['sniperModeSPG']
		config3 = _config_['arcadeAS']['aimingInfo']
		## HotKeys - AimCorrection - ManualMode
		if config0['enabled'] and (key, modifiers) == parseSequence(config0['key']):
			if isDown:
				pass
		## HotKeys - TargetLock - ManualMode
		elif config1['enabled'] and (key, modifiers) == parseSequence(config1['key']):
			if isDown:
				target = BigWorld.target()
				target = target if XModLib.VehicleInfo.VehicleInfo.isVehicle(target) else None
				if target is None and config1['useXRay']:
					target = XModLib.XRayScanner.XRayScanner.getTarget()
				self.XTargetInfo = TargetInfo(target, None) if target is not None else None
		## HotKeys - SPG Sniper Mode
		elif config2['enabled'] and (key, modifiers) == parseSequence(config2['key']):
			if isDown and XModLib.ArenaInfo.ArenaInfo.getClass(BigWorld.player().playerVehicleID) is 'SPG':
				desiredShotPoint = self.ctrl.camera.aimingSystem.getDesiredShotPoint()
				self.onControlModeChanged('sniper', preferredPos=desiredShotPoint, aimingMode=self.ctrl.aimingMode, saveZoom=True, equipmentID=None)
		## HotKeys - AimingInfo
		elif config3['enabled'] and (key, modifiers) == parseSequence(config3['key']):
			if isDown and config3['switch']:
				config3['activated'] = not config3['activated']
			elif not config3['switch']:
				config3['activated'] = isDown
			if hasattr(self.ctrl, 'XAimingInfo') and self.ctrl.XAimingInfo is not None:
				self.ctrl.XAimingInfo.window.gui.visible = config3['activated']
	## HotKeys - Sniper
	if self.ctrlModeName is 'sniper':
		config0 = _config_['sniperAS']['aimCorrection']['manualMode']
		config1 = _config_['sniperAS']['targetLock']['manualMode']
		config2 = _config_['commonAS']['sniperModeSPG']
		config3 = _config_['sniperAS']['aimingInfo']
		## HotKeys - AimCorrection - ManualMode
		if config0['enabled'] and (key, modifiers) == parseSequence(config0['key']):
			self.ctrl.XLockedDistance = None
			if isDown:
				cameraRay, cameraPoint = AvatarInputHandler.cameras.getWorldRayAndPoint(*self.ctrl.getAim().offset())
				shotPoint = self.ctrl.getDesiredShotPoint()
				if shotPoint is not None:
					self.ctrl.XLockedDistance = (shotPoint - cameraPoint).length
		## HotKeys - TargetLock - ManualMode
		elif config1['enabled'] and (key, modifiers) == parseSequence(config1['key']):
			if isDown:
				target = BigWorld.target()
				target = target if XModLib.VehicleInfo.VehicleInfo.isVehicle(target) else None
				if target is None and config1['useXRay']:
					target = XModLib.XRayScanner.XRayScanner.getTarget()
				self.XTargetInfo = TargetInfo(target, None) if target is not None else None
		## HotKeys - SPG Sniper Mode
		elif config2['enabled'] and (key, modifiers) == parseSequence(config2['key']):
			if isDown and XModLib.ArenaInfo.ArenaInfo.getClass(BigWorld.player().playerVehicleID) is 'SPG':
				desiredShotPoint = self.ctrl.camera.aimingSystem.getDesiredShotPoint()
				self.onControlModeChanged('arcade', preferredPos=desiredShotPoint, turretYaw=self.ctrl.camera.aimingSystem.turretYaw, gunPitch=self.ctrl.camera.aimingSystem.gunPitch, aimingMode=self.ctrl.aimingMode, closesDist=False)
		## HotKeys - AimingInfo
		elif config3['enabled'] and (key, modifiers) == parseSequence(config3['key']):
			if isDown and config3['switch']:
				config3['activated'] = not config3['activated']
			elif not config3['switch']:
				config3['activated'] = isDown
			if hasattr(self.ctrl, 'XAimingInfo') and self.ctrl.XAimingInfo is not None:
				self.ctrl.XAimingInfo.window.gui.visible = config3['activated']
	## HotKeys - Strategic
	if self.ctrlModeName is 'strategic':
		config0 = _config_['strategicAS']['aimCorrection']['manualMode']
		config1 = _config_['strategicAS']['targetLock']['manualMode']
		config2 = _config_['strategicAS']['aimCorrection']['relativeMode']
		config3 = _config_['strategicAS']['aimingInfo']
		config4 = _config_['strategicAS']['strategicSniper']
		config5 = _config_['strategicAS']['strategicSniper']['basePitch']['adjustment']
		## HotKeys - AimCorrection - ManualMode
		if config0['enabled'] and (key, modifiers) == parseSequence(config0['key']):
			self.ctrl.XLockedHeight = None
			if isDown:
				shotPoint = self.ctrl.getDesiredShotPoint()
				if shotPoint is not None:
					self.ctrl.XLockedHeight = shotPoint.y
		## HotKeys - TargetLock - ManualMode
		elif config1['enabled'] and (key, modifiers) == parseSequence(config1['key']):
			if isDown:
				target = BigWorld.target()
				target = target if XModLib.VehicleInfo.VehicleInfo.isVehicle(target) else None
				if target is None and config1['useXRay']:
					target = XModLib.XRayScanner.XRayScanner.getTarget()
				self.XTargetInfo = TargetInfo(target, None) if target is not None else None
		## HotKeys - AimCorrection - Relative Mode - Switch
		elif config2['enabled'] and (key, modifiers) == parseSequence(config2['key']):
			if isDown and config2['switch']:
				config2['activated'] = not config2['activated']
				if config2['activated']:
					XModLib.Messages.Messenger.showMessageOnPanel('PlayerMessagesPanel', 0, config2['onActivate'], 'green')
				else:
					XModLib.Messages.Messenger.showMessageOnPanel('PlayerMessagesPanel', 0, config2['onDeactivate'], 'red')
			elif not config2['switch']:
				config2['activated'] = isDown
		## HotKeys - AimingInfo
		elif config3['enabled'] and (key, modifiers) == parseSequence(config3['key']):
			if isDown and config3['switch']:
				config3['activated'] = not config3['activated']
			elif not config3['switch']:
				config3['activated'] = isDown
			if hasattr(self.ctrl, 'XAimingInfo') and self.ctrl.XAimingInfo is not None:
				self.ctrl.XAimingInfo.window.gui.visible = config3['activated']
		## HotKeys - Strategic Sniper - Switch
		elif config4['enabled'] and (key, modifiers) == parseSequence(config4['key']):
			if isDown and config4['switch']:
				config4['activated'] = not config4['activated']
			elif not config4['switch']:
				config4['activated'] = isDown
			self.ctrl.camera.XSwitchMode(config4['activated'])
		## HotKeys - Strategic Sniper - Base Pitch - Increase
		elif config5['enabled'] and (key, modifiers) == parseSequence(config5['increase']):
			if isDown:
				result = self.ctrl.camera.XIncreaseCameraBasePitch()
				if result is not None and result[1] and config5['message']['enabled']:
					message = _globals_['macrosFormatter'](config5['message']['template'], value=result[0], delta=result[1])
					XModLib.Messages.Messenger.showMessageOnPanel('PlayerMessagesPanel', 0, message, 'green')
		## HotKeys - Strategic Sniper - Base Pitch - Decrease
		elif config5['enabled'] and (key, modifiers) == parseSequence(config5['decrease']):
			if isDown:
				result = self.ctrl.camera.XDecreaseCameraBasePitch()
				if result is not None and result[1] and config5['message']['enabled']:
					message = _globals_['macrosFormatter'](config5['message']['template'], value=result[0], delta=result[1])
					XModLib.Messages.Messenger.showMessageOnPanel('PlayerMessagesPanel', 0, message, 'red')
	return
