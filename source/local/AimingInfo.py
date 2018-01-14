# ------------------------ #
#    AimingInfo Classes    #
# ------------------------ #
class AimingInfo(object):
	__slots__ = ('__weakref__', 'aimingThreshold')

	def __init__(self, aimingThreshold=1.05):
		super(AimingInfo, self).__init__()
		self.aimingThreshold = aimingThreshold
		return

	def getMacroData(self):
		playerAimingInfo = XModLib.BallisticsMath.getPlayerAimingInfo()
		if playerAimingInfo is not None:
			staticDispersionAngle, aimingStartTime, aimingStartFactor, dispersionFactor, expAimingTime = playerAimingInfo
			aimingFactor = XModLib.BallisticsMath.getAimingFactor(
				aimingStartTime, aimingStartFactor, dispersionFactor, expAimingTime,
				aimingThreshold=self.aimingThreshold
			)
			fullAimingTime = XModLib.BallisticsMath.getFullAimingTime(aimingStartFactor, dispersionFactor, expAimingTime)
			remainingAimingTime = XModLib.BallisticsMath.getRemainingAimingTime(aimingStartTime, fullAimingTime)
			realDispersionAngle = XModLib.BallisticsMath.getDispersionAngle(staticDispersionAngle, aimingFactor)
			aimingDistance, flyTime, shotAngleRad, hitAngleRad = XModLib.BallisticsMath.getPlayerBallisticsInfo()
			deviation = XModLib.BallisticsMath.getDeviation(realDispersionAngle, aimingDistance)
			shotAngleDeg = math.degrees(shotAngleRad)
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
				'shotAngleRad': shotAngleRad,
				'shotAngleDeg': shotAngleDeg,
				'hitAngleRad': hitAngleRad,
				'hitAngleDeg': hitAngleDeg,
				'deviation': deviation,
				'flyTime': flyTime
			}
		return None

	def enable(self):
		# nothing
		return

	def disable(self):
		# nothing
		return

	def __repr__(self):
		return '{!s}(aimingThreshold={!r})'.format(self.__class__.__name__, self.aimingThreshold)

	def __del__(self):
		return
