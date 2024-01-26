from modules.helpers import (
  Terminal,
  History,
  Content,
  Input,
  Item
)

from modules import (
    # .config
    Config,
    # built-in
    random,
    time,
    # setup
    toast,
)

class Notifier():

    def __init__(self, user_input): 
        self.user_input = user_input
        self.items = Content(user_input).items

    def __str__(self):
        return f"Input: {self.user_input} | Items: {len(self.items)}"

    def show(self, title, description):
        # https://pypi.org/project/win11toast/
        toast(
            title,
            description,
            selection=['I Know'],
            button='Submit',
            #on_click='https://www.python.org'
            )

    def run(self, loop:bool=Config.loop, history:bool=Config.history):
        item = Item(random.choice(self.items))
        title, description = item.parse(Config.sep_char)
        Terminal.print(title, description)
        if history:
            History.add(title, description)
        self.show(title, description)
        time.sleep(Config.new_choice_time)   
        if loop:
            while loop:
                self.run(loop)
        else:
            print('Finished')

def main():
    file = Input()
    notifier = Notifier(file)
    notifier.run(file.loop, file.history)

if __name__ == '__main__':
    main()