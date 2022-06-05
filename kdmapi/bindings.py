#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
"""
OmniMIDI.dll C bindings for Python.

Source: https://github.com/KeppySoftware/OmniMIDI/blob/master/DeveloperContent/OmniMIDI.h
"""

from ctypes import (
	CDLL,
	POINTER,
	Structure,
	c_bool,
	c_char_p,
	c_double,
	c_float,
	c_int,
	c_uint,
	c_uint64,
	c_ulong,
	c_void_p,
	c_wchar_p,
)
from enum import IntEnum

_dll_name = "OmniMIDI.dll"
_lib = CDLL(_dll_name)

class MIDIHDR(Structure):
	pass

class MIDIHDR(Structure):
	_pack_ = 1
	_fields_ = [
		("lpdata", c_char_p),
		("dwBufferLength", c_uint),
		("dwBytesRecorded", c_uint),
		("dwUser", POINTER(c_int)),
		("dwFlags", c_uint),
		("lpNext", POINTER(MIDIHDR)),
		("reserved", POINTER(c_int)),
		("dwOffset", c_uint),
		("dwReserved", POINTER(c_int)),
	]

class DebugInfo(Structure):
	_pack_ = 1
	_fields_ = [
		("RenderingTime", c_float),
		("ActiveVoices", c_uint * 16),
		("ASIOInputLatency", c_double),
		("ASIOOutputLatency", c_double),
		("HealthThreadTime", c_double),
		("ATThreadTime", c_double),
		("EPThreadTime", c_double),
		("CookedThreadTime", c_double),
		("CurrentSFList", c_uint),
		("AudioLatency", c_double),
		("AudioBufferSize", c_uint),
	]

class MMRESULT(IntEnum):
	MMSYSERR_NOERROR = 0
	MMSYSERR_ERROR = 1
	MMSYSERR_BADDEVICEID = 2
	MMSYSERR_NOTENABLED = 3
	MMSYSERR_ALLOCATED = 4
	MMSYSERR_INVALHANDLE = 5
	MMSYSERR_NODRIVER = 6
	MMSYSERR_NOMEM = 7
	MMSYSERR_NOTSUPPORTED = 8
	MMSYSERR_BADERRNUM = 9
	MMSYSERR_INVALFLAG = 10
	MMSYSERR_INVALPARAM = 11
	MMSYSERR_HANDLEBUSY = 12
	MMSYSERR_INVALIDALIAS = 13
	MMSYSERR_BADDB = 14
	MMSYSERR_KEYNOTFOUND = 15
	MMSYSERR_READERROR = 16
	MMSYSERR_WRITEERROR = 17
	MMSYSERR_DELETEERROR = 18
	MMSYSERR_VALNOTFOUND = 19
	MMSYSERR_NODRIVERCB = 20
	WAVERR_BADFORMAT = 32
	WAVERR_STILLPLAYING = 33
	WAVERR_UNPREPARED = 34

"""
// Return the KDMAPI version from OmniMIDI as the following output: Major.Minor.Build Rev. Revision (eg. 1.30.0 Rev. 51).
BOOL KDMAPI(ReturnKDMAPIVer)(LPDWORD Major, LPDWORD Minor, LPDWORD Build, LPDWORD Revision);
"""
ReturnKDMAPIVer = _lib.ReturnKDMAPIVer
ReturnKDMAPIVer.argtypes = [POINTER(c_ulong), POINTER(c_ulong), POINTER(c_ulong), POINTER(c_ulong)]
ReturnKDMAPIVer.restype = c_bool

"""
// Checks if KDMAPI is available. You can ignore the output if you want, but you should give the user the choice between WinMM and KDMAPI.
BOOL KDMAPI(IsKDMAPIAvailable)();
"""
IsKDMAPIAvailable = _lib.IsKDMAPIAvailable
IsKDMAPIAvailable.argtypes = []
IsKDMAPIAvailable.restype = c_bool

"""
// Initializes OmniMIDI through KDMAPI. (Like midiOutOpen)
BOOL KDMAPI(InitializeKDMAPIStream)();
"""
InitializeKDMAPIStream = _lib.InitializeKDMAPIStream
InitializeKDMAPIStream.argtypes = []
InitializeKDMAPIStream.restype = c_bool

"""
// Closes OmniMIDI through KDMAPI. (Like midiOutClose)
BOOL KDMAPI(TerminateKDMAPIStream)();
"""
TerminateKDMAPIStream = _lib.TerminateKDMAPIStream
TerminateKDMAPIStream.argtypes = []
TerminateKDMAPIStream.restype = c_bool

"""
// Resets OmniMIDI and all its MIDI channels through KDMAPI. (Like midiOutReset)
VOID KDMAPI(ResetKDMAPIStream)();
"""
ResetKDMAPIStream = _lib.ResetKDMAPIStream
ResetKDMAPIStream.argtypes = []
ResetKDMAPIStream.restype = None

"""
// Send short messages through KDMAPI. (Like midiOutShortMsg)
BOOL KDMAPI(SendCustomEvent)(DWORD eventtype, DWORD chan, DWORD param) noexcept;
"""
SendCustomEvent = _lib.SendCustomEvent
SendCustomEvent.argtypes = [c_ulong, c_ulong, c_ulong]
SendCustomEvent.restype = c_bool

"""
// Send short messages through KDMAPI. (Like midiOutShortMsg)
VOID KDMAPI(SendDirectData)(DWORD dwMsg);
"""
SendDirectData = _lib.SendDirectData
SendDirectData.argtypes = [c_ulong]
SendDirectData.restype = None

"""
// Send short messages through KDMAPI like SendDirectData, but bypasses the buffer. (Like midiOutShortMsg)
VOID KDMAPI(SendDirectDataNoBuf)(DWORD dwMsg);
"""
SendDirectDataNoBuf = _lib.SendDirectDataNoBuf
SendDirectDataNoBuf.argtypes = [c_ulong]
SendDirectDataNoBuf.restype = None

"""
// Send long messages through KDMAPI. (Like midiOutLongMsg)
UINT KDMAPI(SendDirectLongData)(MIDIHDR* IIMidiHdr, UINT IIMidiHdrSize);
"""
SendDirectLongData = _lib.SendDirectLongData
SendDirectLongData.argtypes = [POINTER(MIDIHDR), c_uint]
SendDirectLongData.restype = c_uint

"""
// Send long messages through KDMAPI like SendDirectLongData, but bypasses the buffer. (Like midiOutLongMsg)
UINT KDMAPI(SendDirectLongDataNoBuf)(LPSTR MidiHdrData, DWORD MidiHdrDataLen);
"""
SendDirectLongDataNoBuf = _lib.SendDirectLongDataNoBuf
SendDirectLongDataNoBuf.argtypes = [c_char_p, c_ulong]
SendDirectLongDataNoBuf.restype = c_uint

"""
// Prepares the long data, and locks its memory to prevent apps from writing to it.
UINT KDMAPI(PrepareLongData)(MIDIHDR* IIMidiHdr, UINT IIMidiHdrSize);
"""
PrepareLongData = _lib.PrepareLongData
PrepareLongData.argtypes = [POINTER(MIDIHDR), c_uint]
PrepareLongData.restype = c_uint

"""
// Unlocks the memory, and unprepares the long data.
UINT KDMAPI(UnprepareLongData)(MIDIHDR* IIMidiHdr, UINT IIMidiHdrSize);
"""
UnprepareLongData = _lib.UnprepareLongData
UnprepareLongData.argtypes = [POINTER(MIDIHDR), c_uint]
UnprepareLongData.restype = c_uint

"""
// Get or set the current settings for the driver.
BOOL KDMAPI(DriverSettings)(DWORD Setting, DWORD Mode, LPVOID Value, UINT cbValue);
"""
DriverSettings = _lib.DriverSettings
DriverSettings.argtypes = [c_ulong, c_ulong, c_void_p, c_uint]
DriverSettings.restype = c_bool

"""
// Get a pointer to the debug info of the driver.
DebugInfo* KDMAPI(GetDriverDebugInfo)();
"""
GetDriverDebugInfo = _lib.GetDriverDebugInfo
GetDriverDebugInfo.argtypes = []
GetDriverDebugInfo.restype = POINTER(DebugInfo)

"""
// Load a custom sflist. (You can also load SF2 and SFZ files)
VOID KDMAPI(LoadCustomSoundFontsList)(LPWSTR Directory);
"""
LoadCustomSoundFontsList = _lib.LoadCustomSoundFontsList
LoadCustomSoundFontsList.argtypes = [c_wchar_p]
LoadCustomSoundFontsList.restype = None

"""
// timeGetTime, but 64-bit
DWORD64 KDMAPI(timeGetTime64)();
"""
timeGetTime64 = _lib.timeGetTime64
timeGetTime64.argtypes = []
timeGetTime64.restype = c_uint64

"""
// modMessage
MMRESULT KDMAPI(modMessage)(UINT uDeviceID, UINT uMsg, DWORD_PTR dwUser, DWORD_PTR dwParam1, DWORD_PTR dwParam2);
"""
modMessage = _lib.modMessage
modMessage.argtypes = [c_uint, c_uint, POINTER(c_ulong), POINTER(c_ulong), POINTER(c_ulong)]
modMessage.restype = MMRESULT
