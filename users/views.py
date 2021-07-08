# Create your views here.
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views import generic


class Register(generic.CreateView):
    model = User
    template_name = "registration/register.html"
    fields = ['email', 'password', 'last_name', 'first_name']
    success_url = "/"

    def form_valid(self, form):
        obj = form.save(commit=False)
        self.object = User.objects.create_user(
            username=obj.email,
            email=obj.email, password=obj.password,
            last_name=obj.last_name, first_name=obj.first_name
        )

        return HttpResponseRedirect(self.get_success_url())
