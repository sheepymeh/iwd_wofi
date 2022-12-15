#!/usr/bin/python3

from asyncio import sleep
from dbus_next import Variant

async def power_on(adapter):
	adapter_interface = adapter.proxy.get_interface('org.freedesktop.DBus.Properties')
	device_interface = adapter.devices[0].proxy.get_interface('org.freedesktop.DBus.Properties')

	await adapter_interface.call_set('net.connman.iwd.Adapter', 'Powered', Variant('b', True))
	await device_interface.call_set('net.connman.iwd.Device', 'Powered', Variant('b', True))

async def power_off(adapter):
	adapter_interface = adapter.proxy.get_interface('org.freedesktop.DBus.Properties')
	device_interface = adapter.devices[0].proxy.get_interface('org.freedesktop.DBus.Properties')

	await device_interface.call_set('net.connman.iwd.Device', 'Powered', Variant('b', False))
	await adapter_interface.call_set('net.connman.iwd.Adapter', 'Powered', Variant('b', False))

async def scan(device):
	station_interface = device.proxy.get_interface('net.connman.iwd.Station')
	props_interface = device.proxy.get_interface('org.freedesktop.DBus.Properties')
	await station_interface.call_scan()
	while await props_interface.call_get('net.connman.iwd.Station', 'Scanning'):
		await sleep(.5)
	return await station_interface.call_get_ordered_networks()

async def connect(network):
	interface = network.get_interface('net.connman.iwd.Network')
	await interface.call_connect()

async def disconnect(device):
	interface = device.proxy.get_interface('net.connman.iwd.Station')
	await interface.call_disconnect()