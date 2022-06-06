#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
"""KDMAPI (Keppy's Direct MIDI API) wrapper for Python."""

from ctypes import (
	POINTER,
	c_char_p,
	c_uint,
	c_ulong,
	c_void_p,
	c_wchar_p,
	sizeof,
)
from pathlib import Path
from typing import Any, List

from kdmapi.bindings import (
	DebugInfo,
	MIDIHDR,
	DriverSettings,
	GetDriverDebugInfo,
	IsKDMAPIAvailable,
	InitializeKDMAPIStream,
	LoadCustomSoundFontsList,
	TerminateKDMAPIStream,
	PrepareLongData,
	ResetKDMAPIStream,
	ReturnKDMAPIVer,
	SendCustomEvent,
	SendDirectData,
	SendDirectDataNoBuf,
	SendDirectLongData,
	SendDirectLongDataNoBuf,
	UnprepareLongData,
	modMessage,
)

__version__ = "1.0.1"

module_path = Path(__file__).parent
current_path = Path.cwd()

class KDMAPI:
	@staticmethod
	def ReturnKDMAPIVer() -> List[int]:
		"""Return the KDMAPI version from OmniMIDI as the following output: Major.Minor.Build Rev. Revision (eg. 1.30.0 Rev. 51)."""
		vers = [POINTER(c_ulong)(c_ulong(0)) for _ in range(4)]

		result = ReturnKDMAPIVer(*vers)
		if not result:
			raise Exception("ReturnKDMAPIVer failed")

		return [ver.contents.value for ver in vers]

	@staticmethod
	def IsKDMAPIAvailable() -> bool:
		"""Checks if KDMAPI is available. You can ignore the output if you want, but you should give the user the choice between WinMM and KDMAPI."""
		return IsKDMAPIAvailable()

	@staticmethod
	def InitializeKDMAPIStream() -> bool:
		"""Initializes OmniMIDI through KDMAPI. (Like midiOutOpen)"""
		result = InitializeKDMAPIStream()
		if not result:
			raise Exception("InitializeKDMAPIStream failed")
		return True

	@staticmethod
	def TerminateKDMAPIStream() -> bool:
		"""Closes OmniMIDI through KDMAPI. (Like midiOutClose)"""
		result = TerminateKDMAPIStream()
		if not result:
			raise Exception("TerminateKDMAPIStream failed")
		return True

	@staticmethod
	def ResetKDMAPIStream() -> None:
		"""Resets OmniMIDI and all its MIDI channels through KDMAPI. (Like midiOutReset)"""
		ResetKDMAPIStream()

	@staticmethod
	def SendCustomEvent(event_type: int, channel: int, param: int) -> bool:
		"""Send short messages through KDMAPI. (Like midiOutShortMsg)"""
		return SendCustomEvent(c_ulong(event_type), c_ulong(channel), c_ulong(param))

	@staticmethod
	def SendDirectData(message: int) -> None:
		"""Send short messages through KDMAPI. (Like midiOutShortMsg)"""
		return SendDirectData(c_ulong(message))

	@staticmethod
	def SendDirectDataNoBuf(message: int) -> None:
		"""Send short messages through KDMAPI like SendDirectData, but bypasses the buffer. (Like midiOutShortMsg)"""
		return SendDirectDataNoBuf(c_ulong(message))

	@staticmethod
	def SendDirectLongData(data: MIDIHDR) -> int:
		"""Send long messages through KDMAPI. (Like midiOutLongMsg)"""
		data_locked = POINTER(data)
		PrepareLongData(data_locked)
		result = SendDirectLongData(data_locked, c_uint(sizeof(data)))
		UnprepareLongData(data_locked)
		return result

	@staticmethod
	def SendDirectLongDataNoBuf(data: bytes) -> int:
		"""Send long messages through KDMAPI like SendDirectLongData, but bypasses the buffer. (Like midiOutLongMsg)"""
		return SendDirectLongDataNoBuf(c_char_p(data), c_ulong(len(data)))

	@staticmethod
	def DriverSettings(setting: int, mode: int, value: Any, cb_value: int) -> int:
		"""Get or set the current settings for the driver."""
		return DriverSettings(c_ulong(setting), c_ulong(mode), c_void_p(value), c_uint(cb_value))

	@staticmethod
	def GetDriverDebugInfo() -> DebugInfo:
		"""Get a pointer to the debug info of the driver."""
		return GetDriverDebugInfo().contents

	@staticmethod
	def LoadCustomSoundFontsList(directory: Path) -> None:
		"""Load a custom sflist. (You can also load SF2 and SFZ files)"""
		return LoadCustomSoundFontsList(c_wchar_p(str(directory)))

	@staticmethod
	def modMessage(device_id: int, message: int, user: int, param1: int, param2: int) -> None:
		"""modMessage"""
		return modMessage(c_uint(device_id), c_uint(message), POINTER(c_ulong(user)),
				POINTER(c_ulong(param1)), POINTER(c_ulong(param2)))
