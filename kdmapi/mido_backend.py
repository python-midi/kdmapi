#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#

from mido.ports import BaseOutput

from kdmapi import KDMAPI

def get_devices():
	devices = []

	if KDMAPI.IsKDMAPIAvailable():
		maj, min, build, rev = KDMAPI.ReturnKDMAPIVer()
		devices.append({
			'name': f'OmniMIDI {maj}.{min}.{build} Rev. {rev}',
			'is_input': False,
			'is_output': True,
		})

	return devices

class Output(BaseOutput):
	def _open(self, **kwargs):
		KDMAPI.InitializeKDMAPIStream()

	def _close(self):
		KDMAPI.TerminateKDMAPIStream()

	def _send(self, message):
		if message.type == 'sysex':
			# Sysex messages are written as a string.
			KDMAPI.SendDirectLongDataNoBuf(bytes(message.bin()))
		else:
			# The bytes of a message as packed into a 32 bit integer.
			packed_message = 0
			for byte in reversed(message.bytes()):
				packed_message <<= 8
				packed_message |= byte

			KDMAPI.SendDirectData(packed_message)
