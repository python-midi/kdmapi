# kdmapi

[![PyPi version](https://img.shields.io/pypi/v/kdmapi)](https://pypi.org/project/kdmapi/)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/1a367d8d58e34eb6a86b860d1513081f)](https://www.codacy.com/gh/python-midi/kdmapi/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=python-midi/kdmapi&amp;utm_campaign=Badge_Grade)

[KDMAPI (Keppy's Direct MIDI API)](https://github.com/KeppySoftware/OmniMIDI/blob/master/DeveloperContent/KDMAPI.md) wrapper for Python

kdmapi provides both C bindings for OmniMIDI.dll and a Python-friendly wrapper for them

A [Mido](https://pypi.org/project/mido/) backend is also provided, instructions on how to use it are below

Requires Python 3.8 or greater

## Installation

```sh
pip3 install kdmapi
```

You will also need to have [OmniMIDI](https://github.com/KeppySoftware/OmniMIDI) installed

## Instructions

```python
from kdmapi import KDMAPI

# Initialize the device
KDMAPI.InitializeKDMAPIStream()

# Send a short 32-bit MIDI message data
KDMAPI.SendDirectData(0x0)

# Close the device
KDMAPI.TerminateKDMAPIStream()
```

## Mido backend

You can use KDMAPI as a [Mido](https://pypi.org/project/mido/) output backend

```python
import mido

# Set KDMAPI as MIDO backend
mido.set_backend("kdmapi.mido_backend")

# Open MIDI file
midi_file = mido.MidiFile("your_file.mid")

with mido.open_output() as out:
    for msg in midi_file.play():
        out.send(msg)
```

## License

```
#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
```
