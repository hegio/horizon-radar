@echo off
chcp 65001 >nul
setlocal
cd /d D:\AI\Horizon

echo ============================================================
echo   Horizon  --  WeChat Listen (interactive bot replies)
echo ============================================================
echo   Keep this window open. In WeChat you can send the bot:
echo     日报 / news  = replay the latest briefing
echo     1 = summary style   2 = overview style
echo     帮助 = help
echo   Close this window (Ctrl+C) to stop listening.
echo ============================================================
echo.

set NO_PROXY=localhost,127.0.0.1,::1
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

uv run horizon-wechat listen
echo.
pause
