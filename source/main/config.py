# *************************
# Application configuration
# *************************
def loadConfiguration():
	configReader = XModLib.XMLConfigReader.XMLConfigReader((
		('SimpleShortcut', XModLib.XMLConfigReader.DataObjectXMLReaderMeta.construct(
			'SimpleShortcutXMLReader',
			constructor=lambda shortcut, **kwargs: XModLib.KeyboardUtils.Shortcut(shortcut, **kwargs),
			sectionType='String'
		)),
		('AdvancedShortcut', XModLib.XMLConfigReader.DataObjectXMLReaderMeta.construct(
			'AdvancedShortcutXMLReader',
			constructor=lambda shortcut: XModLib.KeyboardUtils.Shortcut(**shortcut),
			sectionType='Dict'
		)),
		('LocalizedWideString', XModLib.XMLConfigReader.LocalizedWideStringXMLReaderMeta.construct(
			'LocalizedWideStringXMLReader',
			translator=_globals_['i18nFormatter']
		)),
		('CorrectionPanelSettings', XModLib.XMLConfigReader.OptionalDictXMLReaderMeta.construct(
			'PanelSettingsXMLReader',
			requiredKeys=('visible', ),
			defaultKeys=('visible', )
		)),
		('TargetPanelSettings', XModLib.XMLConfigReader.OptionalDictXMLReaderMeta.construct(
			'PanelSettingsXMLReader',
			requiredKeys=('visible', ),
			defaultKeys=('visible', )
		)),
		('AimingPanelSettings', XModLib.XMLConfigReader.OptionalDictXMLReaderMeta.construct(
			'PanelSettingsXMLReader',
			requiredKeys=('visible', ),
			defaultKeys=('visible', 'template', 'position')
		)),
		('InfoPanelsIngameSettings', XModLib.IngameSettings.IngameSettingsXMLReaderMeta.construct(
			'InfoPanelsIngameSettingsXMLReader',
			constructor=XModLib.IngameSettings.IngameSettingsDictDataObject.loader('mods/GPCracker.AdvancedAimingSystem/gui/panels/ingame', True)
		))
	))
	defaultConfig = {
		'applicationEnabled': ('Bool', True),
		'ignoreClientVersion': ('Bool', True),
		'appLoadedMessage': ('LocalizedWideString', u'<a href="event:AdvancedAimingSystem.official_topic"><font color="#0080FF">"Advanced&nbsp;Aiming&nbsp;System"</font></a> <font color="#008000">successfully loaded.</font>'),
		'appFailedMessage': ('LocalizedWideString', u'<a href="event:AdvancedAimingSystem.official_topic"><font color="#0080FF">"Advanced&nbsp;Aiming&nbsp;System"</font></a> <font color="#E00000">is incompatible with current client version.</font>'),
		'modules': {
			'targetScanner': {
				'enabled': ('Bool', True),
				'scanMode': {
					'useStandardMode': ('Bool', True),
					'useXRayMode': ('Bool', False),
					'useBBoxMode': ('Bool', False),
					'useBEpsMode': ('Bool', False),
					'maxDistance': ('Float', 720.0),
					'boundsScalar': ('Float', 2.5),
					'autoScanInterval': ('Float', 0.04),
					'autoScanExpiryTimeout': ('Float', 10.0),
					'autoScanRelockTimeout': ('Float', 0.16)
				},
				'autoScan': {
					'enabled': ('Bool', True),
					'activated': ('Bool', True),
					'shortcut': ('AdvancedShortcut', {
						'sequence': ('String', 'KEY_LCONTROL+KEY_N'),
						'switch': ('Bool', True),
						'invert': ('Bool', False)
					}),
					'message': {
						'onActivate': ('LocalizedWideString', u'[TargetScanner] AutoMode ENABLED.'),
						'onDeactivate': ('LocalizedWideString', u'[TargetScanner] AutoMode DISABLED.')
					}
				},
				'manualOverride': {
					'enabled': ('Bool', False),
					'shortcut': ('SimpleShortcut', 'KEY_NONE', {'switch': True, 'invert': False})
				}
			},
			'aimCorrection': {
				'arcade': {
					'enabled': ('Bool', False),
					'manualMode': {
						'enabled': ('Bool', True),
						'shortcut': ('SimpleShortcut', 'KEY_LALT', {'switch': False, 'invert': False})
					},
					'targetMode': {
						'enabled': ('Bool', True),
						'activated': ('Bool', True),
						'shortcut': ('AdvancedShortcut', {
							'sequence': ('String', 'KEY_LCONTROL+KEY_K'),
							'switch': ('Bool', True),
							'invert': ('Bool', False)
						}),
						'message': {
							'onActivate': ('LocalizedWideString', u'[ArcadeAimCorrection] TargetMode ENABLED.'),
							'onDeactivate': ('LocalizedWideString', u'[ArcadeAimCorrection] TargetMode DISABLED.')
						},
						'distance': ('Vector2AsTuple', (50.0, 720.0))
					}
				},
				'sniper': {
					'enabled': ('Bool', True),
					'manualMode': {
						'enabled': ('Bool', True),
						'shortcut': ('SimpleShortcut', 'KEY_LALT', {'switch': False, 'invert': False})
					},
					'targetMode': {
						'enabled': ('Bool', True),
						'activated': ('Bool', True),
						'shortcut': ('AdvancedShortcut', {
							'sequence': ('String', 'KEY_LCONTROL+KEY_K'),
							'switch': ('Bool', True),
							'invert': ('Bool', False)
						}),
						'message': {
							'onActivate': ('LocalizedWideString', u'[SniperAimCorrection] TargetMode ENABLED.'),
							'onDeactivate': ('LocalizedWideString', u'[SniperAimCorrection] TargetMode DISABLED.')
						},
						'distance': ('Vector2AsTuple', (10.0, 720.0))
					}
				},
				'strategic': {
					'enabled': ('Bool', True),
					'manualMode': {
						'enabled': ('Bool', True),
						'shortcut': ('SimpleShortcut', 'KEY_LALT', {'switch': False, 'invert': False})
					},
					'targetMode': {
						'enabled': ('Bool', True),
						'activated': ('Bool', False),
						'shortcut': ('AdvancedShortcut', {
							'sequence': ('String', 'KEY_LCONTROL+KEY_K'),
							'switch': ('Bool', True),
							'invert': ('Bool', False)
						}),
						'message': {
							'onActivate': ('LocalizedWideString', u'[StrategicAimCorrection] TargetMode ENABLED.'),
							'onDeactivate': ('LocalizedWideString', u'[StrategicAimCorrection] TargetMode DISABLED.')
						},
						'heightMultiplier': ('Float', 0.5)
					},
					'ignoreVehicles': ('Bool', False)
				},
				'arty': {
					'enabled': ('Bool', False),
					'manualMode': {
						'enabled': ('Bool', True),
						'shortcut': ('SimpleShortcut', 'KEY_LALT', {'switch': False, 'invert': False})
					},
					'targetMode': {
						'enabled': ('Bool', True),
						'activated': ('Bool', True),
						'shortcut': ('AdvancedShortcut', {
							'sequence': ('String', 'KEY_LCONTROL+KEY_K'),
							'switch': ('Bool', True),
							'invert': ('Bool', False)
						}),
						'message': {
							'onActivate': ('LocalizedWideString', u'[ArtyAimCorrection] TargetMode ENABLED.'),
							'onDeactivate': ('LocalizedWideString', u'[ArtyAimCorrection] TargetMode DISABLED.')
						}
					}
				}
			}
		},
		'plugins': {
			'safeShot': {
				'enabled': ('Bool', False),
				'activated': ('Bool', True),
				'shortcut': ('AdvancedShortcut', {
					'sequence': ('String', 'KEY_LALT'),
					'switch': ('Bool', False),
					'invert': ('Bool', True)
				}),
				'message': {
					'onActivate': ('LocalizedWideString', u'[SafeShot] ENABLED.'),
					'onDeactivate': ('LocalizedWideString', u'[SafeShot] DISABLED.')
				},
				'useGunTarget': ('Bool', True),
				'considerBlueHostile': ('Bool', False),
				'fragExpirationTimeout': ('Float', 2.0),
				'template': ('LocalizedWideString', u'[{{reason}}] Shot has been blocked.'),
				'reasons': {
					'team': {
						'enabled': ('Bool', True),
						'chat': {
							'enabled': ('Bool', True),
							'message': ('LocalizedWideString', u'{{player}} ({{vehicle}}), you\'re in my line of fire!')
						},
						'template': ('LocalizedWideString', u'friendly')
					},
					'dead': {
						'enabled': ('Bool', True),
						'template': ('LocalizedWideString', u'corpse')
					},
					'waste': {
						'enabled': ('Bool', False),
						'template': ('LocalizedWideString', u'waste')
					}
				}
			},
			'expertPerk': {
				'enabled': ('Bool', False),
				'cacheExtrasInfo': ('Bool', False),
				'cacheExpiryTimeout': ('Float', 30.0),
				'responseTimeout': ('Float', 5.0)
			},
			'advancedArty': {
				'enabled': ('Bool', False),
				'cameraAdjustment': {
					'enabled': ('Bool', True),
					'interpolationSpeed': ('Float', 5.0),
					'disableInterpolation': ('Bool', True),
					'disableHighPitchLevel': ('Bool', True)
				},
				'orthogonalView': {
					'enabled': ('Bool', True),
					'activated': ('Bool', False),
					'shortcut': ('AdvancedShortcut', {
						'sequence': ('String', 'KEY_LALT+KEY_MIDDLEMOUSE'),
						'switch': ('Bool', True),
						'invert': ('Bool', False)
					}),
					'cameraDistance': ('Float', 700.0),
					'preserveLastView': ('Bool', True)
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
				'useTargetScan': ('Bool', False),
				'useTargetInfo': ('Bool', False)
			}
		},
		'gui': {
			'enabled': ('Bool', True),
			'updateInterval': ('Float', 0.04),
			'panels': {
				'context': {
					'hideInfoPanel': ('LocalizedWideString', u'Hide this panel'),
					'resetInfoPanel': ('LocalizedWideString', u'Reset ingame settings')
				},
				'static': {
					'AdvancedAimingSystemCorrectionPanel': {
						'default': {
							'alpha': ('Float', 1.0),
							'visible': ('Bool', False),
							'background': ('String', ''),
							'tooltip': ('LocalizedWideString', u'Aim correction info panel.'),
							'template': ('LocalizedWideString', u'<p align="center"><font color="#00FF00" size="20" face="$UniversCondC">Distance locked: {{manualInfo:.1f}}m.</font></p>'),
							'position': ('Vector2AsTuple', (0.0, 0.3)),
							'size': ('Vector2AsTuple', (450.0, 25.0))
						},
						'arcade': ('CorrectionPanelSettings', {
							'alpha': ('Float', 1.0),
							'visible': ('Bool', True),
							'background': ('String', ''),
							'tooltip': ('LocalizedWideString', u'Aim correction info panel.'),
							'template': ('LocalizedWideString', u'<p align="center"><font color="#00FF00" size="20" face="$UniversCondC">Distance locked: {{manualInfo:.1f}}m.</font></p>'),
							'position': ('Vector2AsTuple', (0.0, 0.3)),
							'size': ('Vector2AsTuple', (450.0, 25.0))
						}),
						'sniper': ('CorrectionPanelSettings', {
							'alpha': ('Float', 1.0),
							'visible': ('Bool', True),
							'background': ('String', ''),
							'tooltip': ('LocalizedWideString', u'Aim correction info panel.'),
							'template': ('LocalizedWideString', u'<p align="center"><font color="#00FF00" size="20" face="$UniversCondC">Distance locked: {{manualInfo:.1f}}m.</font></p>'),
							'position': ('Vector2AsTuple', (0.0, 0.3)),
							'size': ('Vector2AsTuple', (450.0, 25.0))
						}),
						'strategic': ('CorrectionPanelSettings', {
							'alpha': ('Float', 1.0),
							'visible': ('Bool', True),
							'background': ('String', ''),
							'tooltip': ('LocalizedWideString', u'Aim correction info panel.'),
							'template': ('LocalizedWideString', u'<p align="center"><font color="#00FF00" size="20" face="$UniversCondC">Altitude locked: {{manualInfo:.1f}}m.</font></p>'),
							'position': ('Vector2AsTuple', (0.0, 0.3)),
							'size': ('Vector2AsTuple', (450.0, 25.0))
						}),
						'arty': ('CorrectionPanelSettings', {
							'alpha': ('Float', 1.0),
							'visible': ('Bool', True),
							'background': ('String', ''),
							'tooltip': ('LocalizedWideString', u'Aim correction info panel.'),
							'template': ('LocalizedWideString', u'<p align="center"><font color="#00FF00" size="20" face="$UniversCondC">Unknown parameter locked: {{manualInfo:.1f}}m.</font></p>'),
							'position': ('Vector2AsTuple', (0.0, 0.3)),
							'size': ('Vector2AsTuple', (450.0, 25.0))
						})
					},
					'AdvancedAimingSystemTargetPanel': {
						'default': {
							'alpha': ('Float', 1.0),
							'visible': ('Bool', False),
							'background': ('String', ''),
							'tooltip': ('LocalizedWideString', u'Target scanner info panel.'),
							'template': ('LocalizedWideString', u'<p align="center"><font color="#FF7F00" size="20" face="$UniversCondC">Target: {{shortName}}; Distance: {{distance:.1f}}m; Speed: {{speedMS:.1f}}m/s.</font></p>'),
							'position': ('Vector2AsTuple', (0.0, 0.4)),
							'size': ('Vector2AsTuple', (450.0, 25.0))
						},
						'arcade': ('TargetPanelSettings', {
							'alpha': ('Float', 1.0),
							'visible': ('Bool', True),
							'background': ('String', ''),
							'tooltip': ('LocalizedWideString', u'Target scanner info panel.'),
							'template': ('LocalizedWideString', u'<p align="center"><font color="#FF7F00" size="20" face="$UniversCondC">Target: {{shortName}}; Distance: {{distance:.1f}}m; Speed: {{speedMS:.1f}}m/s.</font></p>'),
							'position': ('Vector2AsTuple', (0.0, 0.4)),
							'size': ('Vector2AsTuple', (450.0, 25.0))
						}),
						'sniper': ('TargetPanelSettings', {
							'alpha': ('Float', 1.0),
							'visible': ('Bool', True),
							'background': ('String', ''),
							'tooltip': ('LocalizedWideString', u'Target scanner info panel.'),
							'template': ('LocalizedWideString', u'<p align="center"><font color="#FF7F00" size="20" face="$UniversCondC">Target: {{shortName}}; Distance: {{distance:.1f}}m; Speed: {{speedMS:.1f}}m/s.</font></p>'),
							'position': ('Vector2AsTuple', (0.0, 0.4)),
							'size': ('Vector2AsTuple', (450.0, 25.0))
						}),
						'strategic': ('TargetPanelSettings', {
							'alpha': ('Float', 1.0),
							'visible': ('Bool', True),
							'background': ('String', ''),
							'tooltip': ('LocalizedWideString', u'Target scanner info panel.'),
							'template': ('LocalizedWideString', u'<p align="center"><font color="#FF7F00" size="20" face="$UniversCondC">Target: {{shortName}}; Distance: {{distance:.1f}}m; Speed: {{speedMS:.1f}}m/s.</font></p>'),
							'position': ('Vector2AsTuple', (0.0, 0.4)),
							'size': ('Vector2AsTuple', (450.0, 25.0))
						}),
						'arty': ('TargetPanelSettings', {
							'alpha': ('Float', 1.0),
							'visible': ('Bool', True),
							'background': ('String', ''),
							'tooltip': ('LocalizedWideString', u'Target scanner info panel.'),
							'template': ('LocalizedWideString', u'<p align="center"><font color="#FF7F00" size="20" face="$UniversCondC">Target: {{shortName}}; Distance: {{distance:.1f}}m; Speed: {{speedMS:.1f}}m/s.</font></p>'),
							'position': ('Vector2AsTuple', (0.0, 0.4)),
							'size': ('Vector2AsTuple', (450.0, 25.0))
						})
					},
					'AdvancedAimingSystemAimingPanel': {
						'default': {
							'alpha': ('Float', 1.0),
							'visible': ('Bool', False),
							'background': ('String', 'img://mods/GPCracker.AdvancedAimingSystem/icons/AimingInfoBackground.png'),
							'tooltip': ('LocalizedWideString', u'Aiming info panel.'),
							'template': ('LocalizedWideString', u'<textformat leftmargin="20" rightmargin="20" tabstops="[0,70]"><font color="#64F0B4" size="20" face="$UniversCondC">\tRemains:\t{{remainingAimingTime:.2f}}s;\n\tDistance:\t{{aimingDistance:.1f}}m;\n\tDeviation:\t{{deviation:.2f}}m;\n\tFly time:\t{{flyTime:.2f}}s;\n\tHit angle:\t{{hitAngleDeg:+.1f}}dg;</font></textformat>'),
							'position': ('Vector2AsTuple', (0.4, -0.1)),
							'size': ('Vector2AsTuple', (175.0, 130.0))
						},
						'arcade': ('AimingPanelSettings', {
							'alpha': ('Float', 1.0),
							'visible': ('Bool', True),
							'background': ('String', 'img://mods/GPCracker.AdvancedAimingSystem/icons/AimingInfoBackground.png'),
							'tooltip': ('LocalizedWideString', u'Aiming info panel.'),
							'template': ('LocalizedWideString', u'<textformat leftmargin="20" rightmargin="20" tabstops="[0,70]"><font color="#64F0B4" size="20" face="$UniversCondC">\tRemains:\t{{remainingAimingTime:.2f}}s;\n\tDistance:\t{{aimingDistance:.1f}}m;\n\tDeviation:\t{{deviation:.2f}}m;\n\tFly time:\t{{flyTime:.2f}}s;\n\tHit angle:\t{{hitAngleDeg:+.1f}}dg;</font></textformat>'),
							'position': ('Vector2AsTuple', (0.4, -0.1)),
							'size': ('Vector2AsTuple', (175.0, 130.0))
						}),
						'sniper': ('AimingPanelSettings', {
							'alpha': ('Float', 1.0),
							'visible': ('Bool', True),
							'background': ('String', 'img://mods/GPCracker.AdvancedAimingSystem/icons/AimingInfoBackground.png'),
							'tooltip': ('LocalizedWideString', u'Aiming info panel.'),
							'template': ('LocalizedWideString', u'<textformat leftmargin="20" rightmargin="20" tabstops="[0,70]"><font color="#64B4F0" size="20" face="$UniversCondC">\tRemains:\t{{remainingAimingTime:.2f}}s;\n\tDistance:\t{{aimingDistance:.1f}}m;\n\tDeviation:\t{{deviation:.2f}}m;\n\tFly time:\t{{flyTime:.2f}}s;\n\tHit angle:\t{{hitAngleDeg:+.1f}}dg;</font></textformat>'),
							'position': ('Vector2AsTuple', (0.4, -0.25)),
							'size': ('Vector2AsTuple', (175.0, 130.0))
						}),
						'strategic': ('AimingPanelSettings', {
							'alpha': ('Float', 1.0),
							'visible': ('Bool', True),
							'background': ('String', 'img://mods/GPCracker.AdvancedAimingSystem/icons/AimingInfoBackground.png'),
							'tooltip': ('LocalizedWideString', u'Aiming info panel.'),
							'template': ('LocalizedWideString', u'<textformat leftmargin="20" rightmargin="20" tabstops="[0,70]"><font color="#B46464" size="20" face="$UniversCondC">\tRemains:\t{{remainingAimingTime:.2f}}s;\n\tDistance:\t{{aimingDistance:.1f}}m;\n\tDeviation:\t{{deviation:.2f}}m;\n\tFly time:\t{{flyTime:.2f}}s;\n\tHit angle:\t{{hitAngleDeg:+.1f}}dg;</font></textformat>'),
							'position': ('Vector2AsTuple', (-0.3, -0.4)),
							'size': ('Vector2AsTuple', (175.0, 130.0))
						}),
						'arty': ('AimingPanelSettings', {
							'alpha': ('Float', 1.0),
							'visible': ('Bool', True),
							'background': ('String', 'img://mods/GPCracker.AdvancedAimingSystem/icons/AimingInfoBackground.png'),
							'tooltip': ('LocalizedWideString', u'Aiming info panel.'),
							'template': ('LocalizedWideString', u'<textformat leftmargin="20" rightmargin="20" tabstops="[0,70]"><font color="#B46464" size="20" face="$UniversCondC">\tRemains:\t{{remainingAimingTime:.2f}}s;\n\tDistance:\t{{aimingDistance:.1f}}m;\n\tDeviation:\t{{deviation:.2f}}m;\n\tFly time:\t{{flyTime:.2f}}s;\n\tHit angle:\t{{hitAngleDeg:+.1f}}dg;</font></textformat>'),
							'position': ('Vector2AsTuple', (-0.3, -0.4)),
							'size': ('Vector2AsTuple', (175.0, 130.0))
						})
					}
				},
				'ingame': ('InfoPanelsIngameSettings', 'KGRwMQou')
			}
		}
	}
	mainSection = XModLib.XMLConfigReader.openSection(os.path.splitext(__file__)[0] + '.xml')
	if mainSection is None:
		print '[{}] Config file is missing. Loading defaults.'.format(__application__[1])
	else:
		print '[{}] Config file was found. Trying to load it.'.format(__application__[1])
	return configReader(mainSection, defaultConfig)

# *************************
# Configuration init
# *************************
_config_ = loadConfiguration()
