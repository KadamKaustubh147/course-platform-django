from .models import Course, Lesson, status


def get_publish_courses():
    return Course.objects.filter(status=status.PUBLISHED)

def get_course_detail(course_id=None):
    if course_id is None:
        return None
    obj = None
    try:
        # get retrieves a single object
        obj =  Course.objects.get(
            status=status.PUBLISHED,
            public_id=course_id
        )
    except:
        pass
    return obj

def get_lesson_detail(course_id=None, lesson_id=None):
    if lesson_id is None or course_id is None:
        return None
    obj = None
    try:
        # get retrieves a single object
        obj =  Lesson.objects.get(
            course__public_id=course_id,
            course__status=status.PUBLISHED,
            status=status.PUBLISHED,
            public_id=lesson_id
        )
    except:
        pass
    return obj