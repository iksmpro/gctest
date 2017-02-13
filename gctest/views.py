from django.http import HttpResponse, Http404
from django.shortcuts import render

from .tree_getter import get_tree

def main_page(request):
    # content = get_tree(request.path)
    # if 'error' in content.keys():
    #     raise Http404("Incorrect path")
    # return render(request, 'main.html', content)
    return render(request, 'example.html', {})

