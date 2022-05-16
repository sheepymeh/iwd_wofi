#!/usr/bin/python3

from gi.repository import GLib

import dbus
import dbus.service
import dbus.mainloop.glib
from random import randrange

from wofi import Wofi

wofi = Wofi()

class Canceled(dbus.DBusException):
	_dbus_error_name = 'net.connman.iwd.Error.Canceled'

class Agent(dbus.service.Object):
	@dbus.service.method('net.connman.iwd.Agent', in_signature='', out_signature='')
	def Release(self):
		print('Release')
		mainloop.quit()

	@dbus.service.method('net.connman.iwd.Agent', in_signature='o', out_signature='s')
	def RequestPassphrase(self, path):
		passphrase = wofi.show('Enter your Wi-Fi password', True)
		if not passphrase:
			raise Canceled('canceled')

		return passphrase

	@dbus.service.method('net.connman.iwd.Agent', in_signature='o', out_signature='s')
	def RequestPrivateKeyPassphrase(self, path):
		passphrase = wofi.show('Enter your key passphrase', True)
		if not passphrase:
			raise Canceled('canceled')

		return passphrase

	@dbus.service.method('net.connman.iwd.Agent', in_signature='o', out_signature='ss')
	def RequestUserNameAndPassword(self, path):
		username = wofi.show('Enter your network username')
		if not username:
			raise Canceled('canceled')

		passphrase = wofi.show('Enter your network password', True)
		if not passphrase:
			raise Canceled('canceled')

		return (username, passphrase)

	@dbus.service.method('net.connman.iwd.Agent', in_signature='s', out_signature='')
	def Cancel(self, reason):
		print(f'Cancel: {reason}')

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

bus = dbus.SystemBus()
manager = dbus.Interface(
	bus.get_object('net.connman.iwd', '/net/connman/iwd'),
	'net.connman.iwd.AgentManager'
)

path = f'/iwd_wofi/agent/{str(randrange(1000))}'
object = Agent(bus, path)

try:
	manager.RegisterAgent(path)
except:
	exit('Failed to register iwd agent')

mainloop = GLib.MainLoop()
mainloop.run()