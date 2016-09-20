# *************************
# Configuration
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
					'updateInterval': ('Float', 0.04),
					'useNormalMode': ('Bool', True),
					'useXRayMode': ('Bool', False),
					'useBBoxMode': ('Bool', False),
					'useBEpsMode': ('Bool', False),
					'maxDistance': ('Float', 720.0),
					'boundsScalar': ('Float', 1.0),
					'expiryTime': ('Float', 5.0)
				},
				'manualOverride': {
					'enabled': ('Bool', False),
					'key': ('String', 'KEY_T')
				}
			},
			'sniperModeSPG': {
				'enabled': ('Bool', False),
				'key': ('String', 'KEY_E')
			},
			'autoAim': {
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
					'key': ('String', 'KEY_LALT')
				},
				'targetMode': {
					'enabled': ('Bool', False),
					'activated': ('Bool', True),
					'shortcut': {
						'key': ('String', 'KEY_LCONTROL+KEY_T'),
						'switch': ('Bool', True),
						'invert': ('Bool', False),
					},
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
					'key': ('String', 'KEY_LALT'),
				},
				'targetMode': {
					'enabled': ('Bool', True),
					'activated': ('Bool', True),
					'shortcut': {
						'key': ('String', 'KEY_LCONTROL+KEY_T'),
						'switch': ('Bool', True),
						'invert': ('Bool', False),
					},
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
					'key': ('String', 'KEY_LALT'),
				},
				'targetMode': {
					'enabled': ('Bool', True),
					'activated': ('Bool', False),
					'shortcut': {
						'key': ('String', 'KEY_LCONTROL+KEY_T'),
						'switch': ('Bool', True),
						'invert': ('Bool', False),
					},
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
						'position': ('Vector2AsTuple', (458.0, 250.0)),
						'size': ('Vector2AsTuple', (450.0, 25.0))
					},
					'arcade': ('PanelSettings', {
						'alpha': ('Float', 1.0),
						'visible': ('Bool', True),
						'background': ('String', ''),
						'tooltip': ('LocalizedWideString', u'AdvancedAimingSystemCorrectionPanel'),
						'text': ('LocalizedWideString', u'<p align="center"><font color="#00FF00" size="20" face="$UniversCondC">Distance locked: {{manualInfo:.1f}}m.</font></p>'),
						'position': ('Vector2AsTuple', (458.0, 250.0)),
						'size': ('Vector2AsTuple', (450.0, 25.0))
					}),
					'sniper': ('PanelSettings', {
						'alpha': ('Float', 1.0),
						'visible': ('Bool', True),
						'background': ('String', ''),
						'tooltip': ('LocalizedWideString', u'AdvancedAimingSystemCorrectionPanel'),
						'text': ('LocalizedWideString', u'<p align="center"><font color="#00FF00" size="20" face="$UniversCondC">Distance locked: {{manualInfo:.1f}}m.</font></p>'),
						'position': ('Vector2AsTuple', (458.0, 250.0)),
						'size': ('Vector2AsTuple', (450.0, 25.0))
					}),
					'strategic': ('PanelSettings', {
						'alpha': ('Float', 1.0),
						'visible': ('Bool', True),
						'background': ('String', ''),
						'tooltip': ('LocalizedWideString', u'AdvancedAimingSystemCorrectionPanel'),
						'text': ('LocalizedWideString', u'<p align="center"><font color="#00FF00" size="20" face="$UniversCondC">Distance locked: {{manualInfo:.1f}}m.</font></p>'),
						'position': ('Vector2AsTuple', (458.0, 250.0)),
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
						'position': ('Vector2AsTuple', (458.0, 225.0)),
						'size': ('Vector2AsTuple', (450.0, 25.0))
					},
					'arcade': ('PanelSettings', {
						'alpha': ('Float', 1.0),
						'visible': ('Bool', True),
						'background': ('String', ''),
						'tooltip': ('LocalizedWideString', u'AdvancedAimingSystemTargetPanel'),
						'text': ('LocalizedWideString', u'<p align="center"><font color="#FF7F00" size="20" face="$UniversCondC">Target: {{shortName}}; Distance: {{distance:.1f}}m; Speed: {{speedMS:.1f}}m/s.</font></p>'),
						'position': ('Vector2AsTuple', (458.0, 225.0)),
						'size': ('Vector2AsTuple', (450.0, 25.0))
					}),
					'sniper': ('PanelSettings', {
						'alpha': ('Float', 1.0),
						'visible': ('Bool', True),
						'background': ('String', ''),
						'tooltip': ('LocalizedWideString', u'AdvancedAimingSystemTargetPanel'),
						'text': ('LocalizedWideString', u'<p align="center"><font color="#FF7F00" size="20" face="$UniversCondC">Target: {{shortName}}; Distance: {{distance:.1f}}m; Speed: {{speedMS:.1f}}m/s.</font></p>'),
						'position': ('Vector2AsTuple', (458.0, 225.0)),
						'size': ('Vector2AsTuple', (450.0, 25.0))
					}),
					'strategic': ('PanelSettings', {
						'alpha': ('Float', 1.0),
						'visible': ('Bool', True),
						'background': ('String', ''),
						'tooltip': ('LocalizedWideString', u'AdvancedAimingSystemTargetPanel'),
						'text': ('LocalizedWideString', u'<p align="center"><font color="#FF7F00" size="20" face="$UniversCondC">Target: {{shortName}}; Distance: {{distance:.1f}}m; Speed: {{speedMS:.1f}}m/s.</font></p>'),
						'position': ('Vector2AsTuple', (458.0, 225.0)),
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
						'position': ('Vector2AsTuple', (870.0, 355.0)),
						'size': ('Vector2AsTuple', (175.0, 130.0))
					},
					'arcade': ('PanelSettings', {
						'alpha': ('Float', 1.0),
						'visible': ('Bool', True),
						'background': ('String', 'img://gui/maps/icons/mods/AdvancedAimingSystem/AimingInfoBGB.png'),
						'tooltip': ('LocalizedWideString', u'AdvancedAimingSystemAimingPanel'),
						'text': ('LocalizedWideString', u'<textformat leftmargin="20" rightmargin="20" tabstops="[0,70]"><font color="#64F0B4" size="20" face="$UniversCondC">\tRemains:\t{{remainingAimingTime:.2f}}s;\n\tDistance:\t{{aimingDistance:.1f}}m;\n\tDeviation:\t{{deviation:.2f}}m;\n\tFly time:\t{{flyTime:.2f}}s;\n\tHit angle:\t{{hitAngleDeg:+.1f}}dg;</font></textformat>'),
						'position': ('Vector2AsTuple', (870.0, 355.0)),
						'size': ('Vector2AsTuple', (175.0, 130.0))
					}),
					'sniper': ('PanelSettings', {
						'alpha': ('Float', 1.0),
						'visible': ('Bool', True),
						'background': ('String', 'img://gui/maps/icons/mods/AdvancedAimingSystem/AimingInfoBGB.png'),
						'tooltip': ('LocalizedWideString', u'AdvancedAimingSystemAimingPanel'),
						'text': ('LocalizedWideString', u'<textformat leftmargin="20" rightmargin="20" tabstops="[0,70]"><font color="#64B4F0" size="20" face="$UniversCondC">\tRemains:\t{{remainingAimingTime:.2f}}s;\n\tDistance:\t{{aimingDistance:.1f}}m;\n\tDeviation:\t{{deviation:.2f}}m;\n\tFly time:\t{{flyTime:.2f}}s;\n\tHit angle:\t{{hitAngleDeg:+.1f}}dg;</font></textformat>'),
						'position': ('Vector2AsTuple', (870.0, 415.0)),
						'size': ('Vector2AsTuple', (175.0, 130.0))
					}),
					'strategic': ('PanelSettings', {
						'alpha': ('Float', 1.0),
						'visible': ('Bool', True),
						'background': ('String', 'img://gui/maps/icons/mods/AdvancedAimingSystem/AimingInfoBGB.png'),
						'tooltip': ('LocalizedWideString', u'AdvancedAimingSystemAimingPanel'),
						'text': ('LocalizedWideString', u'<textformat leftmargin="20" rightmargin="20" tabstops="[0,70]"><font color="#B46464" size="20" face="$UniversCondC">\tRemains:\t{{remainingAimingTime:.2f}}s;\n\tDistance:\t{{aimingDistance:.1f}}m;\n\tDeviation:\t{{deviation:.2f}}m;\n\tFly time:\t{{flyTime:.2f}}s;\n\tHit angle:\t{{hitAngleDeg:+.1f}}dg;</font></textformat>'),
						'position': ('Vector2AsTuple', (395.0, 475.0)),
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
	configReader = XModLib.XMLConfigReader.XMLConfigReader.new({
		'Vector2AsTuple': XModLib.XMLConfigReader.VectorAsTupleXMLReader.new_class(
			'Vector2AsTupleXMLReader',
			VECTOR_TYPE='Vector2'
		),
		'LocalizedWideString': XModLib.XMLConfigReader.LocalizedWideStringXMLReader.new_class(
			'LocalizedWideStringXMLReader',
			TRANSLATOR=_globals_['i18nFormatter']
		),
		'PanelSettings': XModLib.XMLConfigReader.OptionalDictXMLReader.new_class(
			'PanelSettingsXMLReader',
			DEFAULT_KEYS=('visible', 'text', 'position'),
			REQUIRED_KEYS = ('visible', )
		)
	})
	mainSection = configReader.open_section(os.path.splitext(__file__)[0] + '.xml')
	if mainSection is None:
		print '[{}] Config file not found.'.format(__application__[1])
	else:
		print '[{}] Config file found and loaded.'.format(__application__[1])
	return configReader(mainSection, defaultConfig())
