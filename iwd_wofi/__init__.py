#!/usr/bin/python3

import os
from subprocess import Popen
from signal import SIGTERM

import menus
from manager import init

agent = Popen(('/usr/bin/python3', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'agent.py')), preexec_fn=os.setsid)

try:
	adapters, known_networks = init()
	adapter = adapters[0]
	menus.main_menu(adapter)
finally:
	os.killpg(os.getpgid(agent.pid), SIGTERM)