
from setuptools import find_packages, setup

package_name = 'my_first_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='richard',
    maintainer_email='richard.ndisya@strathmore.edu',
    description='My first ROS 2 Python robot controller',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'move_turtle = my_first_robot.move_turtle:main',
            'wall_avoider = my_first_robot.wall_avoider:main',
            'lidar_avoider = my_first_robot.lidar_avoider:main',
        ],
    },
)
