from django.shortcuts import redirect
from MrRobottoStudioServer.utils import is_studio_app

def home(request):
    if is_studio_app(request):
        return redirect('connect')
    else:
        return redirect('studio')