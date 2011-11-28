import douban
import douban.client
import douban.service
import inspect
import gdata
import atom
import time
from model import *


#naming: 
#Item: books, music and movie.
#Collection: a relationship between one book and one people.
class Nemo:
    basedata = None
    collections = None
    items = None
    count_items = None
    sorted_items = None
    def loadDataSet(self):
        if not self.basedata:
            self.basedata = People.objects()

    def buildCollectionSet(self):
        if not self.collections:
            self.collections = []
            for people in self.basedata:
                self.collections.extend(people.collections)

    def buildItemSet(self):
        if not self.collections:
            self.buildCollectionSet()
        if not self.items:
            self.items = []
            for item in self.collections:
                self.items.append(item.subject)
    
    def getMostCommonItem(self):
        self.loadDataSet()
        self.buildItemSet()
        if not self.count_items:
            self.count_items = {}
            for item in self.items:
                print 'item.id', item.id, item.title
                if self.count_items.has_key(item.id):
                    self.count_items[item.id] += 1
                else:
                    self.count_items[item.id] = 1
        if not self.sorted_items:
            self.sorted_items = sorted(self.count_items, 
                    cmp = lambda x,y : self.count_items[y] - self.count_items[x])
        return self.sorted_items

def TestCase1():
    x = Nemo()
    hot = x.getMostCommonItem()
    print hot
    #for i in range(0, 5):
    #    print hot[i], x.count_items[hot[i]]

TestCase1()
