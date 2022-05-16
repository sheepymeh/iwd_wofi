#!/usr/bin/python3

from setuptools import setup

setup(
	name='iwd_wofi',
	version='0.1',
	description='An iwd GUI using wofi',
	license='MIT',
	author='sheepymeh',
	packages=['iwd_wofi'],
	install_requires=['dbus-python', 'PyGObject'], #external packages as dependencies
)