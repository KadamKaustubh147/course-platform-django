from .models import Course, Lesson, status


# retrive a list of courses which are published
def get_publish_courses():
    return Course.objects.filter(status=status.PUBLISHED)

# retrive a single course
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

def get_course_lessons(course_obj=None):
    lessons = Lesson.objects.none() # empty queryset, empty lesson
    if not isinstance(course_obj, Course):
        return lessons
    lessons = course_obj.lesson.filter(
        course__status=status.PUBLISHED,
        # status=status.PUBLISHED,
        status__in = [status.PUBLISHED, status.COMING_SOON] # isse multiple kar sakte aur ek method ka Q lookup ka jo django models ka method hai
    )
    return lessons

def get_lesson_detail(course_id=None, lesson_id=None):
    if lesson_id is None or course_id is None:
        return None
    obj = None
    try:
        # get retrieves a single object
        obj =  Lesson.objects.get(
            course__public_id=course_id,
            course__status=status.PUBLISHED,
            status__in = [status.PUBLISHED, status.COMING_SOON],
            public_id=lesson_id
        )
    except:
        pass
    return obj