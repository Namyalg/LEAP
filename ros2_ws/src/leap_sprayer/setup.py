from setuptools import find_packages, setup

package_name = 'leap_sprayer'

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
    maintainer='Namya',
    maintainer_email='namyalg@gmail.com',
    description='Handles weed detection and spray control on the Amiga',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'sprayer_control = leap_sprayer.sprayer_control:main',
        ],
    },
)
