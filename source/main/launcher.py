# ---------------------------- #
#    Application init stage    #
# ---------------------------- #
if g_config['applicationEnabled']:
	g_inject_stage_init += g_inject_loads
	g_inject_stage_main += g_inject_basis
	g_inject_stage_main += g_inject_hooks
	g_inject_stage_init += g_inject_ovrds

# --------------------------------- #
#    Application loading message    #
# --------------------------------- #
if not g_config['applicationEnabled']:
	print >> sys.stdout, '[{0[1]}] {0[0]} is globally disabled and was not loaded.'.format(__application__)
elif not g_config['ignoreClientVersion'] and not XModLib.ClientUtils.isCompatibleClientVersion(__client__):
	print >> sys.stdout, '[{0[1]}] {0[0]} was not tested with current client version.'.format(__application__)
	g_globals['appLoadingMessage'] = g_config['appWarningMessage']
else:
	print >> sys.stdout, '[{0[1]}] {0[0]} was successfully loaded.'.format(__application__)
	g_globals['appLoadingMessage'] = g_config['appSuccessMessage']

# -------------------------------- #
#    Hooks injection init stage    #
# -------------------------------- #
g_inject_stage_init()
p_inject_stage_init()
