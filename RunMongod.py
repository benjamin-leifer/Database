import subprocess
import _thread as thread, time
import threading

global dbGUI
global mongod
def runGUI():
    #global dbGUI
    dbGUI = subprocess.Popen(r'python Database Working Copy Take 3-9-TemplatesAdded.py',
                        shell = True,
                        cwd =r'C:\Users\bleifer\Documents\MongoDB',
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)

def runMongod():
    #global mongod
    mongod = subprocess.Popen(r'mongod --dbpath="C:\Egnyte\Shared\Shared\MongoDB\data"',
                                shell=True,
                                cwd=r'C:\Program Files\MongoDB\Server\3.2\bin',
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE
                                )
    #Min, Mout = mongod.communicate()
    #print(Mout)
    #mongodOut, mongodErr = mongod.communicate()
    #print(mongodOut)
    #print('did it run Successfully?')

#test=subprocess.Popen(r'mongod --dbpath="C:\Egnyte\Shared\Shared\MongoDB\data"',shell=True,cwd=r'C:\Program Files\MongoDB\Server\3.2\bin')
class mongodThreading(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        #global mongod
        mongod = subprocess.Popen(
                                r'mongod --dbpath="C:\Egnyte\Shared\Shared\MongoDB\data"',
                                shell=True,
                                cwd=r'C:\Program Files\MongoDB\Server\3.2\bin',
                                stdin=subprocess.PIPE,
                                stdout=subprocess.STDOUT
                                #stderr=subprocess.PIPE
                                )
                                
class GUIthreading(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        #global dbGUI
        dbGUI = subprocess.Popen(r'python Database Working Copy Take 3-9-TemplatesAdded.py',
                        shell = True,
                        cwd =r'C:\Users\bleifer\Documents\MongoDB',
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)
#mongodThread = thread.start_new_thread(runMongod,())
mongodThread = mongodThreading().start()
#mongodThread = threading.Thread(target = (lambda: runMongod()))
#time.sleep(5)
print (mongodThread.isAlive())
#print(mongod.stdout.read())
#for line in mongod.stdout: print(line,end = '')
"""
if mongodThread.exitcode==None:
    print('mongod started')
    GUIthread = GUIthreading().start()

#GUIthread = thread.start_new_thread(runGUI, ())
"""

