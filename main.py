import os
import sys
import json
import time
import random
import pathlib
from datetime import datetime

while True: 
    try: 
        from win10toast import ToastNotifier # pip install win10toast
        break # break out of the while loop
    except ImportError as e: # if the import fails
        try: # try to import from the pip package
            import os 
            os.system('pip install pipreqs && pipreqs --encoding utf-8 --force && pip install -r requirements.txt') 
        except: 
            print('Import Error:', e) #: print error
            exit() # exit the program
        
class listNotifier():
    notifier = ToastNotifier() # create an object to ToastNotifier class
    notifierDuration = 7 # 7 sec
    newChoiceTime = 60*5 # + notifierDuration
    historyFileName = 'history.txt' #: history file name
    separator = ':' #: seperator
    passChar = '#' #: pass char

    def __init__(self, file_name):
        self.fileName = file_name #: get file name

    """ 
    def __str__(self): 
        pass
    """

    def fileExtension(self):
        return pathlib.Path(self.fileName).suffix #: get file extension
        
    def readFile(self, extension):
        try:
            contents = []
            if extension == '.json': #: json file
                jsonData = json.load(open(self.fileName, 'r', encoding='utf_8')) # load json file
                for title, description in jsonData.items(): # iterate json file
                    contents.append(f'{title}{self.separator}{description}') # append to contents
            else: # txt, csv or other file types 
            # elif extension in ['.txt','.csv']:   
                with open(self.fileName, 'r', encoding='utf_8') as f: #: txt file
                    contents = f.readlines()
        except FileNotFoundError as e:
            print(e)
            exit()
        finally:
            if contents == []: # if list/file is empty
                print('File is empty!')
                exit() #: exit program
            else:
                return contents

    def randomChoice(self, contents):
        return random.choice(contents) #: random choice from list

    def findSeperator(self, content):
        return content.index(self.separator) #: find seperator index

    def editContent(self, content, sepIndex):
        title = content[:sepIndex].strip() #: get title
        description = content[sepIndex+1:].strip() #: get description
        return title, description #: return title and description

    def runNotifier(self, title, description): 
        self.notifier.show_toast(title, description, duration=self.notifierDuration) #: show toast

    def terminalPrinter(self, title, description):
        print(f'{time.strftime("%X")} | {title}: {description}') #: print on terminal

    def passContent(self, contents): #: remove content with #
        for content in contents: #: iterate contents
            if content[0] == self.passChar: # if first char is #
                contents.remove(content) #: remove content
        return contents #: return contents

    def runner(self):
        extension = self.fileExtension() #: get file extension
        contents = self.readFile(extension) #: read file
        contents = self.passContent(contents) #: remove content with #

        while True: #: infinite loop
            content = self.randomChoice(contents) #: random choice from list
            seperatorIndex = self.findSeperator(content) #: find seperator index
            title, description = self.editContent(content, seperatorIndex) #: edit content
            self.terminalPrinter(title, description) #: print on terminal
            self.writeHistory(title, description) #: write history
            self.runNotifier(title, description) #: show toast

            time.sleep(self.newChoiceTime) #: wait for new choice
    
    def writeHistory(self, title, description): 
        mode = 'a' if os.path.exists(self.historyFileName) else 'w' #: check if file exists
        with open(self.historyFileName, mode) as hf: # append mode
            lastContentDate = self.getLastContent(self.historyFileName, 10) #: get last content date
            if lastContentDate != datetime.now().strftime("%d/%m/%Y"):
                hf.write('\n') #: write history
            hf.write(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} | {title}: {description}\n') #: write history
            hf.close() # close file

    def getLastContent(self, fileName, end=-1):
        with open(fileName, 'r') as hf:
            content = hf.readlines()[-1][:end]
            hf.close()
        return(content)

if __name__ == '__main__': #: main function
    try:
        listFileName = sys.argv[1] # list file name
    except:
        listFileName = input('Enter list filename: ')
    x = listNotifier(listFileName) #: create object
    x.runner() #: run program

