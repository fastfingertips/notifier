from . import os

while True:
    try:
        from win11toast import toast
        break
    except ImportError as ie:
        try: 
            # Installing pipreqs to generate requirements.txt
            # and then installing required libraries
            os.system(' && '.join([
                'pip install pipreqs',
                'pipreqs --encoding utf-8 --force',
                'pip install -r requirements.txt'
            ]))
        except Exception as e: 
            print(f'Import Error: {ie}, Exception: {e}')
            exit()

# Defining the list of modules to be exported
__all__ = ['toast']
