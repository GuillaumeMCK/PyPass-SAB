VENV = venv
FOLDER = Scripts
PYTHON = ./$(VENV)/$(FOLDER)/python.exe
PIP = ./$(VENV)/$(FOLDER)/pip3.exe
ACTIVATE = ./$(VENV)/$(FOLDER)/Activate.ps1

.PHONY: run activate freeze install clean

run: install
	$(PYTHON) main.py

build: install
	$(PYTHON) setup.py

activate: $(ACTIVATE)

$(ACTIVATE):
	python3 -m venv $(VENV)

install: activate requirements.txt
	$(PIP) install -r requirements.txt 

freeze: activate
	$(PIP) freeze > requirements.txt

clean:
	-rmdir /s /q build dist __pycache__ $(VENV)

pre-push: clean freeze