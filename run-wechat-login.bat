@echo off
chcp 65001 >nul
setlocal
cd /d D:\AI\Horizon

echo ============================================================
echo   Horizon  --  WeChat Bot Login (scan the QR code)
echo ============================================================
echo.
echo   Steps:
echo     1. A QR code appears in this window
echo     2. Open WeChat on your phone - Scan
echo     3. Send the bot any message to activate the session
echo.
echo   The session is saved to data\wechat_session.json and reused
echo   by later runs. Re-run this script if delivery stops working.
echo ============================================================
echo.

netstat -an | findstr /C:"127.0.0.1:10809" | findstr /C:"LISTENING" >nul 2>&1
if %errorlevel%==0 (
  set HTTPS_PROXY=http://127.0.0.1:10809
  set HTTP_PROXY=http://127.0.0.1:10809
)
set NO_PROXY=localhost,127.0.0.1,::1
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

uv run horizon-wechat login
echo.
pause
