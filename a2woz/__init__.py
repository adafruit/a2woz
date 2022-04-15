from .loggers import *
from .strings import *
from .util import *
from . import wozardry
import bitarray
import io
import json
import os.path
import time

class PassportGlobals:
    def __init__(self):
        # things about the disk
        self.track = 0 # display purposes only
        self.sector = 0 # display purposes only
        self.last_track = 0
        self.filename = None

class BasePassportProcessor: # base class
    def __init__(self, filename, disk_image, logger_class=DefaultLogger, output_filename=None):
        self.g = PassportGlobals()
        self.g.filename = filename
        self.g.output_filename = output_filename
        self.g.disk_image = disk_image
        self.g.logger = logger_class(self.g)
        self.rwts = None
        self.output_tracks = {}
        self.burn = 0
        if self.preprocess():
            if self.run():
                self.postprocess()

    def preprocess(self):
        return True

    def run(self):
        return True

    def postprocess(self):
        pass

class RawConvert(BasePassportProcessor):
    def run(self):
        self.g.logger.PrintByID("reading", {"filename":self.g.filename})

        self.tracks = {}

        # main loop - loop through disk from track $22 down to track $00
        for logical_track_num in range(0x22, -1, -1):
            self.g.track = logical_track_num # for display purposes only
            self.g.logger.debug("Seeking to track %s" % hex(self.g.track))

            for fractional_track in (0, .25, .5, .75):

                physical_track_num = logical_track_num + fractional_track
                track = self.g.disk_image.seek(physical_track_num)
                if track and track.bits:
                    track.fix()
                    self.g.logger.debug("Writing to track %s + %.2f for %d bits" % (hex(self.g.track), fractional_track, len(track.bits)))
                    self.output_tracks[physical_track_num] = wozardry.Track(track.bits, len(track.bits))

        return True

    def postprocess(self):
        output_filename = self.g.output_filename
        if output_filename is None:
            source_base, source_ext = os.path.splitext(self.g.filename)
            output_filename = source_base + '.woz'
        self.g.logger.PrintByID("writing", {"filename":output_filename})

        woz_image = wozardry.WozDiskImage()
        json_string = self.g.disk_image.to_json()
        woz_image.from_json(json_string)
        j = json.loads(json_string)
        root = [x for x in j.keys()].pop()
        woz_image.info["creator"] = STRINGS["header"].strip()[:32]
        woz_image.info["synchronized"] = j[root]["info"]["synchronized"]
        woz_image.info["cleaned"] = True #self.g.found_and_cleaned_weakbits
        woz_image.info["write_protected"] = j[root]["info"]["write_protected"]
        woz_image.meta["image_date"] = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
        for q in range(1 + (0x23 * 4)):
            physical_track_num = q / 4
            if physical_track_num in self.output_tracks:
                woz_image.add_track(physical_track_num, self.output_tracks[physical_track_num])
        try:
            wozardry.WozDiskImage(io.BytesIO(bytes(woz_image)))
        except Exception as e:
            raise Exception from e
        with open(output_filename, 'wb') as f:
            f.write(bytes(woz_image))
