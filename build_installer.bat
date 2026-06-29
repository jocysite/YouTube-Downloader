@echo off
echo ============================================
echo  Afriway Downloader — Build Installer
echo ============================================
echo.

where pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo Trying python -m PyInstaller...
    python -m PyInstaller --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ERROR: PyInstaller not found. Run: pip install pyinstaller
        pause & exit /b 1
    )
    set PYINST=python -m PyInstaller
) else (
    set PYINST=pyinstaller
)

echo [1/2] Building one-dir bundle...
%PYINST% afriway_installer.spec --clean --noconfirm
if %errorlevel% neq 0 (
    echo BUILD FAILED (PyInstaller step).
    pause & exit /b 1
)

echo.
echo [2/2] Compiling NSIS installer...
set NSIS1=C:\Program Files (x86)\NSIS\makensis.exe
set NSIS2=C:\Program Files\NSIS\makensis.exe
if exist "%NSIS1%" (
    "%NSIS1%" installer.nsi
) else if exist "%NSIS2%" (
    "%NSIS2%" installer.nsi
) else (
    echo WARNING: NSIS not found. Skipping installer step.
    echo Install NSIS from https://nsis.sourceforge.io or run:
    echo   winget install NSIS.NSIS
    echo Then re-run this script (PyInstaller step will be fast - cached).
    echo The one-dir build is ready at: dist\AfriWayDownloader_dir\
    pause & exit /b 0
)

if %errorlevel% neq 0 (
    echo NSIS compilation failed.
    pause & exit /b 1
)

echo.
echo ============================================
echo  Done!
echo  Installer: dist\AfriWayDownloader-Setup-1.0.exe
echo ============================================
pause
