linux:
	@pyinstaller --onefile --windowed --add-data "KeilThemer.ui:." --add-data "icon.jpeg:." main.py

win:
	@pyinstaller --onefile --windowed --add-data "KeilThemer.ui:." --add-data "icon.jpeg:." main.py