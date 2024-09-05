# Reto Multiagentes

## Features
- CLI
- FastAPI server for Unity client

## Install

### Create a [python virtual environment](https://docs.python.org/3/library/venv.html)

```bash
python -m venv .venv
```

### Start the virtual environment

#### Mac/Linux
```bash
source .venv/bin/activate
```

#### Windows (Powershell)
```powershell
.venv\Scripts\Activate.ps1
```

#### Windows (cmd.exe)
```cmd
.venv\Scripts\Activate.bat
```

### Install requirements
```bash
pip install -r requirements.txt
```

## Run CLI
With the virtual environment started, run the CLI tool

```bash
python main.py
```

## Run lab robot simulation
```bash
python main.py search
```
A graph with the paths will be generated with two output files

