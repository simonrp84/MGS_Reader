# MGS_Reader
Some python libraries to record and process data from the IMSRad CZT Spectrometer

The `MGS2.py` file manages the device and records data, with a ten minute acquisition time by default.
The `MGS_Func.py` file contains useful functions for communicating with the device.
The `Parse_MGS2.py` file will convert data output by `MGS2.py` into a user-friendly CSV file.

NOTES:
Nothing is command-line configurable yet, you must edit the files manually to change acquisition times or directory structures.
Only tested on my machine, may not work on yours.
