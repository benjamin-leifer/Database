#import tkinter as tk
import collections as coll
from pymongo import MongoClient
import functools
import re
import matplotlib.pyplot as plt
import Autocomplete
import DBLabelEntry
import ScrolledWindow
import tkinter.tix as tk
#from ScrollableFrameHelper import *
import pprint

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

        printButton = tk.Button(self,text='Print',command = self.OnPrint)
        printButton.grid(row=0,column=0)
        submitButton = tk.Button(self, text='Submit', command = self.OnSubmit)
        submitButton.grid(row=0,column=1)
        autofillButton = tk.Button(self, text = 'Autofill', command= self.OnAutofill)
        autofillButton.grid(row=0,column=2)
        autofillButton = tk.Button(self, text = 'Save', command= self.OnSave)
        autofillButton.grid(row=0,column=3)
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

        client = MongoClient()
        db = client.test
        found = db.operations.find_one(findDict,{'_id': False}) #pull single dictionary from db
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
            count=count+1
            print ('entered Loop #'+str(count))
            print ('looking at '+ labelentry.field)
            parent = labelentry.parent
            if not listOfDicts:
                print ('entered empty list loop')
                holderDict = {}
                holderDict['parent'] = parent
                holderDict[labelentry.field]=[labelentry.getDBEntry()]
                listOfDicts.append(holderDict)
                print (listOfDicts)
            elif listOfDicts:
                for dict in listOfDicts:
                    print ('entered filled list loop')
                    if parent == dict['parent']:
                        print ('parent match found')
                        dict[labelentry.field]=[labelentry.getDBEntry()]
                        print(listOfDicts)
                    else:
                        print ('parent Match not found')
                        holderDict = {}
                        holderDict['parent'] = parent
                        holderDict[labelentry.field]=[labelentry.getDBEntry()]
                        listOfDicts.append(holderDict)
                        print (listOfDicts)
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
            setDict['$set'][''.join(str(x) for x in labelentry.getDBEntry())]={}
            setDict['$set'][''.join(str(x) for x in labelentry.getDBEntry())]=labelentry.parent
            print ('setDict is: ' + str(setDict))
            db.pathTest1.update_one({},setDict,upsert=True)

            pathDict={}
            pathDict[labelentry.field]={'$exists':True}
            print ('pathDict is: ' + str(pathDict))
            #pathDict[labelentry.field][''.join(str(x) for x in labelentry.getDBEntry())]=labelentry.parent
            """
            db.pathsTest.update_one(pathDict,setDict,upsert=True)
            """
            setDict={}
            setDict[labelentry.field]={}
            setDict[labelentry.field][''.join(str(x) for x in labelentry.getDBEntry())]=labelentry.parent
            db.pathsTest1.insert_one(setDict)

            print (labelentry.parent)
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
        listOfDicts=self.aggregateByParent()
        print (listOfDicts)
        pprint.pprint(listOfDicts)
        for thing in listOfDicts:
            operationsDict=labelentry.buildDBPath(self.client,thing['parent'])
            opPathDict = labelentry.buildDBPath(self.client,thing['parent'],False)
            opfound = db.operationsTest1.find_one(operationsDict)
            print ('the opfound dictionary is:')
            pprint.pprint(opfound)
            if opfound is None:
                opupdate={}
                opupdate['$set']=opfound
                print ('the updated dictionary is:')
                pprint.pprint(opupdate)
            else:
                opupdate={}
                opupdate['$set']=opfound
                print ('the updated dictionary is:')
                pprint.pprint(opupdate)
        return

    def OnPrint(self):
        holderDict = {}
        for labelentry in self.viewList:
            holderDict[labelentry.field]=labelentry.getDBEntry()
        print (holderDict)
        return

    def setDBLabelEntryParents(self):
        for labelentry in self.viewList:
            for labelentry2 in self.viewList:
                if labelentry.designateParent == labelentry2.field:
                    labelentry.setParent(labelentry2.getDBEntry())


    #def buildDBPath():

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
