from django.shortcuts import render
from django.http import Http404, JsonResponse
from . import services
import helpers


# Create your views here.

def index(request):
    return render(request, 'index.html')

def courses(request):
    return render(request, 'courses.html')

def course_list_view(request):
    queryset = services.get_publish_courses()
    # print(queryset)
    context = {
        "object_list": queryset
    }
    # return JsonResponse({
    #     "data": [x.path for x in queryset]
    # })
    return render(request, 'courses/list.html', context)

def course_detail_view(request, course_id=None, *args, **kwargs):
    course_obj = services.get_course_detail(course_id=course_id)
    
    if course_obj is None:
        raise Http404
    lesson_queryset = services.get_course_lessons(course_obj)
    # as related name lesson hai toh isliye lesson aaya hai nhi toh lesson_set aata
    context = {
        "object": course_obj,
        "lessons_queryset": lesson_queryset
    }
    # return JsonResponse({
    #     "data": course_obj.id,
    #     "lessons": [x.path for x in lesson_queryset]
    # })
    return render(request, 'courses/detail.html', context)

def lesson_detail_view(request, lesson_id, course_id, *args, **kwargs):
    lesson_obj = services.get_lesson_detail(
        course_id=course_id,
        lesson_id=lesson_id
    )
    
    if lesson_obj is None:
        raise Http404
    
    context = {
        "object": lesson_obj
    }
    # return JsonResponse({
    #     "data": lesson_obj.id
    # })
    
    template_name = "courses/lesson_soon.html"
    
    video_embed_html = helpers.get_cloudinary_video_object(
            lesson_obj,
            width=1250,
            field_name='video',
            as_html=True,
        )
    
    
    # agar coming soon nai hai toh lesson.html aayega
    # nai toh coming soon ka hi page default hai
    if not lesson_obj.is_coming_soon and lesson_obj.has_video:
        template_name = "courses/lesson.html"
        
        context['video_embed'] = video_embed_html
        
    return render(request, template_name, context)