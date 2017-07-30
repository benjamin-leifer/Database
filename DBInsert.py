import pprint
from pymongo import MongoClient
'''
Created on Feb 1, 2017

@author: bleifer
'''

class Path(object):
    '''
    classdocs
    '''


    def __init__(self, client, child, parent, queryType='exists'):
        '''
        Constructor
        '''
        self.client = client
        self.child = child
        self.parent = parent
        self.currentLevel
        #self.RecursionCount = count
        #self.existsClause = existsClause
        #self.count = count
        if queryType!='exists':
            self.query = (lambda: self.traverseQuery(self.bottomLevelQuery(child.field, child.getDBEntry(), queryType), parent.field, parent.getDBEntry()))
        else:
            self.query = (lambda: self.traverseQuery(self.bottomLevelQuery(child.field, None, queryType), parent.field, None))
    
        
    def bottomLevelQuery(self, searchField, SearchEntry=None, type='exists'):
            query={}
            query[searchField]={}
            if SearchEntry==None:
                query[searchField]=self.Querytype(type)
            else:
                query[searchField]=SearchEntry
            return query
        
    def traverseQuery(self, query, parentField, parentEntry, **kwargs):
        newPathDictSearch = {}
        newPathDictSearch[parentField]={}
        newPathDictSearch[parentField]=parentEntry
        nextPath = self.client.db.test.newPathTest1.find_one(newPathDictSearch)
            
        if nextPath is not None:
            print('The next Parent Dict is:')
            pprint.pprint(nextPath)
            nextQueryLevel = {}
            nextQueryLevel[nextPath['DocumentName']]=query
            self.traverseQuery(nextQueryLevel, nextPath['ParentField'], nextPath['parentEntry'])
        else:
            return query
                
                
    def Querytype(self, type='exists'):
        
        if type =='exists':
            existsClause={}
            existsClause['$exists']=True
            existsClause=existsClause
            queryType = existsClause
            return queryType
        else:
            queryType={}
            print('The queryType specified is invalid')
            return (queryType)
        