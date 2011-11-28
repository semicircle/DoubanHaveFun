from mongoengine import *
import douban
import douban.client
import douban.service
import datetime

connect('doubanhavefun')

class createFromGData_MixIn:

    #help used to get the attrNameList in a mongoengine's model.
    @staticmethod
    def getAttrNameListOfModel(modelCls):
        ret = []
        for key in modelCls._fields:
            ret.append(key)
        return ret

    #same as the one with Attr.
    @staticmethod
    def getAttrNameListOfModelObj(modelObj):
        ret = []
        for key in modelObj._data:
            ret.append(key)
        return ret

    #used to assign mongoengine's modelObj with GDataObj's attr value.
    @staticmethod
    def assignAttrWithGDataObj(modelObj, GDataObj, attrNameList=None):
        if not attrNameList:
            attrNameList = createFromGData_MixIn.getAttrNameListOfModel(modelObj.__class__)
        #print '[attrNameList]', attrNameList
        for attrName in attrNameList:
            typeOfModel = type(modelObj.__class__._fields[attrName])
            gDataObj = getattr(GDataObj, attrName, None)
            #print attrName, typeOfModel, gDataObj
            if not gDataObj:
                continue
            else:
                if typeOfModel is StringField:
                    if hasattr(gDataObj, 'text'):
                        setattr(modelObj, attrName, unicode(gDataObj.text, 'utf-8'))
                    else:
                        setattr(modelObj, attrName, unicode(gDataObj, 'utf-8'))
                if typeOfModel is IntField:
                    setattr(modelObj, attrName, int(gDataObj))
                if typeOfModel is FloatField:
                    setattr(modelObj, attrName, float(gDataObj))
            pass
        pass

    #ListField jobs.
    #classmethod.
    #para:
    @classmethod
    def createListField(cls, dbList):
        modelList = []
        for item in dbList:
            modelObj = cls()
            cls.assignAttrWithGDataObj(modelObj, item)
            cls._fillSpecialAttr(modelObj, item)
            modelList.append(modelObj)
        return modelList

    @classmethod
    def createFromGData(cls, dbThing):
        inst = cls()
        createFromGData_MixIn.assignAttrWithGDataObj(inst, dbThing)
        cls._fillSpecialAttr(inst, dbThing)
        return inst

    @classmethod
    def _fillSpecialAttr(cls, inst, dbThing):
        #wish nothing here.
        pass


class Tag(EmbeddedDocument, createFromGData_MixIn):
    count = StringField()
    name = StringField()

class Rating(EmbeddedDocument, createFromGData_MixIn):
    max = IntField()
    min = IntField()
    numRaters = IntField()
    average = FloatField()
    value = FloatField() 

class Subject(Document, createFromGData_MixIn):
    title = StringField()
    id = StringField(primary_key=True)
    #for numbers with point.
    rating = EmbeddedDocumentField(Rating)
    #author is a vaild field in douban's data model, but api didn't give us the detail.
    author = ListField(StringField())
    #tag is a valid field.
    tags = ListField(EmbeddedDocumentField(Tag))

    @classmethod
    def _fillSpecialAttr(cls, inst, dbSubject):
        inst.rating = Rating.createFromGData(dbSubject.rating)
        if hasattr(dbSubject, 'tags'):
            inst.tags = Tag.createListField(dbSubject.tags)

class Collection(Document, createFromGData_MixIn):
    #relationship, this two fields will not be generate from the gdata.
    subject = ReferenceField(Subject)
    user = ReferenceField('People') 
    #info
    id = StringField(primary_key=True)
    title = StringField()
    rating = EmbeddedDocumentField(Rating)
    status = StringField()
    tags = ListField(EmbeddedDocumentField(Tag))

    @classmethod
    def _fillSpecialAttr(cls, inst, dbThing):
        inst.rating = Rating.createFromGData(dbThing.rating)
        #inst.subject = Subject.createFromGData(dbThing.subject)
        inst.tags = Tag.createListField(dbThing.tags)

class People(Document, createFromGData_MixIn):
    uid = StringField(primary_key=True)
    title = StringField()
    location = StringField()
    link = ListField(StringField())
    alterlink = StringField()
    #NOTE: this field is not from GDataObj directly.
    collections = ListField(ReferenceField(Collection))

