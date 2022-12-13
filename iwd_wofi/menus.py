#!/usr/bin/python3

from notify import Notifier
from wofi import Wofi
import functions
from dbus import Interface
from manager import dbus_proxy

notifier = Notifier()
def main_menu(adapter):
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
	_, value = menu.show('Wi-Fi Settings')

	if value == 'on':
		functions.power_on(adapter)
		notifier(
			title='Wi-Fi On',
			desc='Wi-Fi has been turned on',
		)

	elif value == 'off':
		functions.power_off(adapter)
		notifier(
			title='Wi-Fi Off',
			desc='Wi-Fi has been turned off'
		)

	if value == 'connect':
		notifier(
			title='Scanning',
			desc='Scanning for Wi-Fi networks',
			duration=0
		)
		networks = functions.scan(adapter.devices[0])
		if len(networks) == 0:
			notifier(
				title='No Networks',
				desc='No nearby Wi-Fi networks found'
			)
		else:
			notifier.dismiss_notification()
			connection_menu(networks)

	elif value == 'disconnect':
		functions.disconnect(adapter.devices[0])
		notifier(
			title='Wi-Fi Disconnected',
			desc=f'Disconnected from {adapter.devices[0].connected}'
		)

def connection_menu(networks):
	menu = Wofi()
	for network in networks:
		props_interface = Interface(dbus_proxy(network[0]), 'org.freedesktop.DBus.Properties')
		menu.add_option(f'{props_interface.Get("net.connman.iwd.Network", "Name")} ({network[1] // 100})', network[0])
	choice, value = menu.show('Choose a Wi-Fi network')
	functions.connect(dbus_proxy(value))
	notifier(
		title='Wi-Fi Connected',
		desc=f'Connected to {choice}'
	)