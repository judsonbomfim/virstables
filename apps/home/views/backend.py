from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from core.decorators import group_required

# Create your views here.
@login_required(login_url='/login/')
@group_required('Administradores')
def index(request):
    
    context = {
        'painel_title': settings.PAINEL_TITLE,
        'page_title': 'Home',
    }
    
    return render(request, 'backend/index.html', context)