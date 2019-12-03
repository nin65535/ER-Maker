import json
import random
import numpy as np
import pandas as pd
from Table import Table

class Field(object):

    conf = None

    @classmethod
    def init(cls,no=1):
        conf = open("config%02d.json" % no,"r")
        cls.conf = json.load(conf)

        Table.init(cls.conf)

    def __init__(self,src=None):
        if type(src) == str:
            self.load(src)
        elif type(src) == np.ndarray:
            self.cells = np.array(src)
        else:
            self.init_random()
             
        self._score = None

    def load(self,filename):
        f = open(filename,'r')
        cells = json.load(f)
        self.cells = np.array(cells,dtype=np.int8)
#        self.cells = np.fromfile(f,dtype=np.int8)

    def save(self,filename):
        f = open(filename,'w')
        json.dump(self.cells.tolist(),f)
#        self.cells.tofile(f)

    def init_random(self):
        self.cells = np.zeros(Field.conf["size"],dtype=np.int8)

        for t in range(len(Table.tables)):
            pos = self.find(0)
            self.cells[pos] = t

    def print(self):
        names = np.vectorize(lambda x:Table.tables[x] if x else '-')(self.cells)
        df = pd.DataFrame(names)
        print(df)
        print("total score:%04d" % self.score)

    def rel_map(self,rid):
        map = np.vectorize(lambda x:Table.relations[x][rid])(self.cells)
        return map

    def rel_score(self,rid):
        pos = np.where(self.rel_map(rid))
        rscore = max(pos[0]) - min(pos[0]) + max(pos[1]) - min(pos[1])
        return Field.conf["size"][0] + Field.conf["size"][1] - rscore

    def print_relations(self):
        for rid in range(len(Table.tables)):
            if rid == 0:
                continue
            print("\r")

            print("relation [%s] score:%04d" % (Table.tables[rid],self.rel_score(rid)))
            df = pd.DataFrame(self.rel_map(rid))
            print(df)

    @property
    def score(self):
        if self._score is not None:
            return self._score
        score = 0

        for rid in range(1,len(Table.tables)):
            score += self.rel_score(rid)

        self._score = score
        return self._score

    def swap(self,p1,p2):
        temp = self.cells[p1]
        self.cells[p1] = self.cells[p2]
        self.cells[p2] = temp

    def find(self,value):
        return tuple(random.choice(np.array(np.where(self.cells == value)).transpose()))

    def mutate(self):
        s,a = random.choice([(1,0),
            (-1,0),
            (1,1),
            (-1,1)])
        self.cells = np.roll(self.cells , s , a)
        self._score = None

    @classmethod
    def get_random_area(cls):
        w,h = random.randint(1,int((cls.conf['size'][0] + 1) / 2)),random.randint(1,int((cls.conf['size'][1] + 1) / 2))
        l,t = random.randint(0,cls.conf['size'][0] - w) , random.randint(0,cls.conf['size'][1] - h) 
        area = [(x + l,y + t) for x in range(w)  for y in range(h)]
        random.shuffle(area)
        return area

    @classmethod
    def cross(cls,a,b,area):
        c = Field(a.cells)
        for pos in area:
            if c.cells[pos] != b.cells[pos]:
                c.swap(pos,c.find(b.cells[pos]))

        c._score = None
        return c