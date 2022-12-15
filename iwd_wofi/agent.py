#!/usr/bin/python3

from random import randrange

from dbus_next.service import ServiceInterface, method
from dbus_next import DBusError

from .wofi import Wofi
from .dbus_helper import dbus_proxy

wofi = Wofi()

class Canceled(DBusError):
	def __init__(self, err: str):
		super().__init__('net.connman.iwd.Error.Canceled', err)

class Agent(ServiceInterface):
	def __init__(self, bus):
		super().__init__('net.connman.iwd.Agent')
		self.bus = bus

	@method()
	async def Release(self) -> '':
		await self.bus.wait_for_disconnect()

	@method()
	async def RequestPassphrase(self, path: 'o') -> 's':
		passphrase = await wofi.show('Enter your Wi-Fi password', True)
		if not passphrase:
			raise Canceled('canceled')

		return passphrase

	@method()
	async def RequestPrivateKeyPassphrase(self, path: 'o') -> 's':
		passphrase = await wofi.show('Enter your key passphrase', True)
		if not passphrase:
			raise Canceled('canceled')

		return passphrase

	@method()
	async def RequestUserNameAndPassword(self, path: 'o') -> 'ss':
		username = await wofi.show('Enter your network username')
		if not username:
			raise Canceled('canceled')

		passphrase = await wofi.show('Enter your network password', True)
		if not passphrase:
			raise Canceled('canceled')

		return (username, passphrase)

	@method()
	def Cancel(self, reason: 's') -> '':
		print(f'Cancel: {reason}')

async def start_agent(bus, future):
	path = f'/iwd_wofi/agent/{str(randrange(1000))}'
	agent = Agent(bus)
	bus.export(path, agent)

	proxy_object = await dbus_proxy(bus, '/net/connman/iwd')
	manager = proxy_object.get_interface('net.connman.iwd.AgentManager')
	await manager.call_register_agent(path)

	await future
	await manager.call_unregister_agent(path)