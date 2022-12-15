#!/usr/bin/python3

import asyncio

class Wofi:
	def __init__(self):
		self.options = []
		self.values = []

	def add_option(self, option: str, value: str = None):
		self.options.append(option)
		self.values.append(value)

	async def show(self, title: str = 'Wi-Fi', password: bool = False) -> str:
		command = ['wofi', '--dmenu', '-p', title, '-k', '/dev/null']
		if not len(self.options):
			command.extend(['-H', '1', '-b'])
		if password:
			command.extend(['-P"*"'])

		while True:
			process = await asyncio.create_subprocess_exec(
				*command,
				stdin=asyncio.subprocess.PIPE,
				stdout=asyncio.subprocess.PIPE,
				stderr=asyncio.subprocess.DEVNULL,
				shell=False,
				start_new_session=True
			)
			output = await process.communicate(
				input=bytes('\n'.join(self.options), 'utf-8')
			)
			if process.returncode:
				exit()
			output = output[0].decode().strip()
			if len(self.options):
				try:
					idx = self.options.index(output)
				except:
					continue
				value = self.values[idx]
				return output, value
			else:
				return output