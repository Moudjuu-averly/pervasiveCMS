from django.shortcuts import redirect, render

def login_redirect(request):
    return redirect('/account/login')


def handler404(request, *args, **kwargs):
    return render(request, 'errors/404/404.html', status=404)


def handler500(request, *args, **kwargs):
    return render(request, 'errors/500/500.html', status=500)
