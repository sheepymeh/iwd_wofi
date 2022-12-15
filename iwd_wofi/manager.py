#!/usr/bin/python3

import collections
from .dbus_helper import dbus_proxy

async def init(bus):
	Obj = collections.namedtuple('Obj', ['interfaces', 'children'])
	Adapter = collections.namedtuple('Adapter', ['proxy', 'phy', 'powered', 'name', 'devices'])
	Device = collections.namedtuple('Device', ['proxy', 'name', 'address', 'powered', 'state', 'connected'])
	Network = collections.namedtuple('Network', ['path', 'phy'])

	manager = (await dbus_proxy(bus, '/')).get_interface('org.freedesktop.DBus.ObjectManager')
	objects = await manager.call_get_managed_objects()

	tree = Obj({}, {})
	for path in objects:
		node = tree
		elems = path.split('/')
		for subpath in [ '/'.join(elems[:l + 1]) for l in range(1, len(elems)) ]:
			if subpath not in node.children:
				node.children[subpath] = Obj({}, {})
			node = node.children[subpath]
		node.interfaces.update(objects[path])

	root = tree.children['/net'].children['/net/connman'].children['/net/connman/iwd']
	adapters, known_networks = [], []

	for path, phy in root.children.items():
		if 'net.connman.iwd.Adapter' in phy.interfaces:
			devices = []
			for device_path, device in phy.children.items():
				if 'net.connman.iwd.Device' not in device.interfaces or device.interfaces['net.connman.iwd.Device']['Mode'] != 'station':
					continue
				state = connected_network = None
				if device.interfaces['net.connman.iwd.Device']['Powered']:
					state = device.interfaces['net.connman.iwd.Station']['State']
					connected_network = device.interfaces['net.connman.iwd.Station'].get('ConnectedNetwork', None)
				devices.append(Device(
					await dbus_proxy(bus, device_path),
					device.interfaces['net.connman.iwd.Device']['Name'],
					device.interfaces['net.connman.iwd.Device']['Address'],
					device.interfaces['net.connman.iwd.Device']['Powered'],
					state,
					device.children[str(connected_network)][0]['net.connman.iwd.Network']['Name'] if connected_network else None
				))
			adapters.append(Adapter(
				await dbus_proxy(bus, path),
				phy,
				phy.interfaces['net.connman.iwd.Adapter']['Powered'],
				phy.interfaces['net.connman.iwd.Adapter']['Name'],
				devices
			))
		elif 'net.connman.iwd.KnownNetwork':
			known_networks.append(Network(path, phy))

	return adapters, known_networks