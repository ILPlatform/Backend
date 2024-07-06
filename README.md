In order to run the code, you need to run the following;

```
cd functions
source venv/bin/activate
pip3 install -r requirements.txt
```

Then the backend may be emulated through;

```
firebase emulators:start --only functions
```

# Functions

In order to install a module in the backend, add it to `functions/requirements/txt` and run the following;

```
cd functions
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

```

```
