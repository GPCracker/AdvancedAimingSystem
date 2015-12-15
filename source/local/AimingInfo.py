# *************************
# AimingInfo Class
# *************************
class AimingInfo(object):
	def __init__(self, windowSettings, labelSettings):
		self.window = XModLib.GUIWrapper.GUIWrapper.createGUI('Window', windowSettings, True)
		self.window.gui.label = XModLib.GUIWrapper.GUIWrapper.createGUI('Text', labelSettings, False)
		return

	@staticmethod
	def aquireAimingInfo():
		try:
			dispersionAngle, aimingStartTime, aimingStartFactor, dispersionFactor, aimingTime = XModLib.BallisticsMath.BallisticsMath.getPlayerAimingInfo()
			aimingFactor = XModLib.BallisticsMath.BallisticsMath.getAimingFactor(aimingStartTime, aimingStartFactor, dispersionFactor, aimingTime)
			fullAimingTime = XModLib.BallisticsMath.BallisticsMath.getFullAimingTime(aimingStartFactor, dispersionFactor, aimingTime)
			remainingAimingTime = XModLib.BallisticsMath.BallisticsMath.getRemainingAimingTime(aimingStartTime, fullAimingTime)
			realDispersionAngle = XModLib.BallisticsMath.BallisticsMath.getDispersionAngle(dispersionAngle, aimingFactor)
			aimingDistance, flyTime = XModLib.BallisticsMath.BallisticsMath.getPlayerDistanceAndFlyTime()
			deviation = XModLib.BallisticsMath.BallisticsMath.getDeviation(aimingDistance, realDispersionAngle)
			return {
				'staticDispersionAngle': dispersionAngle,
				'dispersionFactor': dispersionFactor,
				'expAimingTime': aimingTime,
				'aimingFactor': aimingFactor,
				'fullAimingTime': fullAimingTime,
				'remainingAimingTime': remainingAimingTime,
				'realDispersionAngle': realDispersionAngle,
				'deviation': deviation,
				'aimingDistance': aimingDistance,
				'flyTime': flyTime
			}
		except:
			pass
		return None

	def __del__(self):
		return
