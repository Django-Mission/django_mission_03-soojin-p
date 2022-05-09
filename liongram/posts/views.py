from multiprocessing import context
from re import template
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse,JsonResponse
from django.views.generic import ListView

from .models import Post
from .forms import PostBaseForm

def index(request):
        # post_list = Post.objects.all().select_related('writer').prefetch_related('comment_set').order_by('-created_at')
    post_list = Post.objects.all().order_by('-created_at')
    context = {
        'post_list': post_list,
    }
    return render(request, 'index.html', context)
    #return render(request,'index.html')


def post_list_view(request):
    #post_list  = Post.object.all() #Post 전체 데이터 조회
    #post_list = Post.objects.all()
    post_list = Post.objects.filter(writer=request.user)#Post.wirte가 현재 로그인인 거 조회
    context = {
        'post_list': post_list,
    }
    return render(request, 'posts/post_list.html', context)


def post_detail_view(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return redirect('index')
    context = {
        'post': post,
    }
    return render(request,'posts/post_detail.html',context)


@login_required
def post_create_view(request):
    if request.method == 'GET':
        return render(request, 'posts/post_form.html')
    else:
        image = request.FILES.get('image')
        content = request.POST.get('content')
        print(image)
        print(content)
        Post.objects.create(
            image=image,
            content=content,
            writer=request.user,
        )
        return redirect('index')

@login_required
def post_create_view(request):
    if request.method == 'GET':
        return render(request, 'posts/post_form.html', {'form': PostBaseForm()})
    else:
        form = PostBaseForm(request.POST, request.FILES)

        if form.is_valid():
            Post.objects.create(
                image=form.cleaned_data.get('image'),
                content=form.cleaned_data.get('content'),
                writer=request.user,
            )
        else:
            return redirect('posts:post-create')

        return redirect('index')


def post_update_view(request, id):
    #post = get_object_or_404(Post, id=id)
    post = Post.objects.get(id=id)

    if request.method == 'GET':
        context = { 'post': post }
        return render(request, 'posts/post_form.html', context)
    else:
        new_image = request.FILES.get('image')
        content = request.POST.get('content')

        if new_image:
            post.image.delete()
            post.image = new_image

        post.content = content
        post.save()
        return redirect('posts:post-detail', post.id)

@login_required
def post_delete_view(request, id):
    post = get_object_or_404(Post, id=id)
#   post = get_object_or_404(Post, id=id,writer=request.user)
    if request.user != post.writer:
        raise Http404('잘못된 접근입니다.')
        
    if request.method == 'GET':
        context = { 'post': post }
        return render(request,'posts/post_confrim_delete.html',context)
    else:
        post.delete()
        return redirect('index')

def url_view(request):
    print('url_view()')
    data = {'code': '001', 'msg':'OK'}
    return HttpResponse('<h1>url_view</h1>')
    #return JsonResponse(data)

def url_parameter_view(request, username):
    print('url_parameter_view')
    print(f'username:{username}') 
    print(f'request.GET:{request.GET}')#쿼리파라미터 ?key=value&abc=aaa
    return HttpResponse(username)

def function_view(request):
    print(f'request.method:{request.method}')

    if request.method == 'GET':
        print(f'request.GET:{request.GET}')
    elif request.method == 'POST':
        print(f'request.POST:{request.POST}')
    return render(request,'view.html')

class class_view(ListView):
    model = Post
    ordering = ['-id']
    #template_name = 'cbv_view.html' 

def function_view(request):
    object_list = Post.objects.all().order_by('-id')
    return render(request,'cbv_view.html',{'object_list': object_list})