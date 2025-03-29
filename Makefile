packup:
	@pyinstaller --onefile --windowed --add-data "KeilThemer.ui:." --add-data "icon.jpeg:."  --icon=icon.jpeg main.py