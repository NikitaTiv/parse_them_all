from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy


class LoginUser(LoginView):
    next_page = reverse_lazy('image_handlers:create_image')
    redirect_authenticated_user = True


def logout_user(request):
    logout(request)
    return redirect('login')
