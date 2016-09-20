# *************************
# AimingInfo Class
# *************************
class AimingInfo(object):
	@staticmethod
	def getMacroData():
		playerAimingInfo = XModLib.BallisticsMath.BallisticsMath.getPlayerAimingInfo()
		if playerAimingInfo is not None:
			staticDispersionAngle, aimingStartTime, aimingStartFactor, dispersionFactor, expAimingTime = playerAimingInfo
			aimingFactor = XModLib.BallisticsMath.BallisticsMath.getAimingFactor(aimingStartTime, aimingStartFactor, dispersionFactor, expAimingTime)
			fullAimingTime = XModLib.BallisticsMath.BallisticsMath.getFullAimingTime(aimingStartFactor, dispersionFactor, expAimingTime)
			remainingAimingTime = XModLib.BallisticsMath.BallisticsMath.getRemainingAimingTime(aimingStartTime, fullAimingTime)
			realDispersionAngle = XModLib.BallisticsMath.BallisticsMath.getDispersionAngle(staticDispersionAngle, aimingFactor)
			aimingDistance, hitAngleRad, flyTime = XModLib.BallisticsMath.BallisticsMath.getPlayerBallisticsInfo()
			deviation = XModLib.BallisticsMath.BallisticsMath.getDeviation(aimingDistance, realDispersionAngle)
			hitAngleDeg = math.degrees(hitAngleRad)
			return {
				'expAimingTime': expAimingTime,
				'fullAimingTime': fullAimingTime,
				'remainingAimingTime': remainingAimingTime,
				'staticDispersionAngle': staticDispersionAngle,
				'realDispersionAngle': realDispersionAngle,
				'dispersionFactor': dispersionFactor,
				'aimingDistance': aimingDistance,
				'aimingFactor': aimingFactor,
				'hitAngleRad': hitAngleRad,
				'hitAngleDeg': hitAngleDeg,
				'deviation': deviation,
				'flyTime': flyTime
			}
		return None
