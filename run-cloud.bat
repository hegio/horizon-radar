@echo off
chcp 65001 >nul
setlocal
cd /d D:\AI\Horizon

echo ============================================================
echo   Horizon News Radar  --  CLOUD mode (MaaS)
echo   Model: atria-dawn-preview    Cost: pay-per-use    Speed: fastest
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
echo [recommended] full source set is ~800 items; cloud handles it best.
echo               to shrink:  run-cloud.bat --hours 6
echo.
uv run horizon -c data/config.cloud.json %*
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
