# ------------ #
#    Python    #
# ------------ #
# nothing

# -------------- #
#    BigWorld    #
# -------------- #
import Math
import BigWorld

# ---------------- #
#    WoT Client    #
# ---------------- #
import BattleReplay
import ProjectileMover

# ---------------------- #
#    WoT Client Hooks    #
# ---------------------- #
import VehicleGunRotator

# ------------------- #
#    X-Mod Library    #
# ------------------- #
import XModLib.HookUtils
import XModLib.MathUtils
import XModLib.CollisionUtils

# ----------------------------------- #
#    Plug-in default configuration    #
# ----------------------------------- #
# nothing

# ----------------------------------------- #
#    Plug-in configuration reading stage    #
# ----------------------------------------- #
# nothing

# ------------------------------------ #
#    Plug-in hooks injection events    #
# ------------------------------------ #
p_inject_hooks = XModLib.HookUtils.HookEvent()
p_inject_ovrds = XModLib.HookUtils.HookEvent()

# ------------------------ #
#    Plug-in init stage    #
# ------------------------ #
if g_config['applicationEnabled']:
	sections = g_config['modules']['aimCorrection'].viewvalues()
	if any(section['fixGunMarker'] for section in sections if section['enabled']):
		p_inject_stage_main += p_inject_hooks
		p_inject_stage_init += p_inject_ovrds
	del sections

# ----------------------------- #
#    VehicleGunRotator Hooks    #
# ----------------------------- #
@XModLib.HookUtils.methodAddExt(p_inject_ovrds, VehicleGunRotator.VehicleGunRotator, '_VehicleGunRotator__getGunMarkerPosition')
def new_VehicleGunRotator_getGunMarkerPosition(self, shotPoint, shotVector, dispersionAngles):
	aimCorrection = getattr(self._VehicleGunRotator__avatar.inputHandler.ctrl, 'XAimCorrection', None)
	def colliderCorrection(collisionTestStart, collisionTestStop):
		if aimCorrection is not None:
			result = aimCorrection.getGunMarkerCollisionPoint(collisionTestStart, collisionTestStop)
			return (result, ) if result is not None else None
		return None
	def colliderMaterial(collisionTestStart, collisionTestStop):
		return ProjectileMover.collideDynamicAndStatic(collisionTestStart, collisionTestStop, (self.getAttachedVehicleID(), ))
	def colliderSpace(collisionTestStart, collisionTestStop):
		result = self._VehicleGunRotator__avatar.arena.collideWithSpaceBB(collisionTestStart, collisionTestStop)
		return (result, ) if result is not None else None
	colliders = (colliderCorrection, colliderMaterial, colliderSpace)
	vehicleTypeDescriptor = self._VehicleGunRotator__avatar.getVehicleDescriptor()
	shotGravity = Math.Vector3(0.0, -1.0, 0.0).scale(vehicleTypeDescriptor.shot.gravity)
	shotMaxDistance = vehicleTypeDescriptor.shot.maxDistance
	hitPoint, hitVector, hitResult, hitCollider = XModLib.CollisionUtils.computeProjectileTrajectoryEnd(shotPoint, shotVector, shotGravity, colliders)
	hitData = hitResult[1] if hitCollider is colliderMaterial and hitResult[1] is not None and hitResult[1].isVehicle() else None
	markerDistance = shotPoint.distTo(hitPoint)
	if hitCollider is colliderSpace and markerDistance >= shotMaxDistance:
		hitVector = XModLib.MathUtils.getNormalisedVector(hitPoint - shotPoint)
		hitPoint = shotPoint + hitVector.scale(shotMaxDistance)
		markerDistance = shotMaxDistance
	markerDiameter = 2.0 * markerDistance * dispersionAngles[0]
	idealMarkerDiameter = 2.0 * markerDistance * dispersionAngles[1]
	if BattleReplay.g_replayCtrl.isPlaying and BattleReplay.g_replayCtrl.isClientReady:
		markerDiameter, hitPoint, hitVector = BattleReplay.g_replayCtrl.getGunMarkerParams(hitPoint, hitVector)
	return hitPoint, hitVector, markerDiameter, idealMarkerDiameter, hitData
