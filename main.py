import pathlib
import random
import time
import json
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
    newChoiceTime = 60*5 # 5 min
    separator = ':' 
    passChar = '#'

    def __init__(self, file_name):
        self.fileName = file_name #: get file name

    """ 
    def __str__(self): 
        pass
    """

    def fileExtension(self):
        return pathlib.Path(self.fileName).suffix #: get file extension
        
    def readFile(self, extension):
        contents = []
        if extension == '.json': #: json file
            jsonData = json.load(open(self.fileName, 'r', encoding='utf_8')) # load json file
            for title, description in jsonData.items(): # iterate json file
                contents.append(f'{title}{self.separator}{description}') # append to contents
        else: # txt, csv or other file types
        # elif extension in ['.txt','.csv']:   
            with open(self.fileName, 'r', encoding='utf_8') as f: #: txt file
                contents = f.readlines()

        if contents == []: # if list/file is empty
            print('File is empty!')
            exit() #: exit program
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
            title, description = self.editContent(content, seperatorIndex)
            self.terminalPrinter(title, description) #: print on terminal
            self.runNotifier(title, description) #: show toast
            time.sleep(self.newChoiceTime) #: wait for new choice

if __name__ == '__main__': #: main function
    x = listNotifier('list.json') #: create object
    x.runner() #: run program

