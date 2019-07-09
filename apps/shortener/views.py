from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views import View

from apps.analytics.models import ClickEvent
from .forms import SubmitUrlForm
from .models import AlmaURL


def home_view_fbv(request):
    if request.method == "POST":
        print(request.POST)
    return render(request, "shortener/home.html", {})


class HomeView(View):
    def get(self, request):
        the_form = SubmitUrlForm()
        bg_image = 'http://hdwpro.com/wp-content/uploads/2017/11/Top-Beach-Background.jpg'
        context = {
            "title": "Alma.co",
            "form": the_form,
            "bg_image": bg_image,
        }
        return render(request, "shortener/home.html", context)

    def post(self, request):
        form = SubmitUrlForm(request.POST)
        context = {
            "title": "Alma.co",
            "form": form
        }
        template = "shortener/home.html"
        if form.is_valid():
            new_url = form.cleaned_data.get("url")
            obj, created = AlmaURL.objects.get_or_create(url=new_url)
            context = {
                "object": obj,
                "created": created,
            }
            if created:
                template = "shortener/success.html"
            else:
                template = "shortener/already-exists.html"

        return render(request, template, context)


class URLRedirectView(View):
    def get(self, request, shortcode=None):
        qs = AlmaURL.objects.filter(shortcode__iexact=shortcode)
        if qs.count() != 1 and not qs.exists():
            raise Http404
        obj = qs.first()
        print(ClickEvent.objects.create_event(obj))
        return HttpResponseRedirect(obj.url)
