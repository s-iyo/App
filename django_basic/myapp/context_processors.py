from .models import Tags, Month  # Monthモデルもインポート

def tags_and_months(request):
    return {
        'tags': Tags.objects.all(),
        'months': Month.objects.all(),  # すべてのMonthオブジェクトを渡す
    }