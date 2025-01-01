from django.shortcuts import render
from django.http import Http404, JsonResponse
from . import services


# Create your views here.

def index(request):
    return render(request, 'index.html')

def courses(request):
    return render(request, 'courses.html')

def course_list_view(request):
    queryset = services.get_publish_courses()
    print(queryset)
    context = {}
    return JsonResponse({
        "data": [x.path for x in queryset]
    })
    return render(request, 'courses/list.html', context)

def course_detail_view(request, course_id=None, *args, **kwargs):
    course_obj = services.get_course_detail(course_id=course_id)
    
    if course_obj is None:
        raise Http404
    lesson_queryset = course_obj.lesson.all()
    # as related name lesson hai toh isliye lesson aaya hai nhi toh lesson_set aata
    context = {}
    return JsonResponse({
        "data": course_obj.id,
        "lessons": [x.path for x in lesson_queryset]
    })
    return render(request, 'courses/detail.html', context)

def lesson_detail_view(request, lesson_id=None, course_id=None, *args, **kwargs):
    lesson_obj = services.get_lesson_detail(
        course_id=course_id,
        lesson_id=lesson_id
    )
    
    if lesson_obj is None:
        raise Http404
    context = {}
    return JsonResponse({
        "data": lesson_obj.id
    })
    return render(request, 'courses/lesson.html', context)