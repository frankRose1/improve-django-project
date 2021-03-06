from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils import timezone
from operator import attrgetter
from datetime import datetime
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from . import models
from . import forms

def menu_list(request):
    menu_list = models.Menu.objects.prefetch_related('items').filter(expiration_date__gte=timezone.now())
    paginator = Paginator(menu_list, 5)
    page = request.GET.get('page', 1)
    menus = paginator.get_page(page)
    return render(request, 'menu/list_current_menus.html', {'menus': menus})

def menu_detail(request, pk):
    menu = get_object_or_404(models.Menu, pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})

def item_detail(request, pk):
    try:
        item = models.Item.objects.select_related('chef').get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    else:
        return render(request, 'menu/item_detail.html', {'item': item})

def new_menu(request):
    form = forms.MenuForm()
    if request.method == "POST":
        form = forms.MenuForm(request.POST)
        if form.is_valid():
            menu = form.save()
            return redirect(menu.get_absolute_url())

    return render(request, 'menu/menu_form.html', {'form': form})

def edit_menu(request, pk):
    try:
        menu = models.Menu.objects.prefetch_related('items').get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    else:
        form = forms.MenuForm(instance=menu)
        if request.method == "POST":
            form = forms.MenuForm(request.POST, instance=menu)
            if form.is_valid():
                form.save()
                return redirect(menu.get_absolute_url())

    return render(request, 'menu/menu_form.html', { 'form': form })


def item_list(request):
    items_list = models.Item.objects.all()
    paginator = Paginator(items_list, 12)
    page = request.GET.get('page', 1)
    items = paginator.get_page(page)
    return render(request, 'menu/item_list.html', {'items': items})