import hashlib

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django.utils.crypto import get_random_string
from app_shurl.forms import UserForm, UrlForm

from app_shurl.models import UrlIndex, Url
from django_shurl.settings import LINK_STRING_LENGTH, SECRET_KEY

# Create your views here.

# url -> random string -> encrypt using secret -> Store in index (index: url model id) -> URL model
# string -> decrypt -> query index for id -> URL model -> return URL -> redirect


def success(request):
    context = None
    return render(request, 'shurl/result.html', context)


def index(request):
    form = UrlForm()
    context = {"form_url": form}
    return render(request, 'shurl/index.html', context)


def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration complete")
            return redirecting("index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = UserForm()
    return render(request=request, template_name="shurl/register.html", context={"register_form": form})


class MainURL(FormView):  # https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic-editing/#formview

    template_name = "shurl/url.html"
    form_class = UrlForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data['url']
            stringas = get_random_string(length=LINK_STRING_LENGTH)
            cipher = self.encryption(stringas)
            if UrlIndex.objects.filter(url=cipher).exists():  # for collision detection
                stringas = get_random_string(length=LINK_STRING_LENGTH)
                cipher = self.encryption(stringas)
            url_instance = Url(url=data, user=request.user)
            url_instance.save()
            index_inst = UrlIndex(url=cipher, url_data=url_instance)
            index_inst.save()

            full_url = request.build_absolute_uri('/') + stringas
            return render(request, 'shurl/result.html', context={"new_url": full_url})

        return render(request, self.template_name, {'form': form})

    @classmethod
    def encryption(cls, stringas):
        full_string = stringas + SECRET_KEY[-32:]
        cipher = hashlib.md5(full_string.encode('utf-8')).hexdigest()
        return cipher


def redirecting(request, shorturl):
    try:
        if len(shorturl) == LINK_STRING_LENGTH:
            stringas = MainURL.encryption(shorturl)

            index_instance = UrlIndex.objects.get(url=stringas)
            main_url = Url.objects.get(id=index_instance.url_data.id, active=True)

            main_url.clicks += 1
            if main_url.clicks + 1 > main_url.max_clicks > 0:
                main_url.active = False
            main_url.save()
            return HttpResponseRedirect(main_url.url)
        else:
            raise Http404('Sorry this link does not exist :(')
    except (UrlIndex.DoesNotExist, Url.DoesNotExist):
        raise Http404('Sorry this link does not exist :(')
