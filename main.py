import os
import sys
import json
import time
import random
import pathlib
from datetime import datetime

while True:
    try: from win11toast import toast; break
    except ImportError as ie: # if the import fails
        try: os.system('pip install pipreqs && pipreqs --encoding utf-8 --force && pip install -r requirements.txt')
        except Exception as e: print(F'Import Error: {ie}, Exception: {e}'); exit()

class listNotifier():
    notifierDuration = 7 # 7 sec
    newChoiceTime = 60*5 # + notifierDuration
    historyFileName = 'history.txt' #: history file name
    sepChar = ':' #: seperator
    passChar = '#' #: pass char
    lineChar = '-'

    def __init__(self, file_name): self.fileName = file_name #: get file name

    """ 
    def __str__(self): 
        pass
    """

    def getFileExtension(self) -> str:
        return pathlib.Path(self.fileName).suffix #: get file extension

    def readFile(self, extension):
        contents = []
        try:
            match extension:
                case '.json':
                    jsonData = json.load(open(self.fileName, 'r', encoding='utf_8')) # load json file
                    for title, description in jsonData.items(): # iterate json file
                        contents.append(f'{title}{self.sepChar}{description}') # append to contents
                case '.txt', '.csv':
                    with open(self.fileName, 'r', encoding='utf_8') as f:
                        contents = f.readlines()
                case _: print('File extension not supported')

            if len(contents):
                print(F'File read successfully! ({len(contents)} contents)')
                return contents
            else:
                print('File is empty!')
                exit()

        except FileNotFoundError as e: 
            print(f'FileNotFoundError: {e}')
            exit()

    def randomChoice(self, contents):
        return random.choice(contents) #: random choice from list

    def findSeperatorIndex(self, content):
        print('Returned: ', content.index(self.sepChar))
        return content.index(self.sepChar) #: find seperator index

    def editContent(self, content, sepIndex):
        title = content[:sepIndex].strip() #: get title
        description = content[sepIndex+1:].strip() #: get description
        return title, description #: return title and description

    def runNotifier(self, title, description):
        # https://pypi.org/project/win11toast/
        toast(
            title,
            description,
            #selection=['Apple', 'Banana', 'Grape'], button='Submit',
            #on_click='https://www.python.org'
            )
        # self.notifier.show_toast(title, description, duration=self.notifierDuration) # win10toast

    def terminalPrinter(self, title, description):
        print(f'{time.strftime("%X")} | {title}: {description}') #: print on terminal

    def passContent(self, contents): #: remove content with #
        for content in contents: #: iterate contents
            if content[0] == self.passChar: contents.remove(content) # remove content with #
        return contents #: return contents

    def runner(self):
        extension = self.getFileExtension() #: get file extension
        contents = self.readFile(extension) #: read file
        contents = self.passContent(contents) #: remove content with #
        while True: #: infinite loop
            content = self.randomChoice(contents) #: random choice from list
            seperatorIndex = self.findSeperatorIndex(content) #: find seperator index
            title, description = self.editContent(content, seperatorIndex) #: edit content
            self.terminalPrinter(title, description) #: print on terminal
            self.writeHistory(title, description) #: write history
            self.runNotifier(title, description) #: show toast
            time.sleep(self.newChoiceTime) #: wait for new choice   

    def writeHistory(self, title, description):
        mode = 'a' if os.path.exists(self.historyFileName) else 'w' #: check if file exists
        with open(self.historyFileName, mode) as hf: # append mode
            lastContent = self.getLastContent(self.historyFileName, 10) #: get last content date
            if lastContent != None and lastContent != datetime.now().strftime("%d/%m/%Y"):
                newDayMsg = f'{self.lineChar*10} {self.lineChar*8} | {self.lineChar*19}'
                print(newDayMsg[11:])
                hf.write(newDayMsg+'\n') #: write history

            hf.write(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} | {title}: {description}\n') #: write history
            hf.close() # close file

    def getLastContent(self, fileName, end=-1):
        with open(fileName, 'r') as hf:
            try:
                line = hf.readlines()[-1][:end]
                if fileName == self.historyFileName and self.lineChar*end == line: return(None)
            except: return None
        return line

if __name__ == '__main__': #: main function
    try: listFileName = sys.argv[1] # list file name
    except: listFileName = input('Enter list filename: ')
    x = listNotifier(listFileName) #: create object
    x.runner() #: run program