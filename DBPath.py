import pprint
from pymongo import MongoClient
'''
Created on Feb 1, 2017

@author: bleifer
'''

class Query(object):
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
        #self.RecursionCount = count
        #self.existsClause = existsClause
        #self.count = count
        if queryType!='exists':
            print('entered queryType!=exists')
            self.query, self.stepList = (self.traverseQuery(self.bottomLevelQuery(child.field, child.getDBEntry(), queryType),
                                                             child.field, child.getDBEntry(), 
                                                             parentField = parent.field, parentEntry = parent.getDBEntry(),
                                                              stepList = self.bottomLevelQueryList(child.field, child.getDBEntry(), queryType)
                                                              )
                                         )
            
        else:
            print('entered queryType=exists')
            self.query, self.stepList = (self.traverseQuery(self.bottomLevelQuery(child.field, None, queryType), 
                                                            child.field, child.getDBEntry(), 
                                                            parentField = parent.field, parentEntry = parent.getDBEntry(),
                                                            stepList = self.bottomLevelQueryList(child.field, None, queryType)))
        print('The self.query dictionary is: ')
        pprint.pprint(self.query)
        self.currentLevel = {}
    
        
    def bottomLevelQuery(self, searchField, SearchEntry=None, type='exists'):
            query={}
            query[searchField]={}
            stepList = []
            stepList.append(searchField)
            if SearchEntry==None:
                query[searchField]=self.Querytype(type)
            else:
                query[searchField]=SearchEntry
            print('bottom level query is: ')
            pprint.pprint(query)
            return query
        
    def bottomLevelQueryList(self, searchField, SearchEntry=None, type='exists'):
            query={}
            query[searchField]={}
            stepList = []
            stepList.append(searchField)
            if SearchEntry==None:
                query[searchField]=self.Querytype(type)
            else:
                query[searchField]=SearchEntry
            print('bottom level query is: ')
            pprint.pprint(query)
            return stepList
        
    def traverseQuery(self, query, childField, childEntry, parentField= None, parentEntry = None, documentName = None, stepList = [], **kwargs):
        newPathDictSearch = {}
        newPathDictSearch['childField']={}
        newPathDictSearch['childField']=childField
        newPathDictSearch['childEntry']={}
        newPathDictSearch['childEntry']=childEntry
        if parentField is not None:
            newPathDictSearch['parentField']=parentField
        if parentEntry is not None:
            newPathDictSearch['parentEntry']=parentEntry
        randomPath=self.client.test.newPathTest1.find_one({})
        print('randomPath is: ')
        pprint.pprint(randomPath)
        nextPath = self.client.test.newPathTest1.find(newPathDictSearch)
        print('newPathDictSearch is: ')
        pprint.pprint(newPathDictSearch)
        print('nextPath is: ')
        pprint.pprint(nextPath)
        #print('nextPath raw result is: '+str(nextPath.raw_result))
        
        returnList, returnPath = self.categorizeNextPath(nextPath,newPathDictSearch)
        
        print('returnList is: ')
        pprint.pprint(returnList)
        print('returnPath is: ')
        pprint.pprint(returnPath)
        #method to choose path
        returnList = []
        returnPath = []
        nextQueryLevel = {}
        nextQueryLevel[nextPath['DocumentName']]=query
        stepList.append(nextPath['DocumentName'])
        
        if nextPath is not None and childField!=nextPath['parentField'] and childEntry!=nextPath['parentEntry']:
            print('The next Parent Dict is:')
            pprint.pprint(nextPath)
            print('nextQueryLevel is: ')
            pprint.pprint(nextQueryLevel)
            self.traverseQuery(nextQueryLevel, nextPath['parentField'], nextPath['parentEntry'],stepList)
        else:
            return nextQueryLevel, stepList
            print('StepList is: '+stepList)
                
    def categorizeNextPath(self, nextPath, currentPath, returnList=[], returnPath=[]):
        
        for doc in nextPath:
            if doc['parentField']==doc['childField'] and doc['parentEntry']==doc['childEntry']:
                print('Found Dictionary parent')
                returnList.append('dictParent')
                returnPath.append(doc)
            else:
                print('Found Dictionary Child')
                returnList.append('dictChild')
                returnPath.append(doc)
            """
            elif doc==currentPath:
                print('Found Top Level Parent')
                returnList.append('EndPath')
                returnPath.append(doc)
            """
                        
        return returnList, returnPath
    
    def Querytype(self, queryType='exists'):
        
        if queryType =='exists':
            existsClause={}
            existsClause['$exists']=True
            existsClause=existsClause
            queryType = existsClause
            return queryType
        else:
            queryType={}
            print('The queryType specified is invalid')
            return (queryType)
        