import pandas as pd
from .constants import *


class ScheduleSheet:

    def __init__(self, file_name):
        cols = ['CEMIS No.', 'hl_term_1', 'hl_term_2', 'hl_term_3', 'hl_term_4',
                'maths_term_1', 'maths_term_2', 'maths_term_3', 'maths_term_4']
        self.df = pd.read_excel(file_name, sheet_name=SHEET_SCHEDULE, skiprows=10,
                                usecols=[4,11,12,13,14,21,22,23,24], names=cols)
        self.df.set_index('CEMIS No.', inplace=True)

    def get_codes(self, lsen_learners):

        for learner in lsen_learners:
            cemis = learner.cemis

            if cemis in self.df.index:
                codes_lolt = self.df.loc[cemis, ['hl_term_1', 'hl_term_2', 'hl_term_3', 'hl_term_4']].tolist()
                codes_maths = self.df.loc[cemis, ['maths_term_1', 'maths_term_2', 'maths_term_3', 'maths_term_4']].tolist()
                learner.set_lolt_codes(codes=codes_lolt)
                learner.set_math_codes(codes=codes_maths)

