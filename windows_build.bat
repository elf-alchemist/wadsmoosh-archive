set ZIP_EXE="c:\Program Files\7-Zip\7z.exe"
set PINST_EXE="c:\python34\scripts\pyinstaller.exe"
set PROJ_NAME="wadsmoosh"

%PINST_EXE% %PROJ_NAME%.py
pause
xcopy /E data\*.* dist\%PROJ_NAME%\data\
xcopy /E res\*.* dist\%PROJ_NAME%\res\
xcopy /E omg\*.* dist\%PROJ_NAME%\omg\
xcopy /E source_wads\delete_me.txt dist\%PROJ_NAME%\source_wads\
xcopy %PROJ_NAME%.py dist\%PROJ_NAME%\
xcopy %PROJ_NAME%_data.py dist\%PROJ_NAME%\
xcopy %PROJ_NAME%.txt dist\%PROJ_NAME%\
xcopy wadsmoo.sh dist\%PROJ_NAME%\
xcopy license.txt dist\%PROJ_NAME%\
%ZIP_EXE% a -r %PROJ_NAME%_win.zip .\dist\%PROJ_NAME%\*
