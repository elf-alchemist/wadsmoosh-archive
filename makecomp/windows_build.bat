set ZIP_EXE="c:\Program Files\7-Zip\7z.exe"
set PINST_EXE="c:\python27\scripts\pyinstaller.exe"
set PROJ_NAME="makecomp"

%PINST_EXE% makecomp.py
pause
xcopy /E data\*.* dist\%PROJ_NAME%\data\
xcopy /E res\*.* dist\%PROJ_NAME%\res\
xcopy /E source_wads\delete_me.txt dist\%PROJ_NAME%\source_wads\
%ZIP_EXE% a -r %PROJ_NAME%_win.zip ./dist/%PROJ_NAME%/*
