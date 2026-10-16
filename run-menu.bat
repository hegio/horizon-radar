@echo off
chcp 65001 >nul
setlocal
cd /d D:\AI\Horizon

echo ============================================================
echo            Horizon News Radar  --  MENU
echo ============================================================
echo.
echo   [1] Local Ollama   (free / slow, qwen3.6:35b-a3b)
echo   [2] Local Strata   (free / fast, start 8080 first)
echo   [3] Cloud MaaS     (fastest / pay-per-use, recommended)
echo   [4] Open briefing folder
echo   [0] Exit
echo.
choice /c 12340 /n /m "Select: "

if errorlevel 5 goto quit
if errorlevel 4 goto openfolder
if errorlevel 3 call run-cloud.bat & goto end
if errorlevel 2 call run-strata.bat & goto end
if errorlevel 1 call run-ollama.bat & goto end

:openfolder
start "" "D:\AI\Horizon\data\summaries"
goto end

:quit
exit /b 0

:end
echo.
pause
