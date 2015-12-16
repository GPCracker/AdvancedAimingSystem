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
		'ignoreClientVersion': ('Bool', False),
		'hookInjectTimeout': ('Float', 3.0),
		'appLoadedMessage': ('WideString', u'&lt;a href=&quot;event:AdvancedAimingSystem.official_topic&quot;&gt;&lt;font color=&quot;#0080FF&quot;&gt;&quot;Advanced&amp;nbsp;Aiming&amp;nbsp;System&quot;&lt;/font&gt;&lt;/a&gt; &lt;font color=&quot;#008000&quot;&gt; successfully loaded.&lt;/font&gt;'),
		'appFailedMessage': ('WideString', u'&lt;a href=&quot;event:AdvancedAimingSystem.official_topic&quot;&gt;&lt;font color=&quot;#0080FF&quot;&gt;&quot;Advanced&amp;nbsp;Aiming&amp;nbsp;System&quot;&lt;/font&gt;&lt;/a&gt; &lt;font color=&quot;#E00000&quot;&gt; is incompatible with current client version.&lt;/font&gt;'),
		'commonAS': {
			'sniperModeSPG': {
				'enabled': ('Bool', False),
				'key': ('String', 'KEY_E')
			},
			'autoAim': {
				'useXRay': ('Bool', True),
				'useBBox': {
					'enabled': ('Bool', False),
					'scalar': ('Float', 2.0)
				}
			},
			'radialMenu': {
				'useXRay': ('Bool', True)
			},
			'safeShot': {
				'enabled': ('Bool', True),
				'activated': ('Bool', True),
				'key': ('String', 'KEY_LALT'),
				'switch': ('Bool', False),
				'onActivate': ('WideString', u'SafeShot enabled.'),
				'onDeactivate': ('WideString', u'SafeShot disabled.'),
				'template': ('WideString', u'[{{reason}}] Shot has been blocked.'),
				'reasons': {
					'team': ('WideString', u'team_shot'),
					'dead': ('WideString', u'dead_shot'),
					'waste': ('WideString', u'waste_shot')
				},
				'team': {
					'enabled': ('Bool', True),
					'normal': ('Bool', True),
					'blue': ('Bool', True),
					'checkGun': ('Bool', True),
					'chat': {
						'enabled': ('Bool', True),
						'timeout': ('Float', 5.0),
						'template': ('WideString', u'{{name}} ({{vehicle}}), you\'re in my line of fire!')
					}
				},
				'dead': {
					'enabled': ('Bool', True),
					'timeout': ('Float', 2.0)
				},
				'waste': {
					'enabled': ('Bool', False),
					'arcade': ('Bool', True)
				}
			},
			'expert': {
				'enabled': ('Bool', False),
				'cache': ('Bool', True),
				'queue': ('Bool', False),
				'reply': ('Float', 5.0),
				'request': ('Float', 5.0)
			}
		},
		'arcadeAS': {
			'aimCorrection': {
				'manualMode': {
					'enabled': ('Bool', False),
					'key': ('String', 'KEY_LALT'),
				},
				'targetMode': {
					'enabled': ('Bool', False)
				},
				'gui': {
					'enabled': ('Bool', False)
				}
			},
			'targetLock': {
				'manualMode': {
					'enabled': ('Bool', False),
					'useXRay': ('Bool', True),
					'key': ('String', 'KEY_T')
				},
				'autoMode': {
					'enabled': ('Bool', True),
					'allies': ('Bool', False),
					'useXRay': ('Bool', True),
					'timeout': ('Float', 3.0)
				},
				'gui': {
					'enabled': ('Bool', True),
					'speedMultiplier': ('Float', 1.0),
					'template': ('WideString', u'Target: "{{targetShortName}}"; Speed: {{targetSpeed:.1f}}m/s.'),
					'settings': {
						'font': ('String', 'default_small.font'),
						'position': ('Vector3', Math.Vector3(0, 0.30, 1.0)),
						'colour': ('Vector4', Math.Vector4(255, 127, 0, 255)),
						'widthMode': ('String', 'PIXEL'),
						'heightMode': ('String', 'PIXEL'),
						'verticalAnchor': ('String', 'CENTER'),
						'horizontalAnchor': ('String', 'CENTER'),
						'verticalPositionMode': ('String', 'CLIP'),
						'horizontalPositionMode': ('String', 'CLIP')
					}
				}
			},
			'aimingInfo': {
				'enabled': ('Bool', False),
				'activated': ('Bool', True),
				'key': ('String', 'KEY_LCONTROL+KEY_A'),
				'switch': ('Bool', True),
				'template': ('WideString', u'Remains: {{remainingAimingTime:.2f}}s;\\nDistance: {{aimingDistance:.1f}}m;\\nDeviation: {{deviation:.2f}}m;\\nFly time: {{flyTime:.2f}}s;'),
				'settings': {
					'window': {
						'size': ('Vector2', Math.Vector2(180, 85)),
						'colour': ('Vector4', Math.Vector4(0, 0, 0, 127)),
						'position': ('Vector3', Math.Vector3(0.4, -0.1, 1.0)),
						'textureName': ('String', 'gui/maps/ingame/textures/AdvancedAimingSystem/aimingInfoBG.dds'),
						'materialFX': ('String', 'BLEND'),
						'widthMode': ('String', 'PIXEL'),
						'heightMode': ('String', 'PIXEL'),
						'verticalAnchor': ('String', 'CENTER'),
						'horizontalAnchor': ('String', 'CENTER'),
						'verticalPositionMode': ('String', 'CLIP'),
						'horizontalPositionMode': ('String', 'CLIP')
					},
					'label': {
						'multiline': ('Bool', True),
						'font': ('String', 'default_small.font'),
						'position': ('Vector3', Math.Vector3(25, 5, 1)),
						'colour': ('Vector4', Math.Vector4(100, 180, 240, 255)),
						'widthMode': ('String', 'PIXEL'),
						'heightMode': ('String', 'PIXEL'),
						'verticalAnchor': ('String', 'TOP'),
						'horizontalAnchor': ('String', 'LEFT'),
						'verticalPositionMode': ('String', 'PIXEL'),
						'horizontalPositionMode': ('String', 'PIXEL')
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
					'enabled': ('Bool', True)
				},
				'gui': {
					'enabled': ('Bool', True),
					'template': ('WideString', u'Distance locked: {{distance:.1f}}m.'),
					'affectedColour': ('Vector4', Math.Vector4(0, 255, 0, 255)),
					'unaffectedColour': ('Vector4', Math.Vector4(255, 0, 0, 255)),
					'settings': {
						'font': ('String', 'default_small.font'),
						'position': ('Vector3', Math.Vector3(0, 0.25, 1.0)),
						'colour': ('Vector4', Math.Vector4(0, 255, 0, 255)),
						'widthMode': ('String', 'PIXEL'),
						'heightMode': ('String', 'PIXEL'),
						'verticalAnchor': ('String', 'CENTER'),
						'horizontalAnchor': ('String', 'CENTER'),
						'verticalPositionMode': ('String', 'CLIP'),
						'horizontalPositionMode': ('String', 'CLIP')
					}
				}
			},
			'targetLock': {
				'manualMode': {
					'enabled': ('Bool', False),
					'useXRay': ('Bool', True),
					'key': ('String', 'KEY_T')
				},
				'autoMode': {
					'enabled': ('Bool', True),
					'allies': ('Bool', False),
					'useXRay': ('Bool', True),
					'timeout': ('Float', 3.0)
				},
				'gui': {
					'enabled': ('Bool', True),
					'speedMultiplier': ('Float', 1.0),
					'template': ('WideString', u'Target: "{{targetShortName}}"; Speed: {{targetSpeed:.1f}}m/s.'),
					'settings': {
						'font': ('String', 'default_small.font'),
						'position': ('Vector3', Math.Vector3(0, 0.30, 1.0)),
						'colour': ('Vector4', Math.Vector4(255, 127, 0, 255)),
						'widthMode': ('String', 'PIXEL'),
						'heightMode': ('String', 'PIXEL'),
						'verticalAnchor': ('String', 'CENTER'),
						'horizontalAnchor': ('String', 'CENTER'),
						'verticalPositionMode': ('String', 'CLIP'),
						'horizontalPositionMode': ('String', 'CLIP')
					}
				}
			},
			'aimingInfo': {
				'enabled': ('Bool', False),
				'activated': ('Bool', True),
				'key': ('String', 'KEY_LCONTROL+KEY_A'),
				'switch': ('Bool', True),
				'template': ('WideString', u'Remains: {{remainingAimingTime:.2f}}s;\\nDistance: {{aimingDistance:.1f}}m;\\nDeviation: {{deviation:.2f}}m;\\nFly time: {{flyTime:.2f}}s;'),
				'settings': {
					'window': {
						'size': ('Vector2', Math.Vector2(180, 85)),
						'colour': ('Vector4', Math.Vector4(0, 0, 0, 127)),
						'position': ('Vector3', Math.Vector3(0.4, -0.25, 1.0)),
						'textureName': ('String', 'gui/maps/ingame/textures/AdvancedAimingSystem/aimingInfoBG.dds'),
						'materialFX': ('String', 'BLEND'),
						'widthMode': ('String', 'PIXEL'),
						'heightMode': ('String', 'PIXEL'),
						'verticalAnchor': ('String', 'CENTER'),
						'horizontalAnchor': ('String', 'CENTER'),
						'verticalPositionMode': ('String', 'CLIP'),
						'horizontalPositionMode': ('String', 'CLIP')
					},
					'label': {
						'multiline': ('Bool', True),
						'font': ('String', 'default_small.font'),
						'position': ('Vector3', Math.Vector3(25, 5, 1)),
						'colour': ('Vector4', Math.Vector4(100, 240, 180, 255)),
						'widthMode': ('String', 'PIXEL'),
						'heightMode': ('String', 'PIXEL'),
						'verticalAnchor': ('String', 'TOP'),
						'horizontalAnchor': ('String', 'LEFT'),
						'verticalPositionMode': ('String', 'PIXEL'),
						'horizontalPositionMode': ('String', 'PIXEL')
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
				'relativeMode': {
					'enabled': ('Bool', True),
					'activated': ('Bool', False),
					'key': ('String', 'KEY_LCONTROL+KEY_H'),
					'switch': ('Bool', True),
					'ignoreVehicles': ('Bool', True),
					'heightMultiplier': ('Float', 0.5),
					'onActivate': ('WideString', u'Target height accounting enabled.'),
					'onDeactivate': ('WideString', u'Target height accounting disabled.')
				},
				'gui': {
					'enabled': ('Bool', True),
					'template': ('WideString', u'Altitude locked: {{absoluteHeight:.1f}}m. Relative height: {{relativeHeight:.1f}}m.'),
					'settings': {
						'font': ('String', 'default_small.font'),
						'position': ('Vector3', Math.Vector3(0, 0.25, 1.0)),
						'colour': ('Vector4', Math.Vector4(0, 255, 0, 255)),
						'widthMode': ('String', 'PIXEL'),
						'heightMode': ('String', 'PIXEL'),
						'verticalAnchor': ('String', 'CENTER'),
						'horizontalAnchor': ('String', 'CENTER'),
						'verticalPositionMode': ('String', 'CLIP'),
						'horizontalPositionMode': ('String', 'CLIP')
					}
				}
			},
			'targetLock': {
				'manualMode': {
					'enabled': ('Bool', False),
					'useXRay': ('Bool', True),
					'key': ('String', 'KEY_T')
				},
				'autoMode': {
					'enabled': ('Bool', True),
					'allies': ('Bool', False),
					'useXRay': ('Bool', True),
					'timeout': ('Float', 3.0)
				},
				'gui': {
					'enabled': ('Bool', True),
					'speedMultiplier': ('Float', 1.0),
					'template': ('WideString', u'Target: "{{targetShortName}}"; Speed: {{targetSpeed:.1f}}m/s.'),
					'settings': {
						'font': ('String', 'default_small.font'),
						'position': ('Vector3', Math.Vector3(0, 0.30, 1.0)),
						'colour': ('Vector4', Math.Vector4(255, 127, 0, 255)),
						'widthMode': ('String', 'PIXEL'),
						'heightMode': ('String', 'PIXEL'),
						'verticalAnchor': ('String', 'CENTER'),
						'horizontalAnchor': ('String', 'CENTER'),
						'verticalPositionMode': ('String', 'CLIP'),
						'horizontalPositionMode': ('String', 'CLIP')
					}
				}
			},
			'aimingInfo': {
				'enabled': ('Bool', False),
				'activated': ('Bool', True),
				'key': ('String', 'KEY_LCONTROL+KEY_A'),
				'switch': ('Bool', True),
				'template': ('WideString', u'Remains: {{remainingAimingTime:.2f}}s;\\nDistance: {{aimingDistance:.1f}}m;\\nDeviation: {{deviation:.2f}}m;\\nFly time: {{flyTime:.2f}}s;'),
				'settings': {
					'window': {
						'size': ('Vector2', Math.Vector2(180, 85)),
						'colour': ('Vector4', Math.Vector4(0, 0, 0, 127)),
						'position': ('Vector3', Math.Vector3(-0.3, -0.4, 1.0)),
						'textureName': ('String', 'gui/maps/ingame/textures/AdvancedAimingSystem/aimingInfoBG.dds'),
						'materialFX': ('String', 'BLEND'),
						'widthMode': ('String', 'PIXEL'),
						'heightMode': ('String', 'PIXEL'),
						'verticalAnchor': ('String', 'CENTER'),
						'horizontalAnchor': ('String', 'CENTER'),
						'verticalPositionMode': ('String', 'CLIP'),
						'horizontalPositionMode': ('String', 'CLIP')
					},
					'label': {
						'multiline': ('Bool', True),
						'font': ('String', 'default_small.font'),
						'position': ('Vector3', Math.Vector3(25, 5, 1)),
						'colour': ('Vector4', Math.Vector4(240, 100, 100, 255)),
						'widthMode': ('String', 'PIXEL'),
						'heightMode': ('String', 'PIXEL'),
						'verticalAnchor': ('String', 'TOP'),
						'horizontalAnchor': ('String', 'LEFT'),
						'verticalPositionMode': ('String', 'PIXEL'),
						'horizontalPositionMode': ('String', 'PIXEL')
					}
				}
			},
			'strategicSniper': {
				'enabled': ('Bool', False),
				'activated': ('Bool', False),
				'key': ('String', 'KEY_LCONTROL+KEY_S'),
				'switch': ('Bool', True),
				'controlLevel': ('Float', -150.0),
				'correctMaxDistance': ('Bool', False),
				'basePitch': {
					'value': ('Float', 0.0),
					'adjustment': {
						'enabled': ('Bool', True),
						'delta': ('Float', 0.05),
						'increase': ('String', 'KEY_LCONTROL+KEY_R'),
						'decrease': ('String', 'KEY_LCONTROL+KEY_F'),
						'message': {
							'enabled': ('Bool', True),
							'template': ('WideString', u'Camera base pitch >>> {{value:.2f}} ({{delta:+.2f}}).')
						}
					}
				}
			}
		}
	}

# *************************
# Read configuration from file
# *************************
def readConfig():
	mainSection = ResMgr.openSection(os.path.splitext(__file__)[0] + '.xml')
	if mainSection is None:
		print '[{}] Config loading failed.'.format(__application__[1])
	else:
		print '[{}] Config successfully loaded.'.format(__application__[1])
	return XModLib.ConfigReader.ConfigReader().readSection(mainSection, defaultConfig())
