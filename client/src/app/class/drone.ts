import { Vec3 } from "@app/class/vec3";

export const UNSET_DRONE_INDEX: number = -1;
export const ALL_DRONE_INDEX: number = -2;

enum DroneState {
  STANDBY = 0,
  TAKE_OFF = 1,
  RETURN_TO_BASE = 2,
  LANDING = 3,
  FAIL = 4,
  UPDATE = 5,
}

export class Drone {
  droneId: number;
  private state: DroneState;
  batteryLevel: number;
  private isConnected: Boolean;
  private currentPosition: Vec3;
  private currentSpeed: number;

  constructor(
    droneId: number = UNSET_DRONE_INDEX,
    state: number = DroneState.STANDBY,
    batteryLevel: number = 0.0,
    isConnected: Boolean = false,
    currentPosition: Vec3 = new Vec3(),
    currentSpeed: number = 0.0
  ) {
    this.droneId = droneId;
    this.state = state;
    this.batteryLevel = batteryLevel;
    this.isConnected = isConnected;
    this.currentPosition = currentPosition;
    this.currentSpeed = currentSpeed;
  }

  updateDrone(updatedDrone: Drone): void {
    this.batteryLevel = updatedDrone.batteryLevel;
    this.state = updatedDrone.state;
    this.isConnected = updatedDrone.isConnected;
    this.currentPosition = updatedDrone.currentPosition;
    this.currentSpeed = updatedDrone.currentSpeed;
  }

  getDroneId(): number {
    return this.droneId;
  }

  getBatteryLevel(): number {
    return this.batteryLevel * 100;
  }

  getDroneStateText(): string {
    switch (this.state) {
      case DroneState.STANDBY:
        return "STANDBY";
      case DroneState.UPDATE:
        return "UPDATE";
      case DroneState.TAKE_OFF:
        return "IN MISSION";
      case DroneState.RETURN_TO_BASE:
        return "RETURN TO BASE";
      case DroneState.LANDING:
        return "LANDING";
      case DroneState.FAIL:
        return "FAIL";
      default:
        return "IMPOSSIBLE";
    }
  }

  getSpeed(): number {
    return this.currentSpeed;
  }
}
