# my_first_robot

ROS 2 (Jazzy) Python package built while learning robotics software, running on an M1 Mac via RoboStack/Pixi.

## Nodes
- **move_turtle**: publishes velocity commands on a timer to drive the turtlesim turtle in a spiral.
- **wall_avoider**: subscribes to the turtle's pose and steers away from walls using a heading-error check (sense → decide → act).

## Run
    ros2 run turtlesim turtlesim_node
    ros2 run my_first_robot wall_avoider