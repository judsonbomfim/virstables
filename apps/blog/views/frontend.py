from django.shortcuts import render, get_object_or_404
from ..models import Post, Category

def post_list(request):
    posts = Post.objects.filter(published=True)
    categories = Category.objects.all()
    
    breadcrumb = [
        {'title': 'Home', 'url': '/'},
        {'title': 'Blog'},
    ]

    context = {
        'posts': posts,
        'categories': categories,
        'page_title': 'Opinião'
    }
    return render(request, 'frontend/post_list.html', context)

def post_detalhe(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    posts = Post.objects.all().order_by('-created_at')
    
    context = {
        'post': post,
        'page_title': post.titulo,
        'posts': posts
    }
    return render(request, 'frontend/post_detalhes.html', context)