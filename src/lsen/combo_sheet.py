import pandas as pd
from .constants import *


class ComboSheet:

    def __init__(self, file_name):
        hl_cols = ['CEMIS No.', 'hl_term_1', 'hl_term_2', 'hl_term_3', 'hl_term_4']
        m_cols = ['CEMIS No.', 'maths_term_1', 'maths_term_2', 'maths_term_3', 'maths_term_4']

        # read in HL1
        self.hl_df = pd.read_excel(file_name, sheet_name=SHEET_HL1, skiprows=11,
                                usecols=[4,55,59,63,70], names=hl_cols)
        self.hl_df.set_index('CEMIS No.', inplace=True)

        # read in MATHS
        self.m_df = pd.read_excel(file_name, sheet_name=SHEET_MATHS, skiprows=11,
                                   usecols=[4,27,29,31,38], names=m_cols)
        self.m_df.set_index('CEMIS No.', inplace=True)

    def get_codes(self, lsen_learners):

        for learner in lsen_learners:
            cemis = learner.cemis

            if cemis in self.hl_df.index:
                codes_lolt = self.hl_df.loc[cemis, ['hl_term_1', 'hl_term_2', 'hl_term_3', 'hl_term_4']].tolist()
                learner.set_lolt_codes(codes=codes_lolt)

            if cemis in self.m_df.index:
                codes_maths = self.m_df.loc[cemis, ['maths_term_1', 'maths_term_2', 'maths_term_3', 'maths_term_4']].tolist()
                learner.set_math_codes(codes=codes_maths)