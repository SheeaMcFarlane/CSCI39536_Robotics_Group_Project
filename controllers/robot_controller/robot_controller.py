import sys
from controller import Robot

# Initialize the Webots Robot instance
robot = Robot()
timestep = int(robot.getBasicTimeStep())

MAX_SPEED = 6.28
SAFETY_THRESHOLD = 0.5

# Map the 4 wheels of the pre-built Pioneer robot
motors = {
    'left_front': robot.getDevice('left front wheel'),
    'left_rear': robot.getDevice('left back wheel'),
    'right_front': robot.getDevice('right front wheel'),
    'right_rear': robot.getDevice('right back wheel')
}

for motor in motors.values():
    motor.setPosition(float('inf'))
    motor.setVelocity(0.0)

# Initialize the front sonar sensors (so0 to so7) built into the robot
sonar_sensors = []
sonar_names = ['so0', 'so1', 'so2', 'so3', 'so4', 'so5', 'so6', 'so7']
for name in sonar_names:
    sensor = robot.getDevice(name)
    sensor.enable(timestep)
    sonar_sensors.append(sensor)

print("[ONLINE] Autonomous navigation loop active. Searching area...")

# Main control loop
while robot.step(timestep) != -1:
    sonar_values = [s.getValue() for s in sonar_sensors]
    
    # Check front left and front right sonar thresholds
    left_blocked = sonar_values[3] < SAFETY_THRESHOLD or sonar_values[2] < SAFETY_THRESHOLD
    right_blocked = sonar_values[4] < SAFETY_THRESHOLD or sonar_values[5] < SAFETY_THRESHOLD

    if left_blocked and right_blocked:
        # Turn around if fully blocked
        left_speed = -MAX_SPEED * 0.3
        right_speed = -MAX_SPEED * 0.5
    elif left_blocked:
        # Pivot right if blocked on left
        left_speed = MAX_SPEED * 0.4
        right_speed = -MAX_SPEED * 0.2
    elif right_blocked:
        # Pivot left if blocked on right
        left_speed = -MAX_SPEED * 0.2
        right_speed = MAX_SPEED * 0.4
    else:
        # Clear path: Drive forward searching
        left_speed = MAX_SPEED * 0.5
        right_speed = MAX_SPEED * 0.5

    # Assign velocities to the motor pairings
    motors['left_front'].setVelocity(left_speed)
    motors['left_rear'].setVelocity(left_speed)
    motors['right_front'].setVelocity(right_speed)
    motors['right_rear'].setVelocity(right_speed)

