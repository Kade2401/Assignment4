def is_global_manager(user):
    return user.is_superuser or user.groups.filter(name="globals").exists()