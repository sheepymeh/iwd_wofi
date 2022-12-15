#!/usr/bin/python3

import asyncio
from dbus_next.aio import MessageBus
from dbus_next import BusType

from . import menus
from .manager import init
from .agent import start_agent
from .dbus_helper import prepare_dbus

async def show_menu(bus, future):
	adapters, known_networks = await init(bus)
	adapter = adapters[0]
	await menus.main_menu(bus, adapter)
	future.set_result(None)

def main():
	prepare_dbus()
	loop = asyncio.get_event_loop()
	bus = loop.run_until_complete(MessageBus(bus_type=BusType(2)).connect())
	future = loop.create_future()
	try:
		tasks = [
			loop.create_task(start_agent(bus, future)),
			loop.create_task(show_menu(bus, future))
		]
		loop.run_until_complete(asyncio.wait([future]))
	except KeyboardInterrupt:
		future.set_result(None)
	finally:
		loop.run_until_complete(asyncio.wait(tasks))
		loop.close()