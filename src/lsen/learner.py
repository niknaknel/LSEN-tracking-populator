import pandas as pd
from .constants import *


class Learner:

    def __init__(self, name, surname, grade, cemis, lolt, school_name):
        self.name = name
        self.surname = surname
        self.grade = grade
        self.cemis = cemis
        self.lolt = lolt
        self.school_name = school_name
        self.code_lolt = {}
        self.code_maths = {}

    def set_lolt_codes(self, t1=None, t2=None, t3=None, t4=None, codes=None):
        self.code_lolt = {}

        if codes:
            for i in range(len(codes)):
                key = "t%d" % (i+1)

                try:
                    self.code_lolt[key] = int(codes[i])
                except:
                    self.code_lolt[key] = ''
            return

        if t1:
            self.code_lolt["t1"] = t1
        if t2:
            self.code_lolt["t2"] = t2
        if t3:
            self.code_lolt["t3"] = t3
        if t4:
            self.code_lolt["t4"] = t4

    def set_math_codes(self, t1=None, t2=None, t3=None, t4=None, codes=None):
        self.code_maths = {}

        if codes:
            for i in range(len(codes)):
                key = "t%d" % (i+1)

                try:
                    self.code_maths[key] = int(codes[i])
                except:
                    self.code_maths[key] = ""
            return

        if t1:
            self.code_maths["t1"] = t1
        if t2:
            self.code_maths["t2"] = t2
        if t3:
            self.code_maths["t3"] = t3
        if t4:
            self.code_maths["t4"] = t4

    def get_dict(self):
        data = {COL_SURNAME : self.surname,
                COL_NAME: self.name,
                COL_GRADE: self.grade,
                COL_CEMIS: self.cemis,
                COL_LOLT : self.lolt,
                COL_LOLT_T1 : self.code_lolt['t1'],
                COL_LOLT_T2 : self.code_lolt['t2'],
                COL_LOLT_T3 : self.code_lolt['t3'],
                COL_LOLT_T4 : self.code_lolt['t4'],
                COL_MATHS_T1 : self.code_maths['t1'],
                COL_MATHS_T2 : self.code_maths['t2'],
                COL_MATHS_T3: self.code_maths['t3'],
                COL_MATHS_T4 : self.code_maths['t4']
               }

        return data


    def __unicode__(self):
        return u'{0} {1}, Gr{2}, {3}, {4}, {5}'.format(self.surname, self.name, self.grade,
                                                      self.lolt, self.cemis, self.school_name)

    def __str__(self):
        return unicode(self).encode('utf-8')


