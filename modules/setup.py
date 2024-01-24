import os

while True:
    try:
       from win11toast import toast
       break
    except ImportError as ie:
        try: 
           os.system(' && '.join([
           'pip install pipreqs',
           'pipreqs --encoding utf-8 --force',
           'pip install -r requirements.txt'
           ]))
        except Exception as e: 
          print(F'Import Error: {ie}, Exception: {e}')
          exit()

__all__ = ['os', 'toast']