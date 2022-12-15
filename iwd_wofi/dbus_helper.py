#!/usr/bin/python3

from dbus_next import Variant

def prepare_dbus():
	def variant_eq(self, other):
		if type(other) is Variant:
			return self.signature == other.signature and self.value == other.value
		else:
			return self.value == other

	def variant_bool(self):
		return bool(self.value)

	def variant_len(self):
		return len(self.value)

	def variant_str(self):
		return str(self.value)

	setattr(Variant, '__eq__', variant_eq)
	setattr(Variant, '__bool__', variant_bool)
	setattr(Variant, '__len__', variant_len)
	setattr(Variant, '__str__', variant_str)

async def dbus_proxy(bus, path, bus_name='net.connman.iwd'):
	introspection = await bus.introspect(bus_name, path)
	return bus.get_proxy_object(bus_name, path, introspection)