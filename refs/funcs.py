from django.contrib.auth.models import Permission


def get_user_regions(user):
    permissions = Permission.objects.filter(
        user=user) | Permission.objects.filter(group__user=user)
    user_regions = []
    for p in permissions:
        if p.codename in ['22', '24', '38', '42', '54', '55', '70']:
            user_regions.append(p.codename)
    return user_regions