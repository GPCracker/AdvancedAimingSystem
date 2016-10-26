# *************************
# Python
# *************************
# Nothing

# *************************
# BigWorld
# *************************
import Math
import BigWorld

# *************************
# WoT Client
# *************************
import BattleReplay
import ProjectileMover

# *************************
# WoT Client Hooks
# *************************
import VehicleGunRotator

# *************************
# X-Mod Code Library
# *************************
import XModLib.Colliders
import XModLib.HookUtils
import XModLib.MathUtils

# *************************
# VehicleGunRotator Hooks
# *************************
@XModLib.HookUtils.HookFunction.methodAddOnEvent(_inject_hooks_, VehicleGunRotator.VehicleGunRotator, '_VehicleGunRotator__getGunMarkerPosition')
def __getGunMarkerPosition(self, shotPoint, shotVector, dispersionAngles):
	aimCorrection = getattr(self._VehicleGunRotator__avatar.inputHandler.ctrl, 'XAimCorrection', None)
	def colliderCorrection(collisionTestStart, collisionTestStop):
		if aimCorrection is not None:
			result = aimCorrection.getGunMarkerCollisionPoint(collisionTestStart, collisionTestStop)
			return (result, ) if result is not None else None
		return None
	collisionEntities = ProjectileMover.getCollidableEntities(
		(self._VehicleGunRotator__avatar.playerVehicleID, ),
		shotPoint,
		shotPoint + shotVector * 10000.0
	)
	def colliderMaterial(collisionTestStart, collisionTestStop):
		return ProjectileMover.collideVehiclesAndStaticScene(collisionTestStart, collisionTestStop, collisionEntities)
	def colliderSpace(collisionTestStart, collisionTestStop):
		result = self._VehicleGunRotator__avatar.arena.collideWithSpaceBB(collisionTestStart, collisionTestStop)
		return (result, ) if result is not None else None
	colliders = (colliderCorrection, colliderMaterial, colliderSpace)
	vehicleTypeDescriptor = self._VehicleGunRotator__avatar.vehicleTypeDescriptor
	shotGravity = Math.Vector3(0.0, -1.0, 0.0).scale(vehicleTypeDescriptor.shot['gravity'])
	shotMaxDistance = vehicleTypeDescriptor.shot['maxDistance']
	hitPoint, hitVector, hitResult, hitCollider = XModLib.Colliders.Colliders.computeProjectileTrajectoryEnd(shotPoint, shotVector, shotGravity, colliders)
	hitData = hitResult[1] if hitCollider is colliderMaterial and hitResult[1] is not None and hitResult[1].isVehicle() else None
	markerDistance = shotPoint.distTo(hitPoint)
	if hitCollider is colliderSpace and markerDistance >= shotMaxDistance:
		hitVector = XModLib.MathUtils.MathUtils.getNormalisedVector(hitPoint - shotPoint)
		hitPoint = shotPoint + hitVector.scale(shotMaxDistance)
		markerDistance = shotMaxDistance
	markerDiameter = 2.0 * markerDistance * dispersionAngles[0]
	idealMarkerDiameter = 2.0 * markerDistance * dispersionAngles[1]
	if BattleReplay.g_replayCtrl.isPlaying and BattleReplay.g_replayCtrl.isClientReady:
		markerDiameter, hitPoint, hitVector = BattleReplay.g_replayCtrl.getGunMarkerParams(hitPoint, hitVector)
	return hitPoint, hitVector, markerDiameter, idealMarkerDiameter, hitData
