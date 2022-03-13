import pathlib
import random
import time
import json
while True:
    try:
        from win10toast import ToastNotifier
        break
    except ImportError as e: #: trying import
        try:
            import os
            os.system('pip install pipreqs && pipreqs --encoding utf-8 --force && pip install -r requirements.txt')
        except:
            print('Import Error:', e)
            exit()
        
class listNotifier():
    notifier = ToastNotifier() # create an object to ToastNotifier class
    notifierDuration = 7 # 7 sec
    newChoiceTime = 60*5 # 5 min
    separator = ':'

    def __init__(self, file_name):
        self.fileName = file_name

    """ 
    def __str__(self): 
        pass
    """

    def fileExtension(self):
        return pathlib.Path(self.fileName).suffix
        
    def readFile(self, extension):
        contents = []
        if extension == '.txt':
            with open(self.fileName, 'r') as f:
                contents = f.readlines()
        elif extension == '.json':
            jsonData = json.load(open(self.fileName))
            for title, description in jsonData.items():
                contents.append(f'{title}{self.separator}{description}')
        elif extension == '.csv':
            pass # Not yet implemented

        return contents

    def randomChoice(self, contents):
        return random.choice(contents)

    def findSeperator(self, content):
        return content.index(self.separator)

    def editContent(self, content, sepIndex):
        title = content[:sepIndex].strip()
        description = content[sepIndex+1:].strip()
        return title, description

    def runNotifier(self, title, description):
        self.notifier.show_toast(title, description, duration=self.notifierDuration)

    def terminalPrinter(self, title, description):
        print(f'{title}: {description}')

    def runner(self):
        extension = self.fileExtension()
        contents = self.readFile(extension)
        while True:
            content = self.randomChoice(contents)
            seperatorIndex = self.findSeperator(content)
            title, description = self.editContent(content, seperatorIndex)
            self.terminalPrinter(title, description)
            self.runNotifier(title, description)
            time.sleep(self.newChoiceTime)

if __name__ == '__main__':
    x = listNotifier('list.json') # Filename
    x.runner()

