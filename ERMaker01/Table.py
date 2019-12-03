import numpy as np
import pandas as pd

class Table(object):

    tables = None
    relations = None

    @classmethod
    def init(cls,conf):
        tables = list(conf["tables"].keys())
        tables.sort()
        tables.insert(0,'None')
        cls.tables = tables

        relations = np.zeros((len(tables),len(tables)),np.bool)
        for tid,tn in enumerate(cls.tables):
            rns = conf["tables"].get(tn)
            if rns is None:
                continue

            for rn in rns:
                rid = tables.index(rn)
                relations[tid][rid] = True

        cls.relations = relations

    @classmethod
    def print(cls):
        df = pd.DataFrame(cls.relations,columns=cls.tables,index=cls.tables)
        print(df)
