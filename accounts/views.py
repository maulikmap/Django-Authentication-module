from importlib.machinery import FrozenImporter
from django.http import HttpResponse
from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.decorators import method_decorator
from blogs.custom_decorators import check_permission, is_logged_in


# Create your views here.
# class based view
class LoginView(View):
    """
    This is Login view
    """

    def get(self, request, *args, **kwargs):
        form = LoginForm()

        context = {
            "form": form,
        }
        return render(request, 'user/login.html', context=context)

    
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"email:-{email} password:-{password}")

        user = CustomUser.get_user_by_email(email=email)
        print(f"user:-{user}")
        if user is not None:
            flag = check_password(password, user.password)
            if flag:
                if user.is_active:
                    request.session["uid"] = user.id
                    if user.is_superuser and user.is_staff:
                        return redirect("dashboard_view")
                    else:
                        return redirect("user_profile")
                else:
                    messages.error(request, "Your Account is disabled!")
                    return redirect("login_view")
            else:
                messages.error(request, "User credentials are incorrect!")
                return redirect("login_view")
        else:
            messages.error(request, "User credentials are incorrect!")
            return redirect("login_view")


class RegisterView(View):
    """
    This is Register view
    """

    def get(self, request, *args, **kwargs):
        form = RegistrationForm()

        context = {
            "form": form,
        }
        return render(request, 'user/register.html', context=context)
    

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(data=request.POST)

        if form.is_valid():
            createdUser = form.save(commit=False)
            createdUser.password = make_password(createdUser.password)
            if createdUser.is_staff:
                createdUser.status = USER_STATUS[1][0]
            else:
                createdUser.status = USER_STATUS[0][0]
                createdUser.is_active = True
            createdUser.save()
            messages.success(request, "Account created successfully!")
            return redirect("login_view")
        else:
            context = {
                "form": form,
            }
            return render(request, 'user/register.html', context=context)


class DashboardView(View):
    """
    This Dashboard view
    """

    @method_decorator(is_logged_in)
    def get(self, request, *args, **kwargs):
        context = {}
        uid = request.session.get('uid')
        user = CustomUser.objects.filter(id=uid).first()
        users = CustomUser.objects.filter(created_by=uid).order_by('full_name')
        page = request.GET.get('page', 1)
        paginator = Paginator(users, 3)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        context = {
            "user": user,
            "users": users,
        }
        return render(request, 'user/dashboard.html', context=context)


class CreateUserView(View):
    """Create a new user"""

    @method_decorator(check_permission(perm="Create User"))
    def get(self, request, *args, **kwargs):
        uid = request.session.get('uid')
        user = CustomUser.objects.filter(id=uid).first()
        form = CreateUserForm()
        context = {
            "user": user,
            "form": form,
        }
        return render(request, 'user/user_create.html', context=context)
    

    def post(self, request, *args, **kwargs):
        form = CreateUserForm(data=request.POST)
        uid = request.session.get('uid')
        user = CustomUser.objects.filter(id=uid).first()

        if form.is_valid():
            createdUser = form.save(commit=False)
            passwd = createdUser.password # for send in email
            print(f"passwd:-{passwd}")
            createdUser.password = make_password(createdUser.password)
            createdUser.status = USER_STATUS[0][0]
            createdUser.is_active = True
            createdUser.created_by = uid
            createdUser.save()
            messages.success(request, "Account created successfully!")
            return redirect("create_view")
        else:
            context = {
                "user": user,
                "form": form,
            }
            return render(request, 'user/user_create.html', context=context)


class EditUserView(View):
    """Edit a user"""

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except:
            return None

    
    @method_decorator(check_permission(perm="Change User"))
    def get(self, request, pk, *args, **kwargs):
        uid = request.session.get('uid')
        user = CustomUser.objects.filter(id=uid).first()
        instance = self.get_object(pk)
        form = EditUserForm(instance=instance)
        context = {
            "user": user,
            "form": form,
            "instance": instance,
        }
        return render(request, 'user/user_edit.html', context=context)


    def post(self, request, pk, *args, **kwargs):
        uid = request.session.get('uid')
        user = CustomUser.objects.filter(id=uid).first()
        instance = self.get_object(pk)
        form = EditUserForm(data=request.POST, instance=instance)

        if form.is_valid():
            form.save()
            messages.success(request, "Account updated successfully!")
            return redirect("dashboard_view")
        else:
            context = {
                "user": user,
                "form": form,
            }
            return render(request, 'user/user_edit.html', context=context)


class DeleteUserView(View):
    """Delete a user"""

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except:
            return None


    @method_decorator(check_permission(perm="Delete User"))
    def get(self, request, pk, *args, **kwargs):
        instance = self.get_object(pk)
        instance.delete()
        messages.success(request, "Account deleted successfully!")
        return redirect("dashboard_view")


class UserProfileView(View):
    """User profile view"""

    @method_decorator(is_logged_in)
    def get(self, request, *args, **kwargs):
        uid = request.session.get('uid')
        user = CustomUser.objects.filter(id=uid).first()
        userProfile = UserProfile.objects.filter(user=user).first()
        userForm = EditUserForm(instance=user)
        userProfileForm = UserProfileForm(instance=userProfile)
        context = {
            "user": user,
            "userProfile": userProfile,
            "userForm": userForm,
            "userProfileForm": userProfileForm,
        }
        return render(request, 'user/user_profile.html', context=context)

    
    def post(self, request, *args, **kwargs):
        uid = request.session.get('uid')
        user = CustomUser.objects.filter(id=uid).first()
        userProfile = UserProfile.objects.filter(user=user).first()
        userForm = EditUserForm(instance=user, data=request.POST)
        userProfileForm = UserProfileForm(instance=userProfile, data=request.POST, files=request.FILES)

        if userForm.is_valid() and userProfileForm.is_valid():
            userForm.save()
            userProfileForm.save()
            messages.success(request, "Profile Updated successfully!")
            return redirect("user_profile")
        else:
            messages.error(request, "Profile Updated is not successfully!")
            return redirect("user_profile")

#function based views
def logout_view(request):
    request.session.clear()
    return redirect("login_view")


def error401_view(request):
    context = {}
    return render(request, 'errors/error401_view.html', context=context)


def error_register(request):
    context = {}
    return render(request, 'errors/error_register.html', context=context)