#!/usr/bin/python3

import dbus

interface = dbus.Interface(
	object=dbus.SessionBus().get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications'),
	dbus_interface='org.freedesktop.Notifications'
)

class Notifier:
	def __init__(self, app_name: str = 'iwd_wofi', auto_dismiss: bool = True) -> None:
		self.app_name = app_name
		self.notification_id = 0
		self.auto_dismiss = auto_dismiss

	def __call__(self, title: str = '', desc: str = '', duration: int = 3000) -> int:
		self.notification_id = interface.Notify(
			self.app_name, # app_name
			self.notification_id if self.auto_dismiss else 0, # replaces_id
			'', # app_icon
			title, # summary
			desc, # body
			[], # actions
			{'urgency': 1}, # hints
			duration # expire_timeout
		)
		return self.notification_id

	def dismiss_notification(self, notification_id: int = 0) -> None:
		interface.CloseNotification(notification_id if notification_id else self.notification_id)