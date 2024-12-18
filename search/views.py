from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
from .models import Search
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@csrf_exempt
def create_search(request):
    if request.method == "POST":
        try:
            # Parse the JSON data
            body = json.loads(request.body)
            user_id = body.get('user_id')
            category_id = body.get('category_id')

            if not user_id or not category_id:
                return JsonResponse({'error': 'User ID and Category ID are required.'}, status=400)

            # Check if a Search record for this user already exists
            search = Search.objects.filter(user_id=user_id).first()

            if search:
                # If a record exists, call the update_search function
                return update_search(request, search.id, category_id)

            # Create a new Search record if none exists
            new_search = Search.objects.create(user_id=user_id, category_id=category_id)
            return JsonResponse({'message': 'Search created successfully.', 'search_id': new_search.id}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def update_search(request, search_id=None, new_category_id=None):
    if request.method == "POST" or search_id:
        try:
            if not search_id:
                # Parse the JSON data
                body = json.loads(request.body)
                search_id = body.get('search_id')
                new_category_id = body.get('category_id')

            if not search_id or not new_category_id:
                return JsonResponse({'error': 'Search ID and New Category ID are required.'}, status=400)

            # Update the existing search record
            search = get_object_or_404(Search, id=search_id)
            search.category_id = new_category_id
            search.save()

            return JsonResponse({'message': 'Search updated successfully.'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@api_view(['GET'])
def get_search(request, user_id):
    try:
        # Fetch the search record for the given user_id
        search_record = Search.objects.get(user_id=user_id)
        return Response({
            'user_id': search_record.user_id,
            'category_id': search_record.category_id,
        })
    except Search.DoesNotExist:
        return Response({'detail': 'Search record not found.'}, status=status.HTTP_404_NOT_FOUND)