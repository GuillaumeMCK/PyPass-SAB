PYTHON = .\venv\Scripts\python.exe
PIP = .\venv\Scripts\pip.exe
ACTIVATE = .\venv\Scripts\activate.bat

run: install
	$(PYTHON) main.py

build: install
	$(PYTHON) setup.py

activate: $(ACTIVATE)

$(ACTIVATE):
	python3 -m venv venv

install: activate requirements.txt
	$(PIP) install -r requirements.txt

freeze: activate
	$(PIP) freeze > requirements.txt

build: install
	$(PYTHON) build.py

clean:
	@if exist build rmdir /s /q build
	@if exist dist rmdir /s /q dist
	@if exist venv rmdir /s /q venv
	@for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"

pre-push: clean freeze
