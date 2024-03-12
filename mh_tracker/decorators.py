from django.http import HttpResponse
from django.shortcuts import redirect

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            print('role', allowed_roles)
            groups=None
            if request.user.groups.exists():
                groups = request.user.groups.all()
                for group in groups: 
                    if str(group) in allowed_roles:
                        return view_func(request, *args, **kwargs)
            else:
              
                msg="You are not authorized to view this page"
                return HttpResponse(msg)
        return wrapper_func
    return decorator