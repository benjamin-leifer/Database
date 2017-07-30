'''
Created on Feb 1, 2017

@author: bleifer
'''
import tkinter as tk
import tkinter.ttk as ttk
import collections as coll
from pymongo import MongoClient
import functools
import re
import matplotlib.pyplot as plt
import Autocomplete
from _csv import field_size_limit


class DBLabelEntry(tk.Frame):
    """
    {
      VarType:'string',
      entrywidth:10,
      ListLength:1,
      newLine:true,
      Autocomplete:false,
      DataType:'Template',
      DBVersion:-1,
      DesignateParent:'P1runID',
      DictType:'Sample',
      parentDict:'Process 1
    }
    """
    GenericDict={}
    GenericDict['VarType']='string'
    GenericDict['entrywidth']=10
    GenericDict['ListLength']=1
    GenericDict['newLine']=True
    GenericDict['Autocomplete']=False
    GenericDict['DataType']='Template'
    GenericDict['DBVersion']=-1
    GenericDict['DesignateParent']='All'
    GenericDict['DictType']='Sample'
    GenericDict['parentDict']='All'
    def __init__(self,root,field,dict,*args,**config):
        tk.Frame.__init__(self,root,**config)
        """
        self.canvas = tk.Canvas(root, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, **config)
        """
        self.root=root
        self.field=field
        self.dict = dict
        self.viewList=[]
        self.tkVarlist=[]
        #print(dict)
        if dict['DataType'] == 'Template':
            self.newLine=dict['newLine']
            self.designateParent=dict['DesignateParent']
            if self.field == self.designateParent:
                self.parentDict = dict['parentDict']
                self.selfID = dict['selfID']
            self.Misc = dict['Misc'] if 'Misc' in dict else None
                
            self.makeDBLabelEntry(field, dict)
            

    def setParent(self,parent, parentObject = None):
        self.parent = parent
        self.parentObject=parentObject
        if parentObject != None:
            self.parentEntry = parentObject.getDBEntry()
            print(self.parentEntry)
            self.parentField = parentObject.field
            print(self.parentField)

    def getDBEntry(self):
        #print (str(self.tkVarlist))
        HoldertkVarlist=[]
        for val in self.tkVarlist:
            #try:
            #print (str(val.get()))
            HoldertkVarlist.append(val.get())
            """
            except (ValueError, AttributeError):
                for val in val:
                    print (str(val.get()))
                    HoldertkVarlist.append(val.get())
            """
        #self.tkVarlist=HoldertkVarlist
        print ("got Values for "+self.field+": "+str(HoldertkVarlist))
        return HoldertkVarlist

    def setDBEntry(self, Entrylist):
        count=0
        for val in self.tkVarlist:
            val.set(Entrylist[count])
            count+=1

    def setDBField(self, field):
        self.field = field
        print(field)
        
    
    def makeDBLabelEntry(self, field, dictionary):

        holdLabel = tk.Label(self,text= field)
        r=0
        holdLabel.grid(row=r, column=0)
        self.viewList.append(holdLabel)
        varList=[]
        varList.append(self.SingleEntry(r,field, dictionary, []))

        for count in range(1,int(dictionary['ListLength'])):
            holdLabel = tk.Label(self, text=field)
            holdLabel.grid(row=r, column = 0)
            #print (r,c)
            self.viewList.append(holdLabel)
            varList.append(self.SingleEntry(r, field, dictionary, varList))
            r=r+1

        #self.tkVarlist=varList
        #print (self.tkVarlist)

    """
    def entryInterpreter(self,r,c,k,v):

        #print ('entered entryInterpreter')
        if  len(v)>0:
            if 'SingleValue' in v: #FLAG
                r,c = self.singleLabel(r,c,k,v,False)
            elif 'ListValue' in v:
                r,c = self.singleLabel(r,c,k,v,True) #FLAG
        return r, c
    """
    def singleLabel(self,r,c,k,v,isList):

        ListLength = int(v[2]) #FLAG !!!

        if ListLength>1:
            isList=True
        else:
            isList=False

        if self.listProceed and isList:
            r = r-ListLength+1


        holdLabel = tk.Label(self.frame,text= k)
        holdLabel.grid(row=r, column=c)
        self.viewList.append(holdLabel)
        varList = self.SingleEntry(r,c,k,v,[])

        for count in range(1,int(ListLength)):
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

    def SingleEntry(self,r,field, dictionary, tkVarlist):
        entrywidth = int(dictionary['entrywidth'])   #Important DB Consideration, will break code if DB isn't done correctly FLAG

        if dictionary['Autocomplete']: #REMEMBER DATABASE CONSIDERATION FLAG
            '''
            holdAutoEntry = Autocomplete.AutocompleteEntry(allFields, self, listboxLength=3, width=entrywidth, matchesFunction=matches)
            holdAutoEntry.grid(row=r, column=c+1)
            self.viewList.append(holdAutoEntry)
            '''
            #tkVarlist = self.MakeAutoEntry(r,field,dictionary,tkVarlist,entrywidth)
            curTkVar = self.TkVarType(dictionary['VarType'])
            tkVarlist.append(curTkVar) #FLAG
            #print (curTkVar)
            holdAutoEntry = ttk.Combobox(self, textvariable=curTkVar,width=entrywidth)
            holdAutoEntry['values']=['a','b','c','d','e']
            holdAutoEntry.grid(row=r, column=1)
            self.viewList.append(holdAutoEntry)
            self.tkVarlist.append(curTkVar)
            
        elif self.Misc:
            FieldTkVar1 = self.TkVarType('string')
            tkVarlist.append(FieldTkVar1) #FLAG
            FieldTkVar1.trace("w", lambda name, index, mode, FieldTkVar1 = FieldTkVar1: self.setDBField(FieldTkVar1.get()))
            curTkVar2 = self.TkVarType(dictionary['VarType'])# Needs work - autodetect data type
            tkVarlist.append(curTkVar2) #FLAG
            fieldEntry = tk.Entry(self, textvariable = FieldTkVar1, width = entrywidth)
            fieldEntry.grid(row=r, column = 1)
            entryEntry = tk.Entry(self, textvariable = curTkVar2, width = entrywidth)
            entryEntry.grid(row = r, column = 2)
            self.viewList.append(entryEntry)
            self.tkVarlist.append(curTkVar2)
        else:
            curTkVar = self.TkVarType(dictionary['VarType'])
            tkVarlist.append(curTkVar) #FLAG
            #print (curTkVar)
            holdEntry = tk.Entry(self, textvariable=curTkVar,width=entrywidth)
            holdEntry.grid(row=r, column=1)
            self.viewList.append(holdEntry)
            self.tkVarlist.append(curTkVar)
        #print (str(tkVarlist))
        return tkVarlist

    def MakeAutoEntry(self,r,field,dict,tkVarlist,entrywidth):

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
        print('Entered MakeAutoEntry')
        print(self.field)
        self.client=MongoClient()
        db = self.client.test
        search = db.operationsTest2.find({self.field:{'$exists': True}})
        for k in search:
            print(k)
            #print(v)
        
        AutoEntryList = functools.reduce(lambda all_keys, rec_keys: all_keys | set(rec_keys), map(lambda d: d.keys(), db.operationsTest2.find({self.field:{'$exists': True}})),set())
        """
        print(AutoEntryList)
        holdAutoEntry = Autocomplete.AutocompleteEntry(AutoEntryList, self, listboxLength=3, width=entrywidth, matchesFunction=matches)
        tkVarlist.append(holdAutoEntry.var)
        holdAutoEntry.grid(row=r, column=1)
        self.viewList.append(holdAutoEntry)
        """
        AutoEntryVar = tk.StringVar()
        holdAutoEntry = ttk.Combobox(self, textvariable = AutoEntryVar)
        holdAutoEntry['values']=['a','b','c','d','e']
        holdAutoEntry.grid(row=r,column=1)
        tkVarlist.append(AutoEntryVar)
        print(tkVarlist)
        tkVarlist[0].set('test')
        self.viewList.append(AutoEntryVar)

        return tkVarlist

    def AutoEntryList(self):#ToDo
        return

    def TkVarType(self, v):
        if 'string' in v:
            return tk.StringVar()
        """
        elif 'double' in v:
            return tk.DoubleVar()
        elif 'boolean' in v:
            return tk.BooleanVar()
        elif 'int' in v:
            return tk.IntVar()
        """
        #else:
        return tk.StringVar()


    def buildDBPath(self, client, parent, existsClause=True , count=0):
        parent = parent[0]
        if count == 0:
            pathDict = {}
            pathDict[parent] = {}
            if existsClause:
                pathDict[parent] = {'$exists':True}

        searchDict = {}
        searchDict[parent]= {}
        searchDict[parent] = {'$exists':True}
        nextPath = client.db.test.pathTest1.find_one(searchDict)

        if nextPath is not None:
            holderPath = {}
            for k,v in nextPath.items():
                v = parent
                holderPath[parent]=pathDict
            pathDict=holderPath
            count = count + 1
            buildDBPath(self, client, parent, count)

        return pathDict
