import uuid
from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
import helpers

# Create your models here.

helpers.cloudinary_init()

class status(models.TextChoices):
    PUBLISHED = "pub", "Published"
    # the first value is the database value and the second one is the human readable one --> jo code mei dikhayega
    DRAFT = "draft", "Draft"
    COMING_SOON = "soon", "Coming soon"
    
    
class access(models.TextChoices):
    ANYONE = "anyone", "Anyone"
    EMAIL = "email", "Email_Required"
    # PURCHASE = "purchase", "Purchase_Required"
    # USER = "user", "User_Required"


def generate_public_id(instance, *args, **kwargs):
    unique_id =str(uuid.uuid4()).replace("-", "")
    if instance.title:
        slug = slugify(instance.title)
        unique_id_short = unique_id[:5]
        return f"{slug}-{unique_id_short}"
    # return instance.__class__.__name__

def get_public_id_prefix(instance, *args, **kwargs):
    '''
        Cloudinary helper function that sets the prefix for the public id for easy image management in cloudinary media explorer.
    '''
    # print(args, kwargs) # to find out what arguments are passed

    # if instance.title:
    #     slug = slugify(instance.title)
    #     unique_id = str(uuid.uuid4()).replace("-", "")[:5]
    #     return f"{instance.__class__.__name__}/{slug}-{unique_id}"
    # return instance.__class__.__name__

    # if hasattr checks if the attribute exists or not
    # if self.title checks if the attribute exists and its value is not falsy like "", 0 or null something like that
    
    if hasattr(instance, 'path'):
        path = instance.path
        if path[0] == "/":
            path = path[1:]
        if path[-1] == "/":
            path = path[:-1]
        return path

    public_id = instance.public_id
    if public_id:
        return f"{slugify(instance.instance.__class__.__name__)}/{public_id}"
    return instance.__class__.__name__

def get_display_name(instance, *args, **kwargs):
    '''
        Cloudinary helper function that sets the prefix for the public id for easy image management in cloudinary media explorer.
    '''
    return f"{instance.title}_thumbnail"

class Course(models.Model):
    title = models.CharField(max_length=255)
    public_id = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    # image = models.ImageField(upload_to='images')
    
    # access = [
    #     ("Anyone", "Anyone"),
    #     ("Email", "Email_Required"),
    #     # "Purchase": "Purchase_Required",
    #     # "User": "User_Required",
    # ],
    
    # class based text choices are better as usme default choices bhi rehti hai
    #! these arguments are mentioned in cloudinary documentation, optional parameters 
    # TODO -->  https://cloudinary.com/documentation/image_upload_api_reference#upload_optional_parameters
    images = CloudinaryField(
        'image',
        null=True,
        blank=True,
        public_id_prefix=get_public_id_prefix, display_name=get_display_name,
        tags=["course", "thumbnail"]
    )

    # If you added parentheses (get_public_id_prefix()), the function would execute immediately, and the result (a string) would be passed to the CloudinaryField. This is not desired in this case because the value depends on the specific instance and possibly runtime context.

    
    access = models.CharField(
        max_length=25,
        choices=access.choices,
        default=access.ANYONE
    )
    
    status = models.CharField(
        max_length=25,
        choices=status.choices,
        default=status.DRAFT
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # def __str__(self):
    #     return self.title
    # this is not needed when admin.py mei list display mei title enabled hai
    
    #? Overriding the default save method
    
    def save(self, *args, **kwargs):
        # default save method --> super.save(*args, **kwargs)
        if self.public_id == "" or self.public_id is None:
            self.public_id = generate_public_id(self)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return self.path
    
    @property
    def path(self):
        return f"/courses/{self.public_id}"
    
    @property
    def is_published(self):
        return self.status == status.PUBLISHED

    @property
    def is_coming_soon(self):
        return self.status == status.COMING_SOON
    
    
    # @property
    # def image_admin(self):
    # !    """img.build_url(width=100, height=100, crop="fill")
    #!     http://res.cloudinary.com/cloud_name/image/upload/c_fill,h_100,w_100/sample.png
        
    #!     build url cloudinary field ka function hai"""
    #     if not self.image:
    #         return ""
    #     image_options = {
    #         "width": 200
    #         # "height": 200
    #     }
    #     url = self.image.build_url(**image_options)
    #     return url

    @property
    def image_admin(self):
        # if not self.images:
        #     return ""
        # image_options = {
        #     "width": 200
        # }
        # url = self.images.build_url(**image_options)
        # return url

        return helpers.get_cloudinary_image_object(
            self, 
            field_name="images",
            as_html=False,
            width=200
        )

        
    def get_image_thumbnail(self, as_html=False, width=500):
        # if not self.images:
        #     return ""
        # image_options = {
        #     "width": width
        #     # "height": 200
        # }
        
        # if as_html: # return the html
        #     return self.images.image(**image_options) # refer cloudinary docs from pyPI
        # url = self.images.build_url(**image_options)
        # return url

        return helpers.get_cloudinary_image_object(
            self, 
            field_name="images",
            as_html=as_html,
            width=width
        )

# Lesson.objects.all() # lesson queryset -> all rows
# Lesson.objects.first()
# course_obj = Course.objects.first()
# course_qs = Course.objects.filter(id=course_obj.id)
# Lesson.objects.filter(course__id=course_obj.id)
# ! double underscore __ --> foreign key ke rows ka reference hai
# course_obj.lesson_set.all()
# course_obj.modelname_set.all()
# lesson_obj = Lesson.objects.first()
# ne_course_obj = lesson_obj.course
# ne_course_lessons = ne_course_obj.lesson_set.all()
# lesson_obj.course_id
# course_obj.lesson_set.all().order_by("-title")

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lesson")
    #! hidden course_id field
    # on delete means if course is deleted then all related lessons will be deleted
    public_id = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    # db_index is true speeds up our querying as we are using public id as lookups
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    # status = models.CharField(
    #     max_length=255,
    #     choices=status.choices,
    #     default=status.Draft
    # )
    
    thumbnail = CloudinaryField(
        'image',
        null=True,
        blank=True,
        public_id_prefix=get_public_id_prefix, display_name=get_display_name,
        tags=["lesson", "thumbnail"]
    )
    video = CloudinaryField(
        'video',
        null=True,
        blank=True,
        resource_type="video",
        public_id_prefix=get_public_id_prefix, display_name=get_display_name,
        type = "private",
        tags=["lesson", "video"]
    )
    order = models.IntegerField(default=0)
    can_preview = models.BooleanField(default=False, help_text="If user does not have access to course, can they see this?")
    status = models.CharField(
        max_length=25,
        choices=status.choices,
        default=status.PUBLISHED
    )
    updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # default save method --> super.save(*args, **kwargs)
        if self.public_id == "" or self.public_id is None:
            self.public_id = generate_public_id(self)
        super().save(*args, **kwargs) # ye save se pehle hai
    
    def get_absolute_url(self):
        return self.path
    
    @property
    def path(self):
        course_path = self.course.path
        if course_path[-1] == "/":
            course_path = course_path[:-1]
        return f"{course_path}/lessons/{self.public_id}"
    
    @property
    def is_coming_soon(self):
        return self.status == status.COMING_SOON

    @property
    def has_video(self):
        return self.video is not None

    
    class Meta:
        '''
        here the order of lessons will be according to order field
        
        order ka jyada priority hai, -updated matlab newest to oldest hai
        '''
        ordering = ["order", "-updated"]
        