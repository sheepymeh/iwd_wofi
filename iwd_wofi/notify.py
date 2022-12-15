#!/usr/bin/python3

from dbus_next import Variant

class Notifier:
	def __init__(self, interface, app_name: str = 'iwd_wofi', auto_dismiss: bool = True) -> None:
		self.app_name = app_name
		self.notification_id = 0
		self.auto_dismiss = auto_dismiss
		self.interface = interface

	async def __call__(self, title: str = '', desc: str = '', duration: int = 3000) -> int:
		self.notification_id = await self.interface.call_notify(
			self.app_name, # app_name
			self.notification_id if self.auto_dismiss else 0, # replaces_id
			'', # app_icon
			title, # summary
			desc, # body
			[], # actions
			{'urgency': Variant('i', 1)}, # hints
			duration # expire_timeout
		)
		return self.notification_id

	async def dismiss_notification(self, notification_id: int = 0) -> None:
		await self.interface.call_close_notification(notification_id if notification_id else self.notification_id)