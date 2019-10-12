from django.shortcuts import render
#from django.http import HttpResponse
from django.shortcuts import HttpResponse
from .models import Post, Tag, Category
from config.models import SideBar
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.contrib import auth
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from comment.forms import CommentForm
from comment.models import Comment



# Create your views here.

class CommonViewMinxin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context

class IndexView(CommonViewMinxin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 20
    context_object_name = 'post_list'
    template_name = 'blog/list.html'

class IndexViewSimple(ListView):
    '''
    控制返回的数据库记录
    '''
    def get_queryset(self):
        print('---这是queryset----')
        print(type(Post.objects.filter(pk=1)))
        return Post.latest_posts()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'ban': 'the web framework',
        })
        print('---这是context----')
        print(context)

        return context

class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context


    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)

class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)

class PostDetailView(CommonViewMinxin, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'comment_form': CommentForm,
            'comment_list': Comment.get_by_target(self.request.path),
        })
        return context

class SearchView(IndexView):

    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        return context


    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))

class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)

class LoginViewSet(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = auth.authenticate(username=username, password=password)
        if not user:
            return JsonResponse(
                {"code": 0,
                 "msg": "用户名或密码错误！",}
            )
        old_token = Token.objects.filter(user=user)
        old_token.delete()
        token = Token.objects.create(user=user)
        return JsonResponse({
            "code": 0,
            "msg": "login success!",
            "username": user.username,
            "token": token.key
        })

class UserView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        return JsonResponse({
            "code": 0,
            "msg": "身份验证通过!",
        })

class DemoView(APIView):
    def post(self, request, *args, **kwargs):
        return JsonResponse({
            "code": 0,
            "msg": "成功!",
            "datas": [
                {
                    "age": 20,
                    "create_time": "2019-09-15",
                    "id": 1,
                    "mail": "283340479@qq.com",
                    "name": "yoyo",
                    "sex": "M"
                },
                {
                    "age": 21,
                    "create_time": "2019-09-16",
                    "id": 2,
                    "mail": "yoyo111",
                    "sex": "M"

                }
            ]
        })





def post_list(request, category_id=None, tag_id=None):
    tag = None
    category = None
    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)

    elif category_id:
        post_list, category = Post.get_by_category(category_id)

    else:
        post_list = Post.latest_posts()

    context = {
        'category': category,
        'tag': tag,
        'post_list': post_list,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request, 'blog/list.html', context=context)



def post_detail(request, post_id=None):
    try:
        post = Post.objects.get(id=post_id)



    except Post.DoesNotExist:
        post = None

    context = {
        'post': post,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request, 'blog/detail.html', context=context)

def demo(request):
    return render(request, 'blog/demo.html')






