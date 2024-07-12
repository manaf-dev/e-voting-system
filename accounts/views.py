from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.


def logout(request):
    if request.method == 'POST':
        selected_candidates = request.session.get("selected_candidates")
        if selected_candidates:
            request.session['selected_candidates'] = {}
        logout(request)
        return redirect('login')
    return redirect('home')