import os

for f in  os.listdir():
  print(f)
  os.system(f'python ..\main.py {f} loop=false history=false')
  print('-'*42)
