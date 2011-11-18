import douban
import douban.client
import douban.service
import inspect
import gdata
import atom
import time
from model import *

#use to define: API_KEY, API_SECRET, and tester's access TOKEN_KEY, TOKEN_SECRET.
from privatekeys import *

#get a valid DoubanService obj.
def getDoubanService_priv():
    ds = douban.service.DoubanService(server="api.douban.com",
            api_key = API_KEY, secret = API_SECRET)
    ret = ds.ProgrammaticLogin(token_key = TOKEN_KEY,
            token_secret = TOKEN_SECRET)
    if ret:
        print 'Login Successful'
        return ds
    else:
        return ret
    pass

#dump obj, useless.
def exploreObj(obj):
    for theKey in dir(obj):
        print 'key: ' + str(theKey) 
    pass

#get all friends of obj.
def getFriendsOfUser(ds, userid):
    #url_gen = lambda start_index, max_results : ''.join(['/people/', userid, '/friends?start-index=', `start_index`, '&max-result', `max_results`])
    url_gen = lambda start_index, max_results : ''.join(['/people/', userid, '/contacts?start-index=', `start_index`, '&max-result=', `max_results`])
    start_index = 1
    item_per_req = 10
    ret = []
    while 1:
        #print(url_gen(start_index, item_per_req))
        rsp = ds.GetFriends(url_gen(start_index, item_per_req))
        #print (`len(rsp.entry)`)
        if (len(rsp.entry) > 0):
            ret.extend(rsp.entry)
        else:
            break;
        start_index += item_per_req
    print("".join([`userid`, " have ", `len(ret)`, " friends"]))
    return ret



def getCollectionOfUser1(ds, userid):
    ret = ds.GetCollectionFeed('/people/' + userid + '/collection')
    return ret

def getCollectionOfUser(ds, userid, limit = 0):
    #TODO: collection is not finished.
    #ret = ds.GetCollectionFeed('/people/' + userid + '/collection')
    url_gen = lambda start_index, max_results : ''.join(['/people/', userid, '/collection?start-index=', `start_index`, '&max-results=', `max_results`])
    #url_gen = lambda start_index, max_results : ''.join(['/people/', userid, '/collection?cat=movie'])
    start_index = 1
    item_per_req = 50
    ret = []
    while 1:
        try:
            rsp = ds.GetCollectionFeed(url_gen(start_index, item_per_req))
        except Exception as err:
            print err
            print 'Exceeded.'
            time.sleep(60)
            continue
        print (`len(rsp.entry)`)
        if (len(rsp.entry) > 0):
            ret.extend(rsp.entry)
        else:
            break;
        start_index += item_per_req
        if (limit != 0) and (len(ret) > limit):
            break;
    print("".join(["user: ", `userid`, "'s collection: ", `len(ret)`]))
    return ret

#get the whole dataset.
def getUserBasedDataSet(ds):
    me = ds.GetPeople('/people/%40me') #WTF!@!!!!@!@#!@#
    print me.id.text
    print me.uid.text
    ret = []
    RET_SIZE_LIMIT = 10;
    friends = getFriendsOfUser(ds, 'donotpanic') 
    for peopleEntry in friends:
        xx_collect = getCollectionOfUser(ds, peopleEntry.uid.text, limit=RET_SIZE_LIMIT - len(ret))
        time.sleep(5)
        ret.extend(xx_collect)
        if (len(ret) > RET_SIZE_LIMIT):
            break
        pass
    print("".join(["A Dataset of ", `len(friends)`, " users, ", `len(ret)`, " records has been established."]))
    return ret
    pass

def pred(key):
    return not (inspect.ismethod(key) or inspect.isbuiltin(key))

def inspectEntry(entry):
    for k,v in inspect.getmembers(entry, pred):
        #print k, v.__class__, v
        #if hasattr(v, 'text'):
        if isinstance(v, atom.AtomBase):
            print k, v.__class__, v.text
            for item in v._attributes:
                print item, getattr(v, item)
        if isinstance(v, gdata.GDataEntry):
            inspectEntry(v)

        pass

# this funcation generates a tree as:
# one people to many collection.
# and people model including the collections.
# the whole design changed from here.
def createPeopleBasedDataSet(ds):
    me = ds.GetPeople('/people/%40me')
    friends = getFriendsOfUser(ds, 'donotpanic')

    final_dataset = []

    for peopleEntry in friends:
        peopleObj = People.createFromGData(peopleEntry)
        user_collections = getCollectionOfUser(ds, peopleObj.uid)
        peopleObj.collections = Collection.createListField(user_collections) 
        final_dataset.append(peopleObj)
        #break for test reason.
        #break

    return final_dataset


def testSuite1():
    service = getDoubanService_priv()
    myCollection = getUserBasedDataSet(service)

    for collection in myCollection[1:5]:
        inspectEntry(collection)


    #test 5 obj
    for collection in myCollection[1:5]:
        collectionObj = Collection.createFromGData(collection)
        #save
        #collectionObj.save()
        print collectionObj

    #print myCollection[0].title.text
    #for k,v in inspect.getmembers(myCollection[0].title, pred):
    #    print k, k.__class__, v
    #    print '---'

    #friends = getFriendsOfUser(service, '3985660')
    pass

def testSuite2():
    service = getDoubanService_priv()
    pbds = createPeopleBasedDataSet(service) #pbds stand for People-Based Dataset.:w
    for peopleObj in pbds:
        peopleObj.save()

#testSuite1()

#exploreObj(service)
#friends = getFriendsOfUser(service, '3985660')
#dir(friends)
#print service
#for peopleEntry in friends.entry:
#    print "-----------------------"
    #print unicode(peopleEntry.author)
    #print unicode(peopleEntry.category)
    #print unicode(peopleEntry.content)
#    print unicode(peopleEntry.uid.text)
#    print (peopleEntry.title.text)
#    print peopleEntry.id.text
#    if peopleEntry.location is not None: 
#        print peopleEntry.location.text
#vera_collect = getCollectionOfUser(service, 'Vera_coffee') #this fool collect only movies, ahhh!!!
#vera_collect = getCollectionOfUser(service, '3985660')

#print "======================="
#for item in vera_collect:
#    print item.title.text


testSuite2()


