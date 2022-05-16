#!/usr/bin/python3

import dbus
from dbus import Interface
from time import sleep

def power_on(adapter):
	adapter_interface = Interface(adapter.proxy, 'org.freedesktop.DBus.Properties')
	device_interface = Interface(adapter.devices[0].proxy, 'org.freedesktop.DBus.Properties')

	adapter_interface.Set('net.connman.iwd.Adapter', 'Powered', dbus.Boolean(1))
	device_interface.Set('net.connman.iwd.Device', 'Powered', dbus.Boolean(1))

def power_off(adapter):
	adapter_interface = Interface(adapter.proxy, 'org.freedesktop.DBus.Properties')
	device_interface = Interface(adapter.devices[0].proxy, 'org.freedesktop.DBus.Properties')

	device_interface.Set('net.connman.iwd.Device', 'Powered', dbus.Boolean(0))
	adapter_interface.Set('net.connman.iwd.Adapter', 'Powered', dbus.Boolean(0))

def scan(device):
	station_interface = Interface(device.proxy, 'net.connman.iwd.Station')
	props_interface = Interface(device.proxy, 'org.freedesktop.DBus.Properties')
	station_interface.Scan()
	while props_interface.Get('net.connman.iwd.Station', 'Scanning'):
		sleep(.5)
	return station_interface.GetOrderedNetworks()

def connect(network):
	interface = Interface(network, 'net.connman.iwd.Network')
	interface.Connect()

def disconnect(device):
	interface = Interface(device.proxy, 'net.connman.iwd.Station')
	interface.Disconnect()