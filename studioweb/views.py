from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from MrRobottoStudioServer import settings
from studioservices import views as services_views


# Create your views here.

def root(request):
    if request.path == "/":
        return redirect("/studio")

def register_user(request):
    response = services_views.RegisterViewSet.as_view({'post':'create'})(request)
    if response.status_code == 201:
        try:
            next = request.GET['next']
            return request(next)
        except:
            return redirect('/studio/')
    else:
        return redirect(settings.LOGIN_URL)

def login_user(request):
    response = services_views.LoginViewSet.as_view({'post':'create'})(request)
    if response.status_code == 200:
        try:
            next = request.GET['next']
            return request(next)
        except:
            return redirect('/studio/')
    else:
        return redirect(settings.LOGIN_URL)

def studio_login_page(request):
    if request.user.is_authenticated():
        return redirect("/studio/")
    if request.method == 'POST':
        if 'register' in request.POST:
            return register_user(request)
        if 'login' in request.POST:
            return login_user(request)
        else:
            return render(request, "pages/studio-login.html")
    else:
        return render(request, "pages/studio-login.html")

@login_required()
def studio_logout_user(request):
    logout(request)
    return redirect(settings.LOGIN_URL)

@login_required()
def studio_home(request):
    return render(request, "pages/studiopage-dashboard.html", context={'page': 'dashboard', 'page_title': 'Dashboard'})

@login_required()
def studio_devices(request):
    devices = services_views.AndroidDeviceViewSet.as_view({'get':'list'})(request)
    return render(request, "pages/studiopage-devices.html",
                  context={'page': 'devices', 'page_title': 'Devices', 'devices': devices.data})

@login_required()
def studio_blender_files(request):
    if request.method == 'GET':
        response = services_views.MrrFilesViewSet.as_view({'get': 'list'})(request)
        blends = response.data
        return render(request, "pages/studiopage-blendfiles.html",
                      context={'page': 'blendfiles', 'page_title': 'Blender Files', 'blends': blends})
    elif request.method == 'POST':
        response = services_views.MrrFilesViewSet.as_view({'post': 'create'})(request)
        return redirect("/studio/blender-files")