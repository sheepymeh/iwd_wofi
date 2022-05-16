#!/usr/bin/python3

import dbus

interface = dbus.Interface(
	object=dbus.SessionBus().get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications'),
	dbus_interface='org.freedesktop.Notifications'
)

def notify(title: str = '', desc: str = ''):
	interface.Notify('iwd_wofi', 0, '', title, desc, [], {'urgency': 1}, 3000)