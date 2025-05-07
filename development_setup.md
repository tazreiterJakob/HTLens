# Windows

## initial setup

1. clone the repo\
`git clone https://github.com/tazreiterJakob/HTLens.git`

2. change directory into the repo\
`cd .\HTLens`

3. start a PS where you can run scripts\
`powershell.exe -noprofile -executionpolicy bypass`

4. create a virtual environment\
`py -3 -m venv .venv`

5. activate the virtual environment\
`.\.venv\Scripts\Activate.ps1`

6. install the requirements\
`pip install -r .\requirements.txt`

7. (optional) install watchdog\
`pip install watchdog`

8. initiate the DB\
`flask --app HTLens init-db`

9. run the server\
`flask --app HTLens run --debug`


## start existing setup

1. open the directory\
`cd .\HTLens`

2. start a PS where you can run scripts\
`powershell.exe -noprofile -executionpolicy bypass`

3. activate the virtual environment\
`.\.venv\Scripts\Activate.ps1`

4. run the server\
`flask --app HTLens run --debug`
