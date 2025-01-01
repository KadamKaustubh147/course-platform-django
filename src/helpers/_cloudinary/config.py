import cloudinary
from decouple import config
from django.conf import settings

# Configuration

def cloudinary_init():
    cloudinary.config( 
        cloud_name = config("CLOUDINARY_CLOUD_NAME"), 
        api_key = config("CLOUDINARY_API_KEY"), 
        api_secret = config("CLOUDINARY_SECRET_API_KEY"), # Click 'View API Keys' above to copy your API secret
        # cloud_name = "ddru17qmx", 
        # api_key = "623229811174356", 
        # api_secret = "tt53cp2FcgwGUumhJ04Qiph_uOw", # 
        secure=True
    )