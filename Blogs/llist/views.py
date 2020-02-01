from django.shortcuts import render

from blog_post.models import Blogpost

def list_details(request):
    obj1 = Blogpost.objects.get(id=2)
    obj2 = Blogpost.objects.get(id=1)
    return render(request, "index.html", {'obj': [obj1, obj2]})
