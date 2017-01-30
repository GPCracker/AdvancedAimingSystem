# *************************
# Application configuration
# *************************
_config_ = None

# *************************
# Default configuration
# *************************
def defaultConfig():
	return {
		'applicationEnabled': ('Bool', True),
		'ignoreClientVersion': ('Bool', True),
		'appLoadedMessage': ('LocalizedWideString', u'<a href="event:AdvancedAimingSystem.official_topic"><font color="#0080FF">"Advanced&nbsp;Aiming&nbsp;System"</font></a> <font color="#008000">successfully loaded.</font>'),
		'appFailedMessage': ('LocalizedWideString', u'<a href="event:AdvancedAimingSystem.official_topic"><font color="#0080FF">"Advanced&nbsp;Aiming&nbsp;System"</font></a> <font color="#E00000">is incompatible with current client version.</font>'),
		'commonAS': {
			'targetScanner': {
				'enabled': ('Bool', True),
				'scanMode': {
					'useNormalMode': ('Bool', True),
					'useXRayMode': ('Bool', False),
					'useBBoxMode': ('Bool', False),
					'useBEpsMode': ('Bool', False),
					'maxDistance': ('Float', 720.0),
					'boundsScalar': ('Float', 1.0),
					'autoScanInterval': ('Float', 0.04),
					'autoScanExpiryTime': ('Float', 5.0)
				},
				'autoScan': {
					'enabled': ('Bool', True),
					'activated': ('Bool', True),
					'shortcut': ('AdvancedShortcut', {
						'sequence': ('String', 'KEY_LCONTROL+KEY_X'),
						'switch': ('Bool', True),
						'invert': ('Bool', False),
					}),
					'message': {
						'onActivate': ('LocalizedWideString', u'TargetScanner:AutoMode ENABLED.'),
						'onDeactivate': ('LocalizedWideString', u'TargetScanner:AutoMode DISABLED.')
					}
				},
				'manualOverride': {
					'enabled': ('Bool', False),
					'shortcut': ('SimpleShortcut', 'KEY_T', {'switch': True, 'invert': False})
				}
			},
			'sniperModeSPG': {
				'enabled': ('Bool', False),
				'shortcut': ('SimpleShortcut', 'KEY_E', {'switch': True, 'invert': False})
			},
			'autoAim': {
				'useTargetScan': ('Bool', False),
				'useTargetInfo': ('Bool', False)
			},
			'radialMenu': {
				'useTargetInfo': ('Bool', False)
			},
			'expertPerk': {
				'enabled': ('Bool', False),
				'cacheExtrasInfo': ('Bool', True),
				'replyTimeout': ('Float', 5.0),
				'cacheExpiryTime': ('Float', 60.0),
			}
		},
		'arcadeAS': {
			'aimCorrection': {
				'manualMode': {
					'enabled': ('Bool', False),
					'shortcut': ('SimpleShortcut', 'KEY_LALT', {'switch': False, 'invert': False})
				},
				'targetMode': {
					'enabled': ('Bool', False),
					'activated': ('Bool', True),
					'shortcut': ('AdvancedShortcut', {
						'sequence': ('String', 'KEY_LCONTROL+KEY_T'),
						'switch': ('Bool', True),
						'invert': ('Bool', False),
					}),
					'message': {
						'onActivate': ('LocalizedWideString', u'ArcadeAimCorrection:TargetMode ENABLED.'),
						'onDeactivate': ('LocalizedWideString', u'ArcadeAimCorrection:TargetMode DISABLED.')
					}
				}
			}
		},
		'sniperAS': {
			'aimCorrection': {
				'manualMode': {
					'enabled': ('Bool', True),
					'shortcut': ('SimpleShortcut', 'KEY_LALT', {'switch': False, 'invert': False}),
				},
				'targetMode': {
					'enabled': ('Bool', True),
					'activated': ('Bool', True),
					'shortcut': ('AdvancedShortcut', {
						'sequence': ('String', 'KEY_LCONTROL+KEY_T'),
						'switch': ('Bool', True),
						'invert': ('Bool', False),
					}),
					'message': {
						'onActivate': ('LocalizedWideString', u'SniperAimCorrection:TargetMode ENABLED.'),
						'onDeactivate': ('LocalizedWideString', u'SniperAimCorrection:TargetMode DISABLED.')
					}
				}
			}
		},
		'strategicAS': {
			'aimCorrection': {
				'manualMode': {
					'enabled': ('Bool', True),
					'shortcut': ('SimpleShortcut', 'KEY_LALT', {'switch': False, 'invert': False}),
				},
				'targetMode': {
					'enabled': ('Bool', True),
					'activated': ('Bool', False),
					'shortcut': ('AdvancedShortcut', {
						'sequence': ('String', 'KEY_LCONTROL+KEY_T'),
						'switch': ('Bool', True),
						'invert': ('Bool', False),
					}),
					'message': {
						'onActivate': ('LocalizedWideString', u'StrategicAimCorrection:TargetMode ENABLED.'),
						'onDeactivate': ('LocalizedWideString', u'StrategicAimCorrection:TargetMode DISABLED.')
					},
					'heightMultiplier': ('Float', 0.5)
				},
				'ignoreVehicles': ('Bool', False)
			}
		},
		'gui': {
			'enabled': ('Bool', True),
			'updateInterval': ('Float', 0.04),
			'panels': {
				'AdvancedAimingSystemCorrectionPanel': {
					'default': {
						'alpha': ('Float', 1.0),
						'visible': ('Bool', True),
						'background': ('String', ''),
						'tooltip': ('LocalizedWideString', u'AdvancedAimingSystemCorrectionPanel'),
						'text': ('LocalizedWideString', u'<p align="center"><font color="#00FF00" size="20" face="$UniversCondC">Distance locked: {{manualInfo:.1f}}m.</font></p>'),
						'position': ('Vector2AsTuple', (0.0, 0.3)),
						'size': ('Vector2AsTuple', (450.0, 25.0))
					},
					'arcade': ('CorrectionPanelSettings', {
						'alpha': ('Float', 1.0),
						'visible': ('Bool', True),
						'background': ('String', ''),
						'tooltip': ('LocalizedWideString', u'AdvancedAimingSystemCorrectionPanel'),
						'text': ('LocalizedWideString', u'<p align="center"><font color="#00FF00" size="20" face="$UniversCondC">Distance locked: {{manualInfo:.1f}}m.</font></p>'),
						'position': ('Vector2AsTuple', (0.0, 0.3)),
						'size': ('Vector2AsTuple', (450.0, 25.0))
					}),
					'sniper': ('CorrectionPanelSettings', {
						'alpha': ('Float', 1.0),
						'visible': ('Bool', True),
						'background': ('String', ''),
						'tooltip': ('LocalizedWideString', u'AdvancedAimingSystemCorrectionPanel'),
						'text': ('LocalizedWideString', u'<p align="center"><font color="#00FF00" size="20" face="$UniversCondC">Distance locked: {{manualInfo:.1f}}m.</font></p>'),
						'position': ('Vector2AsTuple', (0.0, 0.3)),
						'size': ('Vector2AsTuple', (450.0, 25.0))
					}),
					'strategic': ('CorrectionPanelSettings', {
						'alpha': ('Float', 1.0),
						'visible': ('Bool', True),
						'background': ('String', ''),
						'tooltip': ('LocalizedWideString', u'AdvancedAimingSystemCorrectionPanel'),
						'text': ('LocalizedWideString', u'<p align="center"><font color="#00FF00" size="20" face="$UniversCondC">Distance locked: {{manualInfo:.1f}}m.</font></p>'),
						'position': ('Vector2AsTuple', (0.0, 0.3)),
						'size': ('Vector2AsTuple', (450.0, 25.0))
					})
				},
				'AdvancedAimingSystemTargetPanel': {
					'default': {
						'alpha': ('Float', 1.0),
						'visible': ('Bool', True),
						'background': ('String', ''),
						'tooltip': ('LocalizedWideString', u'AdvancedAimingSystemTargetPanel'),
						'text': ('LocalizedWideString', u'<p align="center"><font color="#FF7F00" size="20" face="$UniversCondC">Target: {{shortName}}; Distance: {{distance:.1f}}m; Speed: {{speedMS:.1f}}m/s.</font></p>'),
						'position': ('Vector2AsTuple', (0.0, 0.4)),
						'size': ('Vector2AsTuple', (450.0, 25.0))
					},
					'arcade': ('TargetPanelSettings', {
						'alpha': ('Float', 1.0),
						'visible': ('Bool', True),
						'background': ('String', ''),
						'tooltip': ('LocalizedWideString', u'AdvancedAimingSystemTargetPanel'),
						'text': ('LocalizedWideString', u'<p align="center"><font color="#FF7F00" size="20" face="$UniversCondC">Target: {{shortName}}; Distance: {{distance:.1f}}m; Speed: {{speedMS:.1f}}m/s.</font></p>'),
						'position': ('Vector2AsTuple', (0.0, 0.4)),
						'size': ('Vector2AsTuple', (450.0, 25.0))
					}),
					'sniper': ('TargetPanelSettings', {
						'alpha': ('Float', 1.0),
						'visible': ('Bool', True),
						'background': ('String', ''),
						'tooltip': ('LocalizedWideString', u'AdvancedAimingSystemTargetPanel'),
						'text': ('LocalizedWideString', u'<p align="center"><font color="#FF7F00" size="20" face="$UniversCondC">Target: {{shortName}}; Distance: {{distance:.1f}}m; Speed: {{speedMS:.1f}}m/s.</font></p>'),
						'position': ('Vector2AsTuple', (0.0, 0.4)),
						'size': ('Vector2AsTuple', (450.0, 25.0))
					}),
					'strategic': ('TargetPanelSettings', {
						'alpha': ('Float', 1.0),
						'visible': ('Bool', True),
						'background': ('String', ''),
						'tooltip': ('LocalizedWideString', u'AdvancedAimingSystemTargetPanel'),
						'text': ('LocalizedWideString', u'<p align="center"><font color="#FF7F00" size="20" face="$UniversCondC">Target: {{shortName}}; Distance: {{distance:.1f}}m; Speed: {{speedMS:.1f}}m/s.</font></p>'),
						'position': ('Vector2AsTuple', (0.0, 0.4)),
						'size': ('Vector2AsTuple', (450.0, 25.0))
					})
				},
				'AdvancedAimingSystemAimingPanel': {
					'default': {
						'alpha': ('Float', 1.0),
						'visible': ('Bool', True),
						'background': ('String', 'img://gui/maps/icons/mods/AdvancedAimingSystem/AimingInfoBGB.png'),
						'tooltip': ('LocalizedWideString', u'AdvancedAimingSystemAimingPanel'),
						'text': ('LocalizedWideString', u'<textformat leftmargin="20" rightmargin="20" tabstops="[0,70]"><font color="#64F0B4" size="20" face="$UniversCondC">\tRemains:\t{{remainingAimingTime:.2f}}s;\n\tDistance:\t{{aimingDistance:.1f}}m;\n\tDeviation:\t{{deviation:.2f}}m;\n\tFly time:\t{{flyTime:.2f}}s;\n\tHit angle:\t{{hitAngleDeg:+.1f}}dg;</font></textformat>'),
						'position': ('Vector2AsTuple', (0.4, -0.1)),
						'size': ('Vector2AsTuple', (175.0, 130.0))
					},
					'arcade': ('AimingPanelSettings', {
						'alpha': ('Float', 1.0),
						'visible': ('Bool', True),
						'background': ('String', 'img://gui/maps/icons/mods/AdvancedAimingSystem/AimingInfoBGB.png'),
						'tooltip': ('LocalizedWideString', u'AdvancedAimingSystemAimingPanel'),
						'text': ('LocalizedWideString', u'<textformat leftmargin="20" rightmargin="20" tabstops="[0,70]"><font color="#64F0B4" size="20" face="$UniversCondC">\tRemains:\t{{remainingAimingTime:.2f}}s;\n\tDistance:\t{{aimingDistance:.1f}}m;\n\tDeviation:\t{{deviation:.2f}}m;\n\tFly time:\t{{flyTime:.2f}}s;\n\tHit angle:\t{{hitAngleDeg:+.1f}}dg;</font></textformat>'),
						'position': ('Vector2AsTuple', (0.4, -0.1)),
						'size': ('Vector2AsTuple', (175.0, 130.0))
					}),
					'sniper': ('AimingPanelSettings', {
						'alpha': ('Float', 1.0),
						'visible': ('Bool', True),
						'background': ('String', 'img://gui/maps/icons/mods/AdvancedAimingSystem/AimingInfoBGB.png'),
						'tooltip': ('LocalizedWideString', u'AdvancedAimingSystemAimingPanel'),
						'text': ('LocalizedWideString', u'<textformat leftmargin="20" rightmargin="20" tabstops="[0,70]"><font color="#64B4F0" size="20" face="$UniversCondC">\tRemains:\t{{remainingAimingTime:.2f}}s;\n\tDistance:\t{{aimingDistance:.1f}}m;\n\tDeviation:\t{{deviation:.2f}}m;\n\tFly time:\t{{flyTime:.2f}}s;\n\tHit angle:\t{{hitAngleDeg:+.1f}}dg;</font></textformat>'),
						'position': ('Vector2AsTuple', (0.4, -0.25)),
						'size': ('Vector2AsTuple', (175.0, 130.0))
					}),
					'strategic': ('AimingPanelSettings', {
						'alpha': ('Float', 1.0),
						'visible': ('Bool', True),
						'background': ('String', 'img://gui/maps/icons/mods/AdvancedAimingSystem/AimingInfoBGB.png'),
						'tooltip': ('LocalizedWideString', u'AdvancedAimingSystemAimingPanel'),
						'text': ('LocalizedWideString', u'<textformat leftmargin="20" rightmargin="20" tabstops="[0,70]"><font color="#B46464" size="20" face="$UniversCondC">\tRemains:\t{{remainingAimingTime:.2f}}s;\n\tDistance:\t{{aimingDistance:.1f}}m;\n\tDeviation:\t{{deviation:.2f}}m;\n\tFly time:\t{{flyTime:.2f}}s;\n\tHit angle:\t{{hitAngleDeg:+.1f}}dg;</font></textformat>'),
						'position': ('Vector2AsTuple', (-0.3, -0.4)),
						'size': ('Vector2AsTuple', (175.0, 130.0))
					})
				}
			}
		}
	}

# *************************
# Read configuration from file
# *************************
def readConfig():
	configReader = XModLib.XMLConfigReader.XMLConfigReader((
		('SimpleShortcut', XModLib.XMLConfigReader.DataObjectXMLReaderMeta.construct(
			'SimpleShortcutXMLReader',
			constructor=lambda shortcut, **kwargs: XModLib.KeyboardUtils.Shortcut(shortcut, **kwargs),
			section_type='String'
		)),
		('AdvancedShortcut', XModLib.XMLConfigReader.DataObjectXMLReaderMeta.construct(
			'AdvancedShortcutXMLReader',
			constructor=lambda shortcut: XModLib.KeyboardUtils.Shortcut(**shortcut),
			section_type='Dict'
		)),
		('Vector2AsTuple', XModLib.XMLConfigReader.VectorAsTupleXMLReaderMeta.construct(
			'Vector2AsTupleXMLReader',
			vector_type='Vector2'
		)),
		('LocalizedWideString', XModLib.XMLConfigReader.LocalizedWideStringXMLReaderMeta.construct(
			'LocalizedWideStringXMLReader',
			translator=_globals_['i18nFormatter']
		)),
		('CorrectionPanelSettings', XModLib.XMLConfigReader.OptionalDictXMLReaderMeta.construct(
			'PanelSettingsXMLReader',
			required_keys=('visible', ),
			default_keys=('visible', )
		)),
		('TargetPanelSettings', XModLib.XMLConfigReader.OptionalDictXMLReaderMeta.construct(
			'PanelSettingsXMLReader',
			required_keys=('visible', ),
			default_keys=('visible', )
		)),
		('AimingPanelSettings', XModLib.XMLConfigReader.OptionalDictXMLReaderMeta.construct(
			'PanelSettingsXMLReader',
			required_keys=('visible', ),
			default_keys=('visible', 'text', 'position')
		))
	))
	mainSection = configReader.open_section(os.path.splitext(__file__)[0] + '.xml')
	if mainSection is None:
		print '[{}] Config file is missing. Loading defaults.'.format(__application__[1])
	else:
		print '[{}] Config file was found. Trying to load it.'.format(__application__[1])
	return configReader(mainSection, defaultConfig())
