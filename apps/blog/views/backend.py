import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from ..models import Post
from ..forms import PostForm
from django.urls import reverse
from PIL import Image

def resize_post_image(post, target_width=1440):
    if post.imagem and hasattr(post.imagem, 'path'):
        img_path = post.imagem.path
        img = Image.open(img_path)
        if img.width > target_width:
            ratio = target_width / float(img.width)
            height = int(float(img.height) * ratio)
            img = img.resize((target_width, height), Image.LANCZOS)
            img.save(img_path)

def post_lista(request):
    posts = Post.objects.all().order_by('-updated_at')
    context = {
        'painel_title': settings.PAINEL_TITLE,
        'page_title': f'Lista de posts',
        'page_subtitle': 'Adicionar Foto',
        'page_icon': 'icofont icofont-articles',
        'posts': posts,
    }
    return render(request, 'backend/post_lista.html', context)

def post_adicionar(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user  # atribui o usuário logado como autor
            post.save()
            resize_post_image(post, 1440)
            return redirect('blog_backend:post_lista')
    else:
        form = PostForm()
        context = {
            'painel_title': settings.PAINEL_TITLE,
            'page_title': f'Lista de posts',
            'page_subtitle': 'Novo Post',
            'page_icon': 'icofont icofont-articles',
            'form': form,
        }
    return render(request, 'backend/post_form.html', context)

def post_editar(request, pk):
    post = get_object_or_404(Post, pk=pk)
    old_image = post.imagem
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            # Redimensiona apenas se a imagem foi alterada
            if 'imagem' in form.changed_data and post.imagem != old_image:
                resize_post_image(post, 1440)
            return redirect('blog_backend:post_lista')
    else:
        form = PostForm(instance=post)
        context = {
            'painel_title': settings.PAINEL_TITLE,
            'page_title': f'Editar Post',
            'page_subtitle': 'Atualizar Post',
            'page_icon': 'icofont icofont-articles',
            'form': form,
        }
    return render(request, 'backend/post_form.html', context)

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        # Remove a imagem do servidor, se existir
        if post.imagem and os.path.isfile(post.imagem.path):
            os.remove(post.imagem.path)
        post.delete()
        return redirect('blog_backend:post_lista')
    return render(request, 'backend/post_confirm_delete.html', {'post': post})

def post_detalhe(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {
        'painel_title': settings.PAINEL_TITLE,
        'page_title': f'Detalhe do Post',
        'page_subtitle': 'Atualizar Post',
        'page_icon': 'icofont icofont-articles',
        'post': post,
    }
    return render(request, 'backend/post_detalhe.html', context)