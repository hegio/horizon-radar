@echo off
chcp 65001 >nul
setlocal
cd /d D:\AI\Horizon

echo ============================================================
echo   Horizon  --  SENSITIVE ONLY (push to Telegram)
echo   Sources: China Digital Times + Google News (China politics)
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

if not exist ".env" (
  echo [ERROR] .env missing - HORIZON_WEBHOOK_URL must be set there.
  pause
  exit /b 1
)

echo [info] Telegram delivery uses HORIZON_WEBHOOK_URL from .env
echo.
uv run horizon -c data/config.sensitive.json --hours 24 %*
set RC=%errorlevel%

echo.
echo ============================================================
if "%RC%"=="0" (
  echo   DONE. Pushed to Telegram (if the webhook is configured).
) else (
  echo   Finished with code %RC%. Send the error above to the AI assistant.
)
echo ============================================================
pause
