**Supported File Formats:**
- [.txt](tests/valid_data.txt)
- [.csv](tests/valid_data.json)

**Basic Usage:**
```bash
python main.py
```
```bash
python main.py data.json
```

**Usage with Arguments:**
```bash
python main.py data.json true false
```
The above usage is equivalent to the following. If arguments are not specified, [default values](modules/config.py) will be used.
```bash
python main.py data.json loop=true history=false
```
You can also use all these commands with pyw, but specifying a list is mandatory for it to work.
```bash
pyw main.py data.json
```
If you used pyw and want to terminate, you can use the following: ```taskkill /t /f /im pythonw.exe```