from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils import timezone
from operator import attrgetter
from datetime import datetime
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from . import models
from . import forms

def menu_list(request):
    menus = models.Menu.objects.filter(expiration_date__gte=timezone.now())
    
    # menus = []
    # for menu in all_menus:
    #     if menu.expiration_date is not None:
    #         if menu.expiration_date >= timezone.now():
    #             menus.append(menu)
    menus = sorted(menus, key=attrgetter('expiration_date'))

    return render(request, 'menu/list_current_menus.html', {'menus': menus})

def menu_detail(request, pk):
    menu = get_object_or_404(models.Menu, pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})

def item_detail(request, pk):
    item = get_object_or_404(models.Item, pk=pk)
    return render(request, 'menu/item_detail.html', {'item': item})

@login_required
def create_new_menu(request):
    form = forms.MenuForm()
    if request.method == "POST":
        form = forms.MenuForm(request.POST)
        if form.is_valid():
            menu = form.save()
            return redirect(menu.get_absolute_url())

    return render(request, 'menu/new_menu.html', {'form': form})

@login_required
def edit_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    items = Item.objects.all()
    if request.method == "POST":
        menu.season = request.POST.get('season', '')
        menu.expiration_date = datetime.strptime(request.POST.get('expiration_date', ''), '%m/%d/%Y')
        menu.items = request.POST.get('items', '')
        menu.save()

    return render(request, 'menu/change_menu.html', {
        'menu': menu,
        'items': items,
        })