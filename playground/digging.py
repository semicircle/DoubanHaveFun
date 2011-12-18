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
    

class Nemo2():
    map_collect_id = """
        function() {
            emit(this.subject['$id'], 1);
        }
    """

    reduce_id_count = """
        function(key, values) {
            var total = 0;
            for (var i=0; i<values.length; i++) {
                total += values[i];
            }
            return total;
       }
    """

    def getMostCommonItems(self):
        results = Collection.objects.map_reduce(self.map_collect_id, self.reduce_id_count, "mostCommon")
        results = sorted(list(results), key = lambda item: item.value)
        return results


def TestCase1():
    x = Nemo()
    #hot = x.getMostCommonItem()
    #print hot
    #for i in range(0, 5):
    #    print hot[i], x.count_items[hot[i]]

TestCase1()
