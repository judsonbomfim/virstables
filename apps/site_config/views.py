import os
from django.shortcuts import render, get_object_or_404, redirect
from .models import SiteSettings, Banner, Logo
from .forms import BannerForm, LogoForm, SiteSettingsForm
from PIL import Image

def resize_image(obj, target_width):
    if obj.imagem:
        img_path = obj.imagem.path
        img = Image.open(img_path)
        if img.width != target_width:
            ratio = target_width / float(img.width)
            height = int(float(img.height) * ratio)
            img = img.resize((target_width, height), Image.LANCZOS)
            img.save(img_path)
            

def site_config_detalhes(request):
    site_settings = SiteSettings.objects.first()
    banners = Banner.objects.order_by('ordem')
    logos = Logo.objects.order_by('ordem')
    context = {
        'site_settings': site_settings,
        'banners': banners,
        'logos': logos,
    }
    return render(request, 'backend/site_config_detalhes.html', context)

def site_settings_edit(request, pk):
    site_settings = get_object_or_404(SiteSettings, pk=pk)
    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, instance=site_settings)
        if form.is_valid():
            form.save()
            return redirect('site_config_backend:site_config_detalhes')
    else:
        form = SiteSettingsForm(instance=site_settings)
    return render(request, 'backend/site_settings_form.html', {'form': form})

def banner_add(request):
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            banner = form.save()
            resize_image(banner, 1440)
            return redirect('site_config_backend:site_config_detalhes')
    else:
        form = BannerForm()
    return render(request, 'backend/banner_form.html', {'form': form})

def banner_edit(request, pk):
    banner = get_object_or_404(Banner, pk=pk)
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES, instance=banner)
        if form.is_valid():
            banner = form.save()
            resize_image(banner, 1440)
            return redirect('site_config_backend:site_config_detalhes')
    else:
        form = BannerForm(instance=banner)
    return render(request, 'backend/banner_form.html', {'form': form})

def banner_delete(request, pk):
    banner = get_object_or_404(Banner, pk=pk)
    if request.method == 'POST':
        # Apaga o arquivo de imagem do banner, se existir
        if banner.imagem and os.path.isfile(banner.imagem.path):
            os.remove(banner.imagem.path)
        banner.delete()
        return redirect('site_config_backend:site_config_detalhes')
    return render(request, 'backend/banner_confirm_delete.html', {'banner': banner})

def logo_add(request):
    if request.method == 'POST':
        form = LogoForm(request.POST, request.FILES)
        if form.is_valid():
            logo = form.save()
            resize_image(logo, 600)
            return redirect('site_config_backend:site_config_detalhes')
    else:
        form = LogoForm()
    return render(request, 'backend/logo_form.html', {'form': form})

def logo_edit(request, pk):
    logo = get_object_or_404(Logo, pk=pk)
    if request.method == 'POST':
        form = LogoForm(request.POST, request.FILES, instance=logo)
        if form.is_valid():
            logo = form.save()
            resize_image(logo, 600)
            return redirect('site_config_backend:site_config_detalhes')
    else:
        form = LogoForm(instance=logo)
    return render(request, 'backend/logo_form.html', {'form': form})

def logo_delete(request, pk):
    logo = get_object_or_404(Logo, pk=pk)
    if request.method == 'POST':
        # Apaga o arquivo de imagem do logo, se existir
        if logo.imagem and os.path.isfile(logo.imagem.path):
            os.remove(logo.imagem.path)
        logo.delete()
        return redirect('site_config_backend:site_config_detalhes')
    return render(request, 'backend/logo_confirm_delete.html', {'logo': logo})