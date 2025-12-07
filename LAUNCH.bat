@echo off
setlocal enabledelayedexpansion
title BillGenerator Unified - All Features
color 0A

echo.
echo ========================================
echo   BillGenerator Unified
echo   Configuration-Based System
echo   With Batch Processing!
echo ========================================
echo.

:menu
echo Select variant to launch:
echo 1. V01 (Standard)
echo 2. V02 (Light)
echo 3. V03 (Basic)
echo 4. V04 (Advanced + Batch Processing)
echo 5. SmartBillFlow (All Features)
echo 6. Batch Run (Command Line - HTML & PDF)
echo 7. Insert Title Data into Image
echo 8. Customize Title from Input Files
echo 9. Process All Titles from Input Files
echo 10. Insert Title from Input Files
echo 11. Exit
echo.
set /p choice="Enter your choice (1-11): "

if "%choice%"=="1" goto launch_v01
if "%choice%"=="2" goto launch_v02
if "%choice%"=="3" goto launch_v03
if "%choice%"=="4" goto launch_v04
if "%choice%"=="5" goto launch_smart
if "%choice%"=="6" goto launch_batch
if "%choice%"=="7" goto insert_title
if "%choice%"=="8" goto customize_title
if "%choice%"=="9" goto process_all_titles
if "%choice%"=="10" goto insert_title_from_input
if "%choice%"=="11" goto exit_script
echo Invalid choice. Please try again.
goto menu

:launch_v01
echo.
echo Launching V01 (Standard)...
python launchers/launch_v01.py
goto menu

:launch_v02
echo.
echo Launching V02 (Light)...
python launchers/launch_v02.py
goto menu

:launch_v03
echo.
echo Launching V03 (Basic)...
python launchers/launch_v03.py
goto menu

:launch_v04
echo.
echo Launching V04 (Advanced + Batch Processing)...
python launchers/launch_v04.py
goto menu

:launch_smart
echo.
echo Launching SmartBillFlow (All Features)...
python launchers/launch_smartbillflow.py
goto menu

:launch_batch
echo.
echo Launching Batch Run (Command Line)...
echo.
python batch_run_demo.py
echo.
pause
goto menu

:insert_title
echo.
echo Inserting Title Data into Image...
echo.
call INSERT_TITLE.bat
goto menu

:customize_title
echo.
echo Customizing Title from Input Files...
echo.
call CUSTOMIZE_TITLE.bat
goto menu

:process_all_titles
echo.
echo Processing All Titles from Input Files...
echo.
call PROCESS_ALL_TITLES.bat
goto menu

:insert_title_from_input
echo.
echo Inserting Title from Input Files...
echo.
call INSERT_TITLE_FROM_INPUT.bat
goto menu

:exit_script
echo.
echo Thank you for using BillGenerator Unified!
echo.
exit /b 0
