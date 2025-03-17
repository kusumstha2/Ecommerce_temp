from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    groups = ['Super Admin', 'Admin', 'End User']
    
    for group_name in groups:
        group, created = Group.objects.get_or_create(name=group_name)
        
        # Optionally, assign permissions to the group
        if group_name == 'Super Admin':
            permissions = Permission.objects.all()  # Give all permissions to Super Admin
            group.permissions.set(permissions)
        
        if group_name == 'Admin':
            # Add specific permissions to the Admin group
            permissions = Permission.objects.filter(codename__startswith='change_')  # Example filter
            group.permissions.set(permissions)

        group.save()
