@echo off
echo ">>>>>>>>>>>>>>>>>>>> 	Running mypy"
mypy . 
if %ERRORLEVEL% EQU 0 goto py36
echo ">>>>>>>>>>>>>>>>>>>> 	FAIL mypy"
goto error

:py36
echo ">>>>>>>>>>>>>>>>>>>> 	Running tests on python 3.6"
py -3.6 -m pytest
if %ERRORLEVEL% EQU 0 goto py27
echo ">>>>>>>>>>>>>>>>>>>> 	FAIL Python 3.6"
goto error

:py27
echo ">>>>>>>>>>>>>>>>>>>> 	Running tests on python 2.7"
py -2.7 -m pytest
if %ERRORLEVEL% EQU 0 goto success
echo ">>>>>>>>>>>>>>>>>>>> 	FAIL Python 2.7"
goto error

:success
echo ">>>>>>>>>>>>>>>>>>>> 	SUCCESS"
goto end

:error
echo ">>>>>>>>>>>>>>>>>>>> 	FAIL"

:end
