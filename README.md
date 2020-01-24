# blockchain

**Activate the virtual environment**
```
source blockchain-env/bin/activate
```
**Install all packages**
```
pip3 install -r requirements.txt
```
**Run the tests**
Make sure to activate venv 
```
python3 -m pytest backend/tests
```
**Run the Application and API**
Make sure to activate venv 
```
python3 -m backend.app
```
**Start Mining**
Make sure to activate venv 
```
python3 -m backend.scripts.mining
```
**Run a Peer Instance(Testing Purposes)**
Make sure to activate venv 
```
export PEER=True && python3 -m backend.app
```
