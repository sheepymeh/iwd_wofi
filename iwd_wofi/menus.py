#!/usr/bin/python3

from dbus_next.aio import MessageBus

from .notify import Notifier
from .wofi import Wofi
from . import functions
from .dbus_helper import dbus_proxy

async def main_menu(bus, adapter):
	notifier_interface = (await dbus_proxy(await MessageBus().connect(), '/org/freedesktop/Notifications', 'org.freedesktop.Notifications')).get_interface('org.freedesktop.Notifications')
	notifier = Notifier(notifier_interface)
	menu = Wofi()

	if adapter.powered:
		menu.add_option('Turn Wi-Fi off', 'off')
		if adapter.devices[0].state == 'disconnected':
			menu.add_option('Connect to a network', 'connect')
		else:
			menu.add_option(f'Disconnect from {adapter.devices[0].connected}', 'disconnect')
			menu.add_option('Connect to a different network', 'connect')
	else:
		menu.add_option('Turn Wi-Fi on', 'on')
	try:
		_, value = await menu.show('Wi-Fi Settings')
	except:
		return

	if value == 'on':
		await functions.power_on(adapter)
		await notifier(
			title='Wi-Fi On',
			desc='Wi-Fi has been turned on',
		)

	elif value == 'off':
		await functions.power_off(adapter)
		await notifier(
			title='Wi-Fi Off',
			desc='Wi-Fi has been turned off'
		)

	if value == 'connect':
		await notifier(
			title='Scanning',
			desc='Scanning for Wi-Fi networks',
			duration=0
		)
		networks = await functions.scan(adapter.devices[0])
		if len(networks) == 0:
			await notifier(
				title='No Networks',
				desc='No nearby Wi-Fi networks found'
			)
		else:
			await notifier.dismiss_notification()
			await connection_menu(bus, networks, notifier)

	elif value == 'disconnect':
		await functions.disconnect(adapter.devices[0])
		await notifier(
			title='Wi-Fi Disconnected',
			desc=f'Disconnected from {adapter.devices[0].connected}'
		)

async def connection_menu(bus, networks, notifier):
	menu = Wofi()
	for network in networks:
		props_interface = (await dbus_proxy(bus, network[0])).get_interface('org.freedesktop.DBus.Properties')
		menu.add_option(f'{await props_interface.call_get("net.connman.iwd.Network", "Name")} ({network[1] // 100})', network[0])
	try:
		choice, value = await menu.show('Choose a Wi-Fi network')
	except:
		return
	await functions.connect(await dbus_proxy(bus, value))
	await notifier(
		title='Wi-Fi Connected',
		desc=f'Connected to {choice}'
	)