# ------------ #
#    Python    #
# ------------ #
# nothing

# -------------- #
#    BigWorld    #
# -------------- #
import GUI
import Math
import BigWorld

# ---------------- #
#    WoT Client    #
# ---------------- #
import CommandMapping

# ---------------------- #
#    WoT Client Hooks    #
# ---------------------- #
import gui.battle_control.controllers.chat_cmd_ctrl
import gui.Scaleform.daapi.view.battle.shared.radial_menu

# ------------------- #
#    X-Mod Library    #
# ------------------- #
import XModLib.HookUtils

# ----------------------------------- #
#    Plug-in default configuration    #
# ----------------------------------- #
g_globals['appDefaultConfig']['plugins']['radialMenu'] = {
	'enabled': ('Bool', False),
	'useTargetScan': ('Bool', False),
	'useTargetInfo': ('Bool', False)
}

# ----------------------------------------- #
#    Plug-in configuration reading stage    #
# ----------------------------------------- #
g_config['plugins']['radialMenu'] = g_globals['appConfigReader'](
	XModLib.XMLConfigReader.overrideOpenSubSection(g_globals['appConfigFile'], 'plugins/radialMenu'),
	g_globals['appDefaultConfig']['plugins']['radialMenu']
)

# ------------------------------------ #
#    Plug-in hooks injection events    #
# ------------------------------------ #
p_inject_hooks = XModLib.HookUtils.HookEvent()
p_inject_ovrds = XModLib.HookUtils.HookEvent()

# ------------------------ #
#    Plug-in init stage    #
# ------------------------ #
if g_config['applicationEnabled'] and g_config['plugins']['radialMenu']['enabled']:
	p_inject_stage_main += p_inject_hooks
	p_inject_stage_init += p_inject_ovrds

# ---------------------- #
#    RadialMenu Hooks    #
# ---------------------- #
@XModLib.HookUtils.methodAddExt(p_inject_ovrds, gui.Scaleform.daapi.view.battle.shared.radial_menu.RadialMenu, 'show')
def new_RadialMenu_show(self):
	player = BigWorld.player()
	target = BigWorld.target()
	# Target substitution begins.
	config = g_config['plugins']['radialMenu']
	if target is None and config['useTargetScan']:
		targetScanner = getattr(player.inputHandler, 'XTargetScanner', None)
		if targetScanner is not None:
			target = targetScanner.scanTarget().target
	if target is None and config['useTargetInfo']:
		targetInfo = getattr(player.inputHandler, 'XTargetInfo', None)
		if targetInfo is not None and not targetInfo.isExpired:
			target = targetInfo.getVehicle()
	# Target substitution ends.
	self._RadialMenu__targetID = target.id if target is not None else None
	ctrl = self.sessionProvider.shared.crosshair
	guiScreenWidth, guiScreenHeight = GUI.screenResolution()
	screenRatio = float(guiScreenWidth / BigWorld.screenWidth()), float(guiScreenHeight / BigWorld.screenHeight())
	screenPosition = ctrl.getDisaredPosition() if ctrl is not None else (guiScreenWidth * 0.5, guiScreenHeight * 0.5)
	crosshairType = self._RadialMenu__getCrosshairType(player, target)
	if self.app is not None:
		self.app.registerGuiKeyHandler(self)
	self.as_showS(crosshairType, screenPosition, screenRatio)
	return

# ---------------------------------- #
#    ChatCommandsController Hooks    #
# ---------------------------------- #
@XModLib.HookUtils.methodAddExt(p_inject_ovrds, gui.battle_control.controllers.chat_cmd_ctrl.ChatCommandsController, 'handleShortcutChatCommand')
def new_ChatCommandsController_handleShortcutChatCommand(self, key):
	player = BigWorld.player()
	target = BigWorld.target()
	# Target substitution begins.
	config = g_config['plugins']['radialMenu']
	if target is None and config['useTargetScan']:
		targetScanner = getattr(player.inputHandler, 'XTargetScanner', None)
		if targetScanner is not None:
			target = targetScanner.scanTarget().target
	if target is None and config['useTargetInfo']:
		targetInfo = getattr(player.inputHandler, 'XTargetInfo', None)
		if targetInfo is not None and not targetInfo.isExpired:
			target = targetInfo.getVehicle()
	# Target substitution ends.
	for chatCommand, keyboardCommand in gui.battle_control.controllers.chat_cmd_ctrl.KB_MAPPING.iteritems():
		if CommandMapping.g_instance.isFired(keyboardCommand, key):
			crosshairType = self._ChatCommandsController__getCrosshairType(player, target)
			action = chatCommand
			if crosshairType != gui.battle_control.controllers.chat_cmd_ctrl.DEFAULT_CUT:
				if chatCommand in gui.battle_control.controllers.chat_cmd_ctrl.TARGET_TRANSLATION_MAPPING:
					if crosshairType in gui.battle_control.controllers.chat_cmd_ctrl.TARGET_TRANSLATION_MAPPING[chatCommand]:
						action = gui.battle_control.controllers.chat_cmd_ctrl.TARGET_TRANSLATION_MAPPING[chatCommand][crosshairType]
			if action in gui.battle_control.controllers.chat_cmd_ctrl.TARGET_ACTIONS:
				if crosshairType != gui.battle_control.controllers.chat_cmd_ctrl.DEFAULT_CUT:
					self.handleChatCommand(action, target.id)
			else:
				self.handleChatCommand(action)
	return
