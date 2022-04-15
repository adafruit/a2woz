# SPDX-FileCopyrightText: 2019 4am
#
# SPDX-License-Identifier: MIT

try:
    from .__version__ import version
except:
    version = "UNKNOWN"

_header = "a2woz " + version
STRINGS = {
    "header":      f"a2woz {version}\n",
    "reading":     "Reading from {filename}\n",
    "writing":     "Writing to {filename}\n",
}
