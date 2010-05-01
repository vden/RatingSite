from django.db import models 
from django.contrib.auth.models import User, UserManager

class Profile(User):
    """User with app settings."""
    timezone = models.CharField(max_length=50, default='')
    
    # Use UserManager to get the create_user method, etc.
    objects = UserManager()
