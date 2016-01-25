First run:
This proyect is considered a Django application, so it must be executed like this.

Requeriments:
Python 3
Blender
And installing all the packages declared in requirements.txt
You can run 'pip install -r requirements.txt' to install all in one call

The first run you should run these lines first:
python3 manage.py makemigrations
python3 manage.py migrate

To run the MrRobotto Studio Server you need to run this:
python3 manage.py runserver 0.0.0.0:<port>
For instance 'python3 manage.py runserver 0.0.0.0:8000'

Additional note:
Check if your firewall allows connections from outside if
you get a timeout in the client app.