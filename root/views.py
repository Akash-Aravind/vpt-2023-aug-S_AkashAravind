from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import TemplateView, DetailView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import WishList
from django.contrib.auth.forms import UserCreationForm
import requests


def registerPage(request):
    form=UserCreationForm()
    context={"form":form}
    return render(request, "register.html",context)



class HomePage(TemplateView):
    def get(self, request):
        data = requests.get("https://api.nytimes.com/svc/books/v3/lists/overview.json?api-key=4eqGqpcgPr09d47XDHGaU7UU2sX7ZFxo")
        beta = data.json()
        template_name = "index.html"
        return render(request, 'index.html', {
            'ip': beta["results"]["lists"],
        })
def Wishlist(request,title,isbn):
    try:
        Wishlist.objects.get(
            name=request.user, product=isbn)
        return render(request, 'beginner.html', {
            'success': f'Hey {request.user} {title} has already been added',
        })
    except:
        fetchurl = f"https://www.googleapis.com/books/v1/volumes?q={title}&key=AIzaSyAJ8nHtE3NlGpfnhN1jTT_0FvC49dyf1bo"
        data = requests.get(fetchurl)
        binfo = data.json()
        imgvar = binfo['items'][0]['volumeInfo']['imageLinks']['thumbnail']
        context=WishList.objects.create(name=request.user,product=isbn,imageurl=imgvar,title=title)
        return redirect('http://localhost:8000/wishlistview')

class WishListView(TemplateView):
    template_name = "wishview.html"
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["dat"] = WishList.objects.all().filter(
            name=self.request.user.username)
        return context


def removewishlist(request,isbnum):
    rem = WishList.objects.get(product=isbnum, name=request.user.username)
    rem.delete()
    return redirect('http://localhost:8000/wishlistview')

def SearchPage(request):
    try:
        searchtext=request.POST.get("searchtext")
        fetchurl = f"https://www.googleapis.com/books/v1/volumes?q={searchtext}&maxResults=40&key=AIzaSyAJ8nHtE3NlGpfnhN1jTT_0FvC49dyf1bo"
        data = requests.get(fetchurl)
        res = data.json()

        return render(request, 'search.html',{
            'queryresults': res["items"],
        })
    except:
        return render(request, 'error.html',{
            'error':"the query was not applicable try another one" ,
        })


class DetailPage(TemplateView):
    template_name = "detail.html"
    def get(self,request,title):
        fetchurl = f"https://www.googleapis.com/books/v1/volumes?q={title}&key=AIzaSyAJ8nHtE3NlGpfnhN1jTT_0FvC49dyf1bo"
        data = requests.get(fetchurl)
        binfo = data.json()
        return render(request, 'detail.html', {
            'bookinfo':binfo["items"][0],
        })

