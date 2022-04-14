# woz rawconvert (was passport.py)

# Theory of a2r to woz raw conversion:

The a2r file contains "1 and a fraction" revolutions, for each track. (It can actually contain multiple revolutions, but ignore that for now)

`passport.py rawconvert` takes a revolution, then finds all the "sync points".
"sync points" are a sequence of 2 or more "FF36" or "FF40", which are used
by the floppy interface controller to synchronize with data on the floppy.

For each pair of sync points within some distance of the start of the capture,
and some distance of the "estimated bit length" of the capture, find the
similarity measure.  A similarity of 1.0 indicates that the next few thousand
bits (at least one full 256-byte sector) are an exact match; a similiary of
0.67 seems to happen for random/fake flux regions.

The pair of sync points with the best similarity is used as the "exact bit length" of the track.
Ties are broken by choosing the resulting track length that is closest to the estimated bit length.
Chop the flux after exactly this many bits, and write it to the output woz file.

That's about all there is to it.

This has worked for a small set of a2r files:

 * Amnesia - Disk 1, Side A.a2r (4am from archive.org)
 * DOS 3.3 System Master [1983] - Disk 1, Side A.a2r (cowgod from archive.org)
 * skyfox.a2r (jepler from fluxengine)

This method doesn't deal with "fake bits"/"weak bits" properly. It could be improved by:

 * Trying different revolutions, if available in the a2r file, hopefully
   finding a single best revolution
 * Properly handling "weak bits" by locating stretches that look like they are
   not valid flux (due to sequences of 3+ zeros), and setting all the bits in
   the region to 0. A proper emulator then generates fake flux for these
   sections of the track.


## TODO

 * Rip out everything that is not 'rawconvert'
 * Come up with an awesome name
 * Share with the world
 * Try more a2rs

