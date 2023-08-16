@echo off

REM Get the current directory where the batch script is located
set "script_path=%~dp0"

REM Check if "sshman" file exists in the current directory
if exist "%script_path%sshman.exe" (
    REM Add the current directory to the PATH variable
    setx PATH "%PATH%;%script_path%"
    echo sshman has been added to the PATH.
) else (
    echo Error: The file "sshman" does not exist in the same folder as this script.
)

pause
