@echo off
py -m PyInstaller --onefile --noconsole ^
	--add-data "icon.png;." ^
  main.py