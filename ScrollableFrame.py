'''
Created on Feb 1, 2017

@author: bleifer
'''
#import tkinter as tk
import collections as coll
from pymongo import MongoClient
import functools
import re
import matplotlib.pyplot as plt
import numpy
import random
import DBLabelEntry
#import ScrolledWindow
import tkinter.tix as tk
#from ScrollableFrameHelper import *
import pprint
from _overlapped import NULL
#from tutorial.root import nested
from pandas.core.config import _get_root
from tkinter.tix import LabelEntry

class ScrollableEntryForm(tk.Frame):
    def __init__(self, root,sheetDict, **config):

        tk.Frame.__init__(self, root, **config)
        """
        self.canvas = tk.Canvas(root, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.hsb = tk.Scrollbar(root, orient="horizontal",command = self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.hsb.set)
        self.vsb = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.hsb.pack(side="bottom", fill="x")
        self.vsb.pack(side="right", fill="y")

        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)
        """
        self.client=MongoClient()
        self.listProceed = False
        self.listCount = 0
        self.curListLength = 0
        self.viewList=[]
        self.populate(sheetDict)
        
        #printButton = tk.Button(self,text='Print',command = lambda: self.OnPrint(lambda: self.lambdaMakeDict(searchField.get(), searchField.get())))
        printButton = tk.Button(self, text = 'Print', command = lambda:self.OnPrint())
        printButton.grid(row=0,column=0)
        submitButton = tk.Button(self, text='Submit', command = self.OnSubmit)
        submitButton.grid(row=0,column=1)
        autofillButton = tk.Button(self, text = 'Autofill', command= self.OnAutofill)
        autofillButton.grid(row=0,column=2)
        saveButton = tk.Button(self, text = 'Save', command= self.OnSave3)
        saveButton.grid(row=0,column=3)
        randomGenButton=tk.Button(self, text = 'randPop', command = lambda:self.randomPop())
        randomGenButton.grid(row=0,column=4)
        self.randomPopList = ['a', 'b', 'c', 'd', 'e']
        """
        searchFieldVar = tk.StringVar()
        searchEntryVar = tk.StringVar()
        searchField = tk.Entry(self,textvariable=searchFieldVar)
        searchEntry = tk.Entry(self,textvariable=searchEntryVar)
        searchField.grid(row=0,column=4)
        searchEntry.grid(row=0,column=5)
        """
        
        #self.frame.bind("<Configure>", self.onFrameConfigure)
        """
        menu = tk.Menu(root) #Adds menu to window
        root.config(menu=menu)

        file = tk.Menu(menu) #instantiate file dropdown for menu
        file.add_command(label = 'Print', command = self.OnSubmit) #adds options to file dropdown
        file.add_command(label='Load', command = self.OnAutofill)
        file.add_command(label='Save', command = self.OnSave)
        menu.add_cascade(label='File', menu=file)#adds file dropdown to menu

        analysis = tk.Menu(menu)
        analysis.add_command(label='Graph', command = self.OnSubmit)
        menu.add_cascade(label='Analysis',menu=analysis)
        """


    def OnSubmit(self):
        holderDict1 = {}
        holderDict ={}
        for labelentry in self.viewList:
            holderDict1[labelentry.field]=labelentry.getDBEntry()
        print (holderDict1)
        return

    def OnAutofill(self):
        findDict = {}
        holderDict1 = {}
        holderDict ={}
        for labelentry in self.viewList:
            holderDict1[labelentry.field]=labelentry.getDBEntry()
        print (holderDict1)
        for k,v in holderDict1.items():
            holderList=[]
            holderDict={}
            for val in v:
                if (val!=''):
                    holderList.append(val)
                    holderDict[k]=holderList
                findDict.update(holderDict)
        checkDict = {}
        for k, v in findDict.items():
            nullcount = 0
            for val in v:
                if (val==''):
                    nullcount = nullcount+1
            if (nullcount == len(v)):
                checkDict[k]=v
        for k,v in checkDict.items():
            findDict.pop(k, None)
        print(findDict)
        client = MongoClient()
        db = client.test
        found = db.operationsTest2.find_one(findDict,{'_id': False}) #pull single dictionary from db
        print (found)

        for k,v in found.items(): #set StringVars to new strings from database
            """
            listcount = 0
            for val in v:
                self.viewList[k][listcount].set(str(val))
                listcount=listcount+1
            """
            for labelentry in self.viewList:
                if labelentry.field == k:
                    labelentry.setDBEntry(v)

        return

    def aggregateByParent(self):
        print ('entered aggregateByParent')
        print ('self.viewList is:')
        pprint.pprint(self.viewList)
        listOfDicts = []
        count = 0
        for labelentry in self.viewList:
            holderDict = {}
            if labelentry.designateParent == labelentry.field:
                holderDict[labelentry]={}
                listOfDicts.append(holderDict)
        print('list of Dicts is now: ')
        pprint.pprint(listOfDicts)
        
        for labelentry in self.viewList:
            count=count+1
            print ('entered Loop #'+str(count))
            print ('looking at '+ labelentry.field)
            parent = labelentry.parent
            """
            if not listOfDicts:
                print ('entered empty list loop')
                holderDict = {}
                holderDict['parent'] = parent
                holderDict[labelentry.field]=[labelentry.getDBEntry()]
                listOfDicts.append(holderDict)
                print (listOfDicts)
            """
            holderDict = {}
            for dictionary in listOfDicts:
                print ('entered filled list loop')
                for k,v in dictionary.items():
                    #holderDict = {}
                    if parent == k.getDBEntry():
                        print ('parent match found')
                        print(dictionary[k])
                        """
                        holderDict[labelentry.field]=labelentry.getDBEntry()
                        dictionary[k].append(holderDict)
                        """
                        holderDict={}
                        holderDict[labelentry.field]=labelentry.getDBEntry()
                        dictionary[k].update(holderDict)
                        pprint.pprint(listOfDicts)
                """
                else:
                    print ('parent Match not found')
                    holderDict = {}
                    holderDict['parent'] = parent
                    holderDict[labelentry.field]=[labelentry.getDBEntry()]
                    listOfDicts.append(holderDict)
                    print (listOfDicts)
                """
        newlistOfDicts = []
        newlistOfDicts2 = []
        for dictionary in listOfDicts:
            for k,v in dictionary.items():
                print('entered new processing loop')
                documentNameLevel = {}
                documentNameLevel[k.parentObject.parentDict]=[]
                documentLevel = {}
                documentLevel = v
                documentNameLevel[k.parentObject.parentDict].append(documentLevel)
                print('new processing loop output is: ')
                pprint.pprint(documentNameLevel)
        for dictionary in listOfDicts:
            for k,v in dictionary.items():
                print('entered processing loop')
                holderDict={}
                holderDict[k.field]=[]
                holderDict2 = {}
                holderDict2[''.join(str(x) for x in k.getDBEntry())]=v
                print('v is: ')
                print(v)
                print('holder dict 2 is: ')
                pprint.pprint(holderDict2)
                holderDict[k.field].append(holderDict2)
                pprint.pprint(holderDict)
                newlistOfDicts.append(holderDict)
        
        print('post processing listOfDicts is: ')
        pprint.pprint(newlistOfDicts)
        return documentNameLevel

    def aggregateByParent3(self):
        print ('entered aggregateByParent')
        print ('self.viewList is:')
        pprint.pprint(self.viewList)
        print('which translated is: ')
        for view in self.viewList:
            print(str(view.field)+': '+str(view.getDBEntry()))
        
        
        listOfDicts = []
        count = 0
        for labelentry in self.viewList:
            holderDict={}
            if labelentry.designateParent == labelentry.field:
                holderDict[labelentry]={}
                listOfDicts.append(holderDict)
        print('list of Dicts is now: ')
        pprint.pprint(listOfDicts)
        
        for labelentry in self.viewList:
            count=count+1
            print ('entered Loop #'+str(count))
            print ('looking at '+ labelentry.field)
            parent = labelentry.parent
            """
            if not listOfDicts:
                print ('entered empty list loop')
                holderDict = {}
                holderDict['parent'] = parent
                holderDict[labelentry.field]=[labelentry.getDBEntry()]
                listOfDicts.append(holderDict)
                print (listOfDicts)
            """
            holderDict = {}
            for dictionary in listOfDicts:
                print ('entered filled list loop')
                for k,v in dictionary.items():
                    #holderDict = {}
                    if parent == k.getDBEntry():
                        print ('parent match found')
                        pprint.pprint(dictionary[k])
                        """
                        holderDict[labelentry.field]=labelentry.getDBEntry()
                        dictionary[k].append(holderDict)
                        """
                        holderDict={}
                        holderDict[labelentry]=labelentry
                        dictionary[k].update(holderDict)
                        pprint.pprint(listOfDicts)
                """
                else:
                    print ('parent Match not found')
                    holderDict = {}
                    holderDict['parent'] = parent
                    holderDict[labelentry.field]=[labelentry.getDBEntry()]
                    listOfDicts.append(holderDict)
                    print (listOfDicts)
                """
        return listOfDicts
    
    def aggregateByParent2(self):
        print ('entered aggregateByParent')
        print ('self.viewList is:')
        pprint.pprint(self.viewList)
        listOfDicts = []
        count = 0
        for labelentry in self.viewList:
            holderDict = {}
            if labelentry.designateParent == labelentry.field:
                holderDict[labelentry]={}
                listOfDicts.append(holderDict)
        print('list of Dicts is now: ')
        pprint.pprint(listOfDicts)
        
        for labelentry in self.viewList:
            count=count+1
            print ('entered Loop #'+str(count))
            print ('looking at '+ labelentry.field)
            parent = labelentry.parent
            """
            if not listOfDicts:
                print ('entered empty list loop')
                holderDict = {}
                holderDict['parent'] = parent
                holderDict[labelentry.field]=[labelentry.getDBEntry()]
                listOfDicts.append(holderDict)
                print (listOfDicts)
            """
            holderDict = {}
            for dictionary in listOfDicts:
                print ('entered filled list loop')
                for k,v in dictionary.items():
                    #holderDict = {}
                    if parent == k.getDBEntry():
                        print ('parent match found')
                        pprint.pprint(dictionary[k])
                        """
                        holderDict[labelentry.field]=labelentry.getDBEntry()
                        dictionary[k].append(holderDict)
                        """
                        holderDict={}
                        holderDict[labelentry]=labelentry
                        dictionary[k].update(holderDict)
                        pprint.pprint(listOfDicts)
                """
                else:
                    print ('parent Match not found')
                    holderDict = {}
                    holderDict['parent'] = parent
                    holderDict[labelentry.field]=[labelentry.getDBEntry()]
                    listOfDicts.append(holderDict)
                    print (listOfDicts)
                """
        print('The final ListOfDicts is: ')
        pprint.pprint(listOfDicts)
        newlistOfDicts = []
        newlistOfDicts2 = []
        for dictionary in listOfDicts:
            for k,v in dictionary.items():
                print('entered new processing loop')
                documentNameLevel = {}
                documentNameLevel[k.parentObject.parentDict]=[]
                documentLevel = {}
                documentLevel = v
                documentNameLevel[k.parentObject.parentDict].append(documentLevel)
                print('new processing loop output is: ')
                pprint.pprint(documentNameLevel)
        for dictionary in listOfDicts:
            for k,v in dictionary.items():
                print('entered processing loop')
                holderDict={}
                holderDict[k.field]=[]
                holderDict2 = {}
                holderDict2[''.join(str(x) for x in k.getDBEntry())]=v
                print('v is: ')
                print(v)
                print('holder dict 2 is: ')
                pprint.pprint(holderDict2)
                holderDict[k.field].append(holderDict2)
                pprint.pprint(holderDict)
                newlistOfDicts.append(holderDict)
        
        print('post processing listOfDicts is: ')
        pprint.pprint(newlistOfDicts)
        return listOfDicts
    
    def OnSave(self):
        db=self.client.test
        insertDict = {}
        holderDict1 = {}
        holderDict1['$set']={}
        #upsert={}
        #upsert['upsert']=True
        self.setDBLabelEntryParents()
        for labelentry in self.viewList:
            """
            fieldPathDict={}
            fieldPathDict[labelentry.field]={'$exists':True}
            print ('fieldpathDict is: ' + str(fieldPathDict))
            found = db.fieldPathTest1.find_one(fieldPathDict)
            print ('the found dictionary is:')
            pprint.pprint(found)
            if found is not None:
                found[labelentry.field][''.join(str(x) for x in labelentry.getDBEntry())]=labelentry.parent
                update = {}
                update['$set']=found
                print ('the updated dictionary is:')
                pprint.pprint(update)
            else:
                update={}
                update['$set']={}
                update['$set'][labelentry.field]={}
                update['$set'][labelentry.field][''.join(str(x) for x in labelentry.getDBEntry())]={}
                update['$set'][labelentry.field][''.join(str(x) for x in labelentry.getDBEntry())]=labelentry.parent
            db.fieldPathTest1.update_one(fieldPathDict,update,upsert=True)
            foundcheck = db.fieldPathTest1.find_one(fieldPathDict)
            print ('the new found dictionary is:')
            pprint.pprint(foundcheck)

            setDict = {}
            setDict['$set']={}
            print('AAAAAAAAAAAAAAAAAH')
            pprint.pprint('joined is '+''.join(str(x) for x in labelentry.getDBEntry()))
            #pprint.pprint('unjoined is '+(str(x) for x in labelentry.getDBEntry()))
            setDict['$set'][''.join(str(x) for x in labelentry.getDBEntry())]={}
            setDict['$set'][''.join(str(x) for x in labelentry.getDBEntry())]=labelentry.parent
            print ('setDict is: ' + str(setDict))
            pathTestreturnVal = db.pathTest1.update_one({},setDict,upsert=True)
            """
            newPathDict = {}
            setLevel = {}
            setLevel['$set']={}
            if labelentry.parentObject is not None:
                newPathDict['childField']=labelentry.field
                newPathDict['childEntry']=labelentry.getDBEntry()
                newPathDict['parentField']=labelentry.parentField
                newPathDict['parentEntry']=labelentry.parentEntry
                newPathDict['DocumentName']=labelentry.parentObject.parentDict
            setLevel['$set']=newPathDict
            newPathTestreturnVal = db.newPathTest1.update_one(newPathDict,setLevel,upsert=True)
            print ('The return value on the upsert is:'+str(newPathTestreturnVal.raw_result))
            
            """"
            pathDict={}
            pathDict[labelentry.field]={'$exists':True}
            print ('pathDict is: ' + str(pathDict))
            #pathDict[labelentry.field][''.join(str(x) for x in labelentry.getDBEntry())]=labelentry.parent
            """
            """
            db.pathsTest.update_one(pathDict,setDict,upsert=True)
            """
            """
            setDict={}
            setDict[labelentry.field]={}
            setDict[labelentry.field][''.join(str(x) for x in labelentry.getDBEntry())]=labelentry.parent
            pathsTestreturnVal = db.pathsTest1.insert_one(setDict)

            print (labelentry.parent)
            """
            """
            operationsDict=labelentry.buildDBPath(self.client,labelentry.parent)
            opPathDict = labelentry.buildDBPath(self.client,labelentry.parent,False)
            print ('operationsDict is: ' )
            pprint.pprint(operationsDict)
            opfound = db.operationsTest1.find_one(operationsDict)
            print ('the opfound dictionary is:')
            pprint.pprint(opfound)
            if opfound is not None:
                opfound[labelentry.field]={}
                opfound[labelentry.field]=[labelentry.getDBEntry()]
                opupdate = {}
                opupdate['$set']=opfound
                print ('the updated dictionary is:')
                pprint.pprint(opupdate)
            else:
                opupdate={}
                opupdate['$set']={}
                opupdate['$set'][labelentry.field]={}
                opupdate['$set'][labelentry.field]=[labelentry.getDBEntry()]
            operationsReturnValue=db.operationsTest1.update_one(operationsDict,opupdate,upsert=True)
            print ('The return value on the upsert is:'+str(operationsReturnValue.raw_result))
            foundcheck = db.operationsTest1.find_one(operationsDict)
            print ('the new operationsfound dictionary is:')
            pprint.pprint(foundcheck)
            """
        listOfDicts=self.aggregateByParent2()
        print (listOfDicts)
        print('list of dicts is: ')
        pprint.pprint(listOfDicts)
        for thing in listOfDicts:
            print(thing)
        for thing in listOfDicts:
            print(thing)
            operationsDict=DBPath.Query(self.client,thing[0],thing[0].parentObject)
            print ('the operationsDict is: ')
            pprint.pprint(operationsDict)
            opPathDict = labelentry.buildDBPath(self.client,thing['parent'],False)
            print ('the opPathDict is: ')
            pprint.pprint(opPathDict)
            opfound = db.operationsTest1.find_one(operationsDict)
            print ('the opfound dictionary is:')
            pprint.pprint(opfound)
            if opfound is None:
                opupdate={}
                opupdate['$set']=thing
                print ('the updated dictionary is:')
                pprint.pprint(opupdate)
                returnVal = db.operationsTest1.update_one(operationsDict,opupdate,upsert=True)
                print ('The return value on the upsert is:'+str(returnVal.raw_result))
                foundcheck = db.operationsTest1.find_one(operationsDict)
                print ('the new operationsfound dictionary is:')
                pprint.pprint(foundcheck)
            else:
                opupdate={}
                opupdate['$set']=opfound
                print ('the updated dictionary is:')
                pprint.pprint(opupdate)
        return
    
    def OnSave3(self):
        db=self.client.test
        insertDict={}
        holderDict1={}
        holderDict1['$set']={}
        self.setDBLabelEntryParents()
        
        listOfDicts=self.aggregateByParent3()
        #print (listOfDicts)
        print('In main OnSave, list of dicts is: ')
        pprint.pprint(listOfDicts)
        formattedListOfDicts = []
        for dictionary in listOfDicts:
            pprint.pprint(dictionary)
            formattedHolderDict = {}
            for key,value in dictionary.items():
                formattedHolderDict[key]={}
                for k,v in value.items():
                    formattedHolderDict[key][k.field] = v.getDBEntry()
                    #print(k.field+': '+str(v.getDBEntry()))
                formattedListOfDicts.append(formattedHolderDict)
        print('formatted List of Dicts is: ')
        pprint.pprint(formattedListOfDicts)
        
        for ParDictionary in formattedListOfDicts:
            for k,dictionary in ParDictionary.items():
                print(k)
                pprint.pprint(dictionary)
                dictionary['DictParent']=k.getDBEntry()
                dictionary['Parent']=['Initialization']
                dictionary['Children']=['Initialization']
                dictionary['selfID']=k.selfID
                dictionary['parentDict']=k.parentDict
                parent=k
                print(k.field)
                setdictionary={}
                setdictionary['$set']=dictionary
                returnVal = db.operationsTest2.update_one(dictionary,setdictionary,upsert=True)
                print ('The return value on the upsert is:'+str(returnVal.raw_result))
                operationsCheck = db.operationsTest2.find_one(dictionary)
                print(operationsCheck)
                insertID={}
                insertID['_id']=operationsCheck['_id']
                insertID2 = insertID
                
                findcheck=db.operationsTest2.find_one(insertID)
                #pprint.pprint(findcheck)
                holderCheck=insertID
                holderCheck.update(dictionary)
                if findcheck == holderCheck:
                    print('Insert Successful, Found Dict Matches Inserted Dict')
                    pprint.pprint(findcheck)
                    
                parentSearch = {}
                parentSearch[k.field]=k.getDBEntry()
                notExpression = {}
                notExpression['$ne']=k.selfID
                parentSearch['selfID']=notExpression
                
                pprint.pprint(parentSearch)
                
                findParent = db.operationsTest2.find_one(parentSearch)
                
                pprint.pprint(findParent)
                
                if findParent is None:
                    print('No parent Found')
                else:
                    foundParentID = findParent['_id']
                    findParent['Children'].append(insertID['_id'])
                    parentSetUpsert = {}
                    parentSetUpsert['$set']=findParent
                    parentUpsert = db.operationsTest2.update(parentSearch,parentSetUpsert,upsert=True)
                    #print(parentUpsert)
                    print ('The return value on the parentUpsert is:'+str(parentUpsert))
                    
                    findcheck['Parent'].append(foundParentID)
                    selfSetUpsert = {}
                    selfSetUpsert['$set']=findcheck
                    selfUpsert = db.operationsTest2.update(insertID,selfSetUpsert,upsert=True)
                    print ('The return value on the selfUpsert is:'+str(selfUpsert))
                    
                    
                            
                
                
                """
                for key,value in dictionary.items():
                    print('looking at: '+str(key)+' and '+str(value))
                    
                    pathDict={}
                    parentPathDict = {}
                    
                    parentPathDict['selfField']=k.field
                    parentPathDict['selfEntry']=k.getDBEntry()
                    
                    pathDict['parentField']=k.field
                    pathDict['parentEntry']=k.getDBEntry()
                    pathDict['selfField']=key
                    pathDict['selfEntry']=value
                    pathDict['ChildrenIDs']=['Initialization']
                    
                    
                    findcheckPath = db.pathTest2.find_one(pathDict)
                    
                    if not findcheckPath:
                        print('No duplicate path found')
                        db.pathTest2.insert(pathDict)
                    
                    print('parentPathDict is: ')
                    pprint.pprint(parentPathDict)
                    findcheckParent = db.pathTest2.find(parentPathDict)
                    print('FindcheckParent is: ')
                    pprint.pprint(findcheckParent)
                    
                    if not findcheckParent:
                        print ('No parent')
                    else:
                        inserted = db.pathTest2.find_one(pathDict)
                        insertedObjectID = inserted['_id']
                        findcheckParent['ChildrenIDs'].append(insertedObjectID)
                        setdictionary['$set']=findcheckParent
                        ParentPathUpdate = db.pathTest2.update_one(parentPathDict,setdictionary,upsert=True)
                        print ('The return value on the Parent Path upsert is:'+str(ParentPathUpdate.raw_result))
                    """
                        
                
                
            
        return self
    def OnSave2(self):
        db=self.client.test
        insertDict = {}
        holderDict1 = {}
        holderDict1['$set']={}
        #upsert={}
        #upsert['upsert']=True
        self.setDBLabelEntryParents()
        for labelentry in self.viewList:
            """
            fieldPathDict={}
            fieldPathDict[labelentry.field]={'$exists':True}
            print ('fieldpathDict is: ' + str(fieldPathDict))
            found = db.fieldPathTest1.find_one(fieldPathDict)
            print ('the found dictionary is:')
            pprint.pprint(found)
            if found is not None:
                found[labelentry.field][''.join(str(x) for x in labelentry.getDBEntry())]=labelentry.parent
                update = {}
                update['$set']=found
                print ('the updated dictionary is:')
                pprint.pprint(update)
            else:
                update={}
                update['$set']={}
                update['$set'][labelentry.field]={}
                update['$set'][labelentry.field][''.join(str(x) for x in labelentry.getDBEntry())]={}
                update['$set'][labelentry.field][''.join(str(x) for x in labelentry.getDBEntry())]=labelentry.parent
            db.fieldPathTest1.update_one(fieldPathDict,update,upsert=True)
            foundcheck = db.fieldPathTest1.find_one(fieldPathDict)
            print ('the new found dictionary is:')
            pprint.pprint(foundcheck)

            setDict = {}
            setDict['$set']={}
            print('AAAAAAAAAAAAAAAAAH')
            pprint.pprint('joined is '+''.join(str(x) for x in labelentry.getDBEntry()))
            #pprint.pprint('unjoined is '+(str(x) for x in labelentry.getDBEntry()))
            setDict['$set'][''.join(str(x) for x in labelentry.getDBEntry())]={}
            setDict['$set'][''.join(str(x) for x in labelentry.getDBEntry())]=labelentry.parent
            print ('setDict is: ' + str(setDict))
            pathTestreturnVal = db.pathTest1.update_one({},setDict,upsert=True)
            """
            newPathDict = {}
            setLevel = {}
            setLevel['$set']={}
            if labelentry.parentObject is not None:
                newPathDict['childField']=labelentry.field
                newPathDict['childEntry']=labelentry.getDBEntry()
                newPathDict['parentField']=labelentry.parentField
                newPathDict['parentEntry']=labelentry.parentEntry
                newPathDict['DocumentName']=labelentry.parentObject.parentDict
            setLevel['$set']=newPathDict
            newPathTestreturnVal = db.newPathTest1.update_one(newPathDict,setLevel,upsert=True)
            print ('The return value on the upsert is:'+str(newPathTestreturnVal.raw_result))
            
            """"
            pathDict={}
            pathDict[labelentry.field]={'$exists':True}
            print ('pathDict is: ' + str(pathDict))
            #pathDict[labelentry.field][''.join(str(x) for x in labelentry.getDBEntry())]=labelentry.parent
            """
            """
            db.pathsTest.update_one(pathDict,setDict,upsert=True)
            """
            """
            setDict={}
            setDict[labelentry.field]={}
            setDict[labelentry.field][''.join(str(x) for x in labelentry.getDBEntry())]=labelentry.parent
            pathsTestreturnVal = db.pathsTest1.insert_one(setDict)

            print (labelentry.parent)
            """
            """
            operationsDict=labelentry.buildDBPath(self.client,labelentry.parent)
            opPathDict = labelentry.buildDBPath(self.client,labelentry.parent,False)
            print ('operationsDict is: ' )
            pprint.pprint(operationsDict)
            opfound = db.operationsTest1.find_one(operationsDict)
            print ('the opfound dictionary is:')
            pprint.pprint(opfound)
            if opfound is not None:
                opfound[labelentry.field]={}
                opfound[labelentry.field]=[labelentry.getDBEntry()]
                opupdate = {}
                opupdate['$set']=opfound
                print ('the updated dictionary is:')
                pprint.pprint(opupdate)
            else:
                opupdate={}
                opupdate['$set']={}
                opupdate['$set'][labelentry.field]={}
                opupdate['$set'][labelentry.field]=[labelentry.getDBEntry()]
            operationsReturnValue=db.operationsTest1.update_one(operationsDict,opupdate,upsert=True)
            print ('The return value on the upsert is:'+str(operationsReturnValue.raw_result))
            foundcheck = db.operationsTest1.find_one(operationsDict)
            print ('the new operationsfound dictionary is:')
            pprint.pprint(foundcheck)
            """
        listOfDicts=self.aggregateByParent2()
        print (listOfDicts)
        print('list of dicts is: ')
        pprint.pprint(listOfDicts)
        for thing in listOfDicts:
            print(thing)
            
        for thing in listOfDicts:
            print('thing is: ')
            pprint.pprint(thing)
            for key,value in thing.items():
                print('key is :'+str(key.field))
                print('value is: ')
                for k,v in value.items():
                    print('key is: ')
                    print(key.field)
                    print('k is: ')
                    print(k.field)
                    print('v is: ')
                    print(v.field)
                    operationsDict=DBPath.Query(self.client,v,key)
                    print ('the operationsDict is: ')
                    #pprint.pprint(operationsDict.query)
                    #opPathDict = labelentry.buildDBPath(self.client,thing,False)
                    print ('the opPathDict is: ')
                    #pprint.pprint(opPathDict)
                    opfound = db.operationsTest1.find_one(operationsDict.query)
                    print('the query is: ')
                    pprint.pprint(operationsDict.query)
                    print ('the opfound dictionary is:')
                    pprint.pprint(opfound)
                    newThing=self.DictClean(thing)
                    print('cleaned dict is: ')
                    pprint.pprint(newThing)
                    if opfound is None:
                        opupdate={}
                        opupdate['$set']=newThing
                        print ('the updated dictionary is:')
                        pprint.pprint(opupdate)
                        print('the query is: ')
                        pprint.pprint(operationsDict.query)
                        print('the StepList is: ')
                        pprint.pprint(operationsDict.stepList)
                        findVal = db.operationsTest1.find_one(operationsDict.query)
                        print('the findVal call returns: ')
                        pprint.pprint(findVal)
                        #print ('The return value on the find_one is:'+str(findVal.raw_result))
                        returnVal = db.operationsTest1.update_one(operationsDict.query,opupdate,upsert=True)
                        print ('The return value on the upsert is:'+str(returnVal.raw_result))
                        foundcheck = db.operationsTest1.find_one(operationsDict.query)
                        print ('the new operationsfound dictionary is:')
                        pprint.pprint(foundcheck)
                    else:
                        opupdate={}
                        opupdate['$set']=opfound
                        print ('the updated dictionary is:')
                        pprint.pprint(opupdate)
                    break
        return
    def DictClean(self,dictionary):
        cleanedDict={}
        print (type(dictionary))
        for key,value in dictionary.items():
            print(type(key))
            print(type(value))
            cleanedDict[key.parentDict]={}
            for k,v in value.items():
                cleanedDict[key.parentDict][k.field]=v.getDBEntry()
        return cleanedDict
            
    def buildNestedDict(self, searchDict):
        
        def get_root(node):
            for parent in node['Parent']:
                if parent!='Initialization':
                    parentSearchDict={}
                    parentSearchDict['_id']=parent
                    parentParent = db.operationsTest2.find_one(parentSearchDict)
                    node = get_root(parentParent)
            return node
        
        def store_tree(root):
            for child in root['Children']:
                if child!='Initialization':
                    childSearchDict={}
                    childSearchDict['_id']=child
                    childChild = db.operationsTest2.find_one(childSearchDict)
                    childNode = store_tree(childChild)
                    root[childChild['parentDict']]=childNode            
            return root
        
        db=self.client.test
        search=db.operationsTest2.find_one(searchDict)
        #print(search)
        if search is None:
            print('No Search Results')
            nestedDict = {}
        else:
            root =get_root(search)
            nestedDict = store_tree(root)
        return nestedDict
    
    def lambdaMakeDict(self,field,entry):
        dict = {}
        dict[field]=entry
        return dict
        
    def OnPrint(self):
        holderDict = {}
        print (self.viewList)
        for labelentry in self.viewList:
            print(labelentry.tkVarlist)
        for labelentry in self.viewList:
            holderDict[labelentry.field]=labelentry.getDBEntry()
        print (holderDict)
        
        pprint.pprint(self.buildNestedDict(holderDict))
        
        return

    def setDBLabelEntryParents(self):
        for labelentry in self.viewList:
            if labelentry.designateParent == 'None':
                print('No Parent')
            elif labelentry.designateParent == 'All':
                print('Figure out how to configure All Designate Parent option')
            else:
                for labelentry2 in self.viewList:
                    if labelentry.designateParent == labelentry2.field:
                        print(labelentry.field + "'s parent has been set to: "+str(labelentry2.field))
                        labelentry.setParent(labelentry2.getDBEntry(),labelentry2)

    def randomPop(self):
        for labelentry in self.viewList:
            if labelentry.field in ['at1','at2','at3','at4','at5']:
                labelentry.tkVarlist[0].set(numpy.random.randint(10))
            else:
                try:
                    labelentry.tkVarlist[0].set(self.randomPopList.pop())
                except IndexError:
                    print ('Pop List Exhausted')
        return
            


    def populate(self,sheetDict):
        #Put in some fake data
        '''
        for row in range(100):
            tk.Label(self.frame, text="%s" % row, width=3, borderwidth="1",
                     relief="solid").grid(row=row, column=0)
            t="this is the second column for row %s" %row
            tk.Label(self.frame, text=t).grid(row=row, column=1)
        '''
        self.generateSheet(sheetDict)


    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def generateSheet(self, sheetDict):
        orderedList = sheetDict['orderedList']#FLAG
        ordered = coll.OrderedDict()
        self.variables=coll.OrderedDict()
        #dictLength = 20
        """
        for view in self.viewList:
            if view is not None:
                view.grid_forget()
        """
        self.viewList=[]
        for item in orderedList:
            for label, v in sheetDict.items():
                if (label == item):
                    ordered.update({label:v})
        r = 1
        c = 0
        print(ordered)
        print (r,c)
        for k,v in ordered.items():
            """
            print (k,v)
            r, c  = self.entryInterpreter(r,c,k,v)
            print (r,c)
            """
            print (k,v)
            labelEntry = DBLabelEntry.DBLabelEntry(self,k,v)
            labelEntry.grid(row=r,column=c)
            self.viewList.append(labelEntry)
            if labelEntry.newLine:
                r=r+1
                c=0
            else:
                c=c+1
            print (r,c)
    """
    def entryInterpreter(self,r,c,k,v):

        print ('entered entryInterpreter')
        if  len(v)>0:
            if 'SingleValue' in v: #FLAG
                r,c = self.singleLabel(r,c,k,v,False)
            elif 'ListValue' in v:
                r,c = self.singleLabel(r,c,k,v,True) #FLAG
        return r, c


    def listLabel(self, r,c,k,v):
        '''
        self.curListLength = v[2] #IMPORTANT REMEMBER THESE PLACEMENTS

        if self.listProceed:
            c = c+1


        for i in range(0,curListLength):
            if i == 0:
                holderlist = TkVarType(v)
            else:
                holderlist.append(TkVarType(v))
            holdLabel = tk.Label(self.frame, text = k)
            holdLabel.grid(row=r, column=c)
            self.viewList.append(holdLabel)
            SingleEntry(r,c,k,v)
            r = r+1

        self.listProceed = True
        self.listCount = self.listCount+1
        return r,c
        '''


    def singleLabel(self,r,c,k,v,isList):

        ListLength = int(v[2]) #FLAG !!!

        if ListLength>1:
            isList=True
        else:
            isList=False

        if self.listProceed and isList:
           r = r-ListLength+1


        #holderlist = TkVarType(v)
        #self.variables[k] = holderlist #set variables dictionary key label to correspond to a Var list object
        holdLabel = tk.Label(self.frame,text= k)
        holdLabel.grid(row=r, column=c)
        self.viewList.append(holdLabel)
        varList = self.SingleEntry(r,c,k,v,[])

        for count in range(1,int(ListLength)):
            #holderlist.append(TkVarType(v))
            #self.variables[k] = holderlist
            holdLabel = tk.Label(self.frame, text=k)
            holdLabel.grid(row=r, column = c)
            print (r,c)
            self.viewList.append(holdLabel)
            varList = self.SingleEntry(r,c,k,v,varList)
            r=r+1
        '''
        holdEntry = tk.Entry(self, textvariable=holderlist)
        holdEntry.grid(row=r, column=c+1)
        self.viewList.append(holdEntry)
        #self.viewList.append(tk.Entry(self, textvariable=holderlist).grid(row=r, column=c+1))#add Entry field with StringVar object to the grid
        '''
        c=c+2
        if 'r' in v: #FLAG
            r=r+ListLength
            c=0

        if ListLength>1:
            self.listProceed = True
        else:
            self.listProceed = False
        return r,c

    def SingleEntry(self,r,c,k,v,tkVarlist):
        entrywidth = int(v[1])   #Important DB Consideration, will break code if DB isn't done correctly FLAG

        if 'Autocomplete' in v: #REMEMBER DATABASE CONSIDERATION FLAG
            '''
            holdAutoEntry = Autocomplete.AutocompleteEntry(allFields, self, listboxLength=3, width=entrywidth, matchesFunction=matches)
            holdAutoEntry.grid(row=r, column=c+1)
            self.viewList.append(holdAutoEntry)
            '''
            tkVarlist = self.MakeAutoEntry(r,c,k,v,tkVarlist,entrywidth)
        else:
            tkVarlist.append(self.TkVarType(v))
            self.variables[k] = tkVarlist
            holdEntry = tk.Entry(self.frame, textvariable=tkVarlist[-1],width=entrywidth)
            holdEntry.grid(row=r, column=c+1)
            self.viewList.append(holdEntry)

        return tkVarlist

    def MakeAutoEntry(self,r,c,k,v,tkVarlist,entrywidth):

        def matches(fieldValue, acListEntry):
            pattern = re.compile(re.escape(fieldValue) + '.*', re.IGNORECASE)
            return re.match(pattern, acListEntry)
        '''
        allFields=functools.reduce(lambda all_keys, rec_keys: all_keys | set(rec_keys), map(lambda d: d.keys(), db.operations.find()), set())
        client = MongoClient() #start client for MongoDB
        db = client.test #connect to test db
        template = db.operations.find_one({'name':'Attritor Data Sheet'},{'_id': False})
        holdAutoEntry = Autocomplete.AutocompleteEntry(allFields, self, listboxLength=3, width=entrywidth, matchesFunction=matches)
        holdAutoEntry.grid(row=r, column=c+1)
        self.viewList.append(holdAutoEntry)
        '''
        db = self.client.test
        AutoEntryList = functools.reduce(lambda all_keys, rec_keys: all_keys | set(rec_keys), map(lambda d: d.keys(), db.operations.find({k:{'$exists': True}})),set())
        holdAutoEntry = Autocomplete.AutocompleteEntry(AutoEntryList, self.frame, listboxLength=3, width=entrywidth, matchesFunction=matches)
        tkVarlist.append(holdAutoEntry.var)
        holdAutoEntry.grid(row=r, column=c+1)
        self.viewList.append(holdAutoEntry)
        self.variables[k]=tkVarlist

        return tkVarlist

    def AutoEntryList():
        return

    def TkVarType(self, v):
        if 'string' in v:
            return [tk.StringVar()]
        elif 'double' in v:
            return [tk.DoubleVar()]
        elif 'boolean' in v:
            return [tk.BooleanVar()]
        elif 'int' in v:
            return [tk.IntVar()]
        else:
            return [tk.StringVar()]
"""
    def makeTopLevel(newWindowQuery):
        root = tk.Toplevel()
        scroll = tk.ScrolledWindow(root, scrollbar=tk.BOTH)
        scroll.pack(fill=tk.BOTH, expand=1)
        mClient = MongoClient()
        db = mClient.test #connect to test db
        sheetDict = db.templatesTest1.find_one({'finder':newWindowQuery})
        print (sheetDict)
        ScrollableEntryForm(scroll.window,sheetDict).grid(row=0,column=0,sticky='nsew')

if __name__ == "__main__":
    root1=tk.Tk()
    newWindowQuery = tk.StringVar()
    newWindowEntry = tk.Entry(root1, textvariable = newWindowQuery)
    newWindowButton = tk.Button(root1, text = 'Load Entry Sheet', command=lambda: ScrollableEntryForm.makeTopLevel(newWindowQuery.get()))
    newWindowEntry.pack()
    newWindowButton.pack()
    """
    root = Toplevel()
    scroll = tk.ScrolledWindow(root, scrollbar=tk.BOTH)
    scroll.pack(fill=tk.BOTH, expand=1)
    mClient = MongoClient()
    db = mClient.test #connect to test db
    sheetDict = db.templatesTest1.find_one({'finder':newWindowQuery.get()})
    print (sheetDict)
    ScrollableEntryForm(scroll.window,sheetDict).grid(row=0,column=0,sticky='nsew')
    """
    root1.mainloop()
