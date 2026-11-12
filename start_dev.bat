@echo off
echo Starting SehatSetu...
echo.
echo [1/2] Starting Flask API on http://localhost:8000
start "SehatSetu API" cmd /k "cd /d "e:\multidisease prdiction" && pip install flask flask-cors && python api.py"

timeout /t 3 >nul

echo [2/2] Starting React frontend on http://localhost:5173
start "SehatSetu UI" cmd /k "cd /d "e:\multidisease prdiction\frontend" && pnpm run dev"

echo.
echo Both servers starting...
echo   API  -> http://localhost:8000
echo   UI   -> http://localhost:5173
echo.
pause
