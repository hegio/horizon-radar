@echo off
chcp 65001 >nul
setlocal
cd /d D:\AI\Horizon

echo ============================================================
echo   Horizon News Radar  --  LOCAL OLLAMA mode
echo   Model: qwen3.6:35b-a3b    Cost: free    Speed: slow
echo ============================================================
echo.

netstat -an | findstr /C:"127.0.0.1:10809" | findstr /C:"LISTENING" >nul 2>&1
if %errorlevel%==0 (
  set HTTPS_PROXY=http://127.0.0.1:10809
  set HTTP_PROXY=http://127.0.0.1:10809
  echo [net] proxy 10809 detected  =^>  using proxy
) else (
  echo [net] no proxy detected  =^>  direct connection
)
set NO_PROXY=localhost,127.0.0.1,::1
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

echo.
echo [tip] default window is 24h. change it:  run-ollama.bat --hours 6
echo.
uv run horizon -c data/config.ollama.json %*
set RC=%errorlevel%

echo.
echo ============================================================
if "%RC%"=="0" (
  echo   DONE. Briefing saved to:  D:\AI\Horizon\data\summaries\
) else (
  echo   Finished with code %RC%. Send the error above to the AI assistant.
)
echo ============================================================
pause
