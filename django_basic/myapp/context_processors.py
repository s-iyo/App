from .models import Tags, Month

def tags_and_months(request):
    return {
        'tags': Tags.objects.all(),
        'months': Month.objects.all(),
    }