from setuptools import find_packages, setup

package_name = 'sprayer_health'

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
    description='Health/status reporting for the sprayer stack on the Amiga',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'sprayer_health = sprayer_health.sprayer_health:main',
        ],
    },
)
