import helpers
from cloudinary import CloudinaryImage
from django.contrib import admin
from django.utils.html import format_html
from .models import Course, Lesson

# Register your models here.


# class LessonInline(admin.TabularInline):
# personally stackedinline ka mujhe better UI laga --> is case mei aur jyada accha lag rha
class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 0
    readonly_fields = [
        'public_id',
        'created_at',
        'updated',
        'display_image',
        'display_video',
    ] # as phle visible nai tha
    
    def display_image(self, course_object,*args, **kwargs):
        url = helpers.get_cloudinary_image_object(
            course_object,
            width=500,
            field_name='thumbnail',
        )
        return format_html(f"<img src='{url}' />")
        
        # iss display image ka, jo djnago admin mei naam hai voh change kar sakte 
    display_image.short_description = "Current Image"
    # the problem is this image is huge
    
    def display_video(self, course_object,*args, **kwargs):
        video_embed_html = helpers.get_cloudinary_video_object(
            course_object,
            width=500,
            field_name='video',
            as_html=True,
        )
        return video_embed_html
        
        # iss display image ka, jo djnago admin mei naam hai voh change kar sakte 
    display_image.short_description = "Current Video"

    

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    '''
        custom admin for course model ---> changing order + displaying cloudinary image
    '''
    inlines = [LessonInline]
    fields = ['public_id', 'title', 'description', 'access', 'status', 'images', 'display_image']
    readonly_fields = ['public_id','display_image']
    # order change karliya meine fields ka
    list_display = ['title', 'access', 'status']
    list_filter = ['access', 'status']
    
    # displaying the image
    
    def display_image(self, course_object,*args, **kwargs):
        # args and kwargs were used to find what arguments are passed in the function
        # print(course_object.images)
        # return format_html(f"<img src='{course_object.images.url}' />")

        # html_from_cloudinary = CloudinaryImage(
        #     course_object.images.public_id,
        # ).image(
        #     width=500,)
        # return format_html(html_from_cloudinary)
        # print(course_object.image_admin)
        # url = course_object.get_image_thumbnail(as_html=True, width=500)
        return format_html(f"<img src='{course_object.image_admin}' />")
        
        # iss display image ka, jo djnago admin mei naam hai voh change kar sakte 
    display_image.short_description = "Current Image"
        # the problem is this image is huge
    
    
        

# admin.site.register(Lesson)
