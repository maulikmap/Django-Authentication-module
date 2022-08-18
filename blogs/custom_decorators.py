from accounts.models import CustomUser, UserPermissions
from django.shortcuts import redirect, HttpResponseRedirect, HttpResponse


def is_logged_in(func):
    """
    This function is used to check if the user is logged in or not.
    """
    def wrapper(request, *args, **kwargs):
        uid = request.session.get('uid')
        if uid is not None:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(redirect_to="/")
    return wrapper


# def is_user_approved(func):
#     """
#     This function is used to check the user status is approved.
#     """
#     def wrapper(request, *args, **kwargs):
#         uid = request.session.get('uid')
#         user = CustomUser.objects.filter(id=uid).first()
#         if uid is not None and not user.is_staff: # check if user is not a staff member.
#             return func(request, *args, **kwargs)
#         elif uid is not None and user.status == 2: # check if user is a staff member and approved.
#             return func(request, *args, **kwargs)
#         else:
#             return HttpResponseRedirect(redirect_to="/user_profile/")
#     return wrapper


def check_permission(perm=None):
    """
    This function is used to check user have permission or not.
    """
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            permissionObj = UserPermissions.objects.filter(permission=perm).first()
            uid = request.session.get('uid')
            if uid is not None:
                user = CustomUser.objects.filter(id=uid).first()
                print(f"custom_permissions:------{user.custom_permissions.all()}")
                permisions = user.custom_permissions.all()
                if permissionObj in permisions:
                    return func(request, *args, **kwargs)
                else:
                    return redirect('error401_view')
            return redirect('error_register')
        return wrapper
    return decorator