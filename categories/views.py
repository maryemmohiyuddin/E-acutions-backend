from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Category
from django.core.exceptions import ObjectDoesNotExist
import json

@csrf_exempt
def add_category(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')

        if not name:
            return JsonResponse({'error': 'Name is required'}, status=400)

        category = Category.objects.create(name=name)
        return JsonResponse({'message': 'Category added successfully', 'id': category.id}, status=201)

def view_categories(request):
    categories = Category.objects.all().values('id', 'name', 'created_at')
    return JsonResponse(list(categories), safe=False)

@csrf_exempt
def delete_category(request, category_id):
    if request.method == 'DELETE':
        try:
            category = Category.objects.get(id=category_id)
            category.delete()
            return JsonResponse({'message': 'Category deleted successfully'}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Category not found'}, status=404)
