
from django.core.exceptions import PermissionDenied
from functools import wraps

def group_required(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated or not request.user.groups.filter(name=group_name).exists():
                raise PermissionDenied("Você não tem acesso a esta página.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator