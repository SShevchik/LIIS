from django.utils import six
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test


class GroupRequiredMixin(object):
    group_required = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        else:
            user_groups = []
            for group in request.user.groups.values_list('name', flat=True):
                user_groups.append(group)
            if len(set(user_groups).intersection(self.group_required)) <= 0:
                raise PermissionDenied
        return super(GroupRequiredMixin, self).dispatch(request, *args, **kwargs)


def group_required(group, login_url=None):
    def check_perms(user):
        if isinstance(group, six.string_types):
            groups = (group,)
        else:
            groups = group

        if user.groups.filter(name__in=groups).exists():
            return True
        else:
            raise PermissionDenied

    return user_passes_test(check_perms, login_url=login_url)
