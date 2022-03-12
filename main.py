import random
import time
from win10toast import ToastNotifier


class listNotifier():
    notifier = ToastNotifier() # create an object to ToastNotifier class
    notifierDuration = 7 # 7 sec
    newChoiceTime = 60*5 # 5 min

    def __init__(self, file_name, sep):
        self.separator = sep
        self.fileName = file_name

    """ 
    def __str__(self): 
        pass
    """

    def readFile(self):
        with open(self.fileName, encoding='utf8') as f:
            return f.readlines()

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
        while True:
            contents = self.readFile() # Reading file
            content = self.randomChoice(contents)
            seperatorIndex = self.findSeperator(content)
            title, description = self.editContent(content, seperatorIndex)
            self.terminalPrinter(title, description)
            self.runNotifier(title, description)
            time.sleep(self.newChoiceTime)

if __name__ == '__main__':
    x = listNotifier('list.txt', ':') # Filename, 'seperator'
    x.runner()

