from django.shortcuts import render
from django.http import HttpResponse
from .models import Post, Tag, Category
from config.models import SideBar
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.db.models import Q


# Create your views here.
class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context




