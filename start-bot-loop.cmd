:scriptstart 
call %cd%\.venv\scripts\activate.bat
echo Run-bot
python runbot.py
echo Stop-bot
goto scriptstart