@echo off
echo ============================================
echo  Building Afriway Downloader desktop app
echo ============================================
echo.

where pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pyinstaller not found. Run: pip install pyinstaller pywebview
    pause
    exit /b 1
)

echo Cleaning previous build...
if exist build rmdir /s /q build
if exist dist  rmdir /s /q dist

echo.
echo Running PyInstaller...
pyinstaller afriway.spec --clean --noconfirm

if %errorlevel% neq 0 (
    echo.
    echo BUILD FAILED. See output above.
    pause
    exit /b 1
)

echo.
echo ============================================
echo  Build complete!
echo  Executable: dist\AfriWayDownloader.exe
echo ============================================
echo.
echo You can copy dist\AfriWayDownloader.exe anywhere.
echo Drop aria2c.exe next to it to enable torrent downloads.
echo.
pause
