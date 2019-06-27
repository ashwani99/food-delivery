import os
import subprocess


os.chdir('food-delivery')
print('Creating virtual environment...')
subprocess.call(['python3', '-m', 'venv', 'venv'])
if os.name == 'nt':
    subprocess.call(['source', 'venv/Scripts/activate'], shell=True)
else:
    subprocess.call(['source', 'venv/bin/activate'], shell=True)
print('Installing dependencies...')
subprocess.call(['pip', 'install', '-r', '../requirements.txt'])
print('Setting up environment variables...')
os.environ['FLASK_APP'] = 'app/api.py'
os.environ['FLASK_DEBUG'] = '1'
os.environ['DATABASE_URL'] = 'sqlite:///food.db'
print('Done!')


# work in progress