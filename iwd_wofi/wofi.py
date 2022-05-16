#!/usr/bin/python3

from subprocess import check_output

class Wofi:
	def __init__(self):
		self.options = []
		self.values = []

	def add_option(self, option: str, value: str = None):
		self.options.append(option)
		self.values.append(value)

	def show(self, title: str = 'Wi-Fi', password: bool = False) -> str:
		command = ['wofi', '-dmenu', '-p', title, '-k', '/dev/null']
		if not len(self.options):
			command.extend(['-L', '0'])
		if password:
			command.extend(['--password', '•'])

		if len(self.options):
			while True:
				choice = check_output(command, input=bytes('\n'.join(self.options), 'utf-8')).decode('utf-8').strip()
				try:
					idx = self.options.index(choice)
				except:
					continue
				value = self.values[idx]
				return choice, value
		else:
			return check_output(command, input=bytes('\n'.join(self.options), 'utf-8')).decode('utf-8').strip()