import pandas as pd
from .constants import *
from .learner import Learner


class InfoSheet:

    def __init__(self, file_name):
        self.df = pd.read_excel(file_name, sheet_name=SHEET_INFO, skiprows=5, usecols=[1,2,3,4,9])
        self.school_name = pd.read_excel(file_name, sheet_name=SHEET_INFO).iloc[1, 4]
        grade = pd.read_excel(file_name, sheet_name=SHEET_INFO).iloc[1, 8]

        if 1 <= grade <= 3:
            self.type = TYPE_SCHEDULE
        else:
            self.type = TYPE_COMBO

    def get_school_name(self):
        return self.school_name

    def get_learners(self, lsen_cemis):
        filtered = self.df.loc[self.df['CEMIS No.'].isin(lsen_cemis)]
        l_f = filtered.apply(self.create_learner, axis=1)
        return l_f.tolist()

    def create_learner(self, args):
        surname = args[0]
        name = args[1]
        gr = self.parse_class_group(args[2])
        cemis = args[3]
        lolt = args[4]
        return Learner(name, surname, gr, cemis, lolt, self.school_name)

    @classmethod
    def parse_class_group(cls, class_group):
        gr = (class_group.strip()).split(' ')[0]
        grade = gr[2]
        return grade
