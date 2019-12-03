import os
import random
import time
from Field import Field

class Family(object):
    conf_no = None

    @classmethod
    def init(cls,no=1):
        cls.conf_no = no
        Field.init(no)

    def __init__(self):
        self.pool = []
        self.load()
        self.gen = 0

    def load(self):
        fn = "result%02d.json" % Family.conf_no
        if os.path.isfile(fn):
            self.pool.append(Field(fn))
            self.pool[0].print()


    @staticmethod
    def sort_by_score(a):
        a.sort(key=lambda x:x.score)
        return a

    def save(self):
        fn = "result%02d.json" % Family.conf_no
        Family.sort_by_score(self.pool)
        self.pool[-1].save(fn)

    def run(self,gen_max=100):
        time_start = time.time()
        while self.gen < gen_max:
            self.generate()
            Family.sort_by_score(self.pool)
            t = time.time() - time_start 
            print("gen:%04d % 4.2fsec score:%04d \r" % (self.gen ,t, self.pool[-1].score) ,end="")
        self.save()
        print("\r\n")
        a = self.pool[-1]
        a.print()

    def generate(self):
        self.gen += 1

        while len(self.pool) < 2:
            self.pool.append(Field())

        parents = self.get_parents()
        children = self.get_children(parents)

        if children[0].score > parents[1].score:
            self.pool.append(children[0])
            self.pool.append(children[1])
            self.pool.append(parents[1])
            return

        if parents[0].score > children[1].score:
            self.pool.append(parents[1])
            return

        if parents[1].score > children[1].score:
            self.pool.append(children[1])
            self.pool.append(parents[1])
            return

        self.pool.append(children[1])
        self.pool.append(Field())
        return

    def get_parents(self):
        parents = random.sample(self.pool,2)
        self.pool.remove(parents[0])
        self.pool.remove(parents[1])
        return Family.sort_by_score(parents)

    def get_children(self,parents):
        area = Field.get_random_area()
        c1 = Field.cross(parents[0],parents[1],area)
        c2 = Field.cross(parents[1],parents[0],area)
        c2.mutate()
        return Family.sort_by_score([c1,c2])