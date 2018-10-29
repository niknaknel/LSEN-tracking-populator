from os import listdir
from os.path import isfile, join
from lsen import *
import time
from gui import Gui


class Tracker:
    def __init__(self):
        self.gui = Gui(self)
        self.gui.show()

    def read_lsen_list(self, file_name):
        lsen_cemis = []

        with open(file_name, 'r') as f:
            line = f.readline()
            while line:
                line = f.readline().strip()
                lsen_cemis.append(line)

        return lsen_cemis

    def parse_files(self, lsen_cemis, dir="../data/"):
        try:
            files = [f for f in listdir(dir) if isfile(join(dir, f))]
        except:
            raise OSError('Could not parse shared files list!')
        else:
            all_learners = []

            self.gui.set_prog_len(len(files) + 2)

            for f in files:
                # read in excel
                self.gui.inc_prog("reading " + f)
                file_in = dir + f
                info = InfoSheet(file_in)

                # select lsen_learners as list of objects
                lsen_learners = info.get_learners(lsen_cemis)

                if info.type == TYPE_SCHEDULE:
                    schedule = ScheduleSheet(file_in)
                    schedule.get_codes(lsen_learners)

                elif info.type == TYPE_COMBO:
                    combo = ComboSheet(file_in)
                    combo.get_codes(lsen_learners)

                else:
                    continue

                all_learners += lsen_learners

            return all_learners

    def process(self, lst, cemis_path, records_dir, track_path):
        # read in cemis
        self.gui.init_prog()
        lsen_cemis = self.read_lsen_list(cemis_path)

        t0 = time.time()

        # read in learners
        learners = self.parse_files(lsen_cemis, records_dir)

        # get school
        school = (learners[0]).school_name

        # checked missed
        cemis = [l.cemis for l in learners]
        missed = [l for l in lsen_cemis if l not in cemis]

        # export
        self.gui.inc_prog(msg="Exporting tracking file")
        track = TrackingSheet(track_path, lst, school)
        track.export(learners)
        self.gui.complete()

        t1 = time.time()
        elapsed = t1 - t0
        self.gui.display("File written to 'out/'")
        self.gui.display("%d learners processed in %.2fs" % (len(learners), elapsed))

        if len(missed) > 0:
            self.gui.display("Missed: " + str(missed)[1:-1])

if __name__ == "__main__":
    Tracker()