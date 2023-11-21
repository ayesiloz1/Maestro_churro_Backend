from rest_framework import viewsets
from .models import Churro, Survey, Career, Contact, Order
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import ChurroSerializer
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.views.decorators.http import require_http_methods
from django.core.files.base import ContentFile
import json
from .models import Order, OrderItem, MenuItem
from django.db.models import Q
from .models import Booking
class ChurroViewSet(viewsets.ModelViewSet):
    queryset = Churro.objects.all()
    serializer_class = ChurroSerializer


def home(request):
    return HttpResponse("Welcome to the Churro API!")

def churro_create_view(request):
    if request.method == 'POST':
        # Extract data from the POST request
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        imageUrl = request.POST.get('imageUrl')  # Make sure 'imageUrl' matches the field name in your form

        # Validate the data (add more validation as needed)
        if not name or not description or not price or not imageUrl:
            return JsonResponse({'error': 'All fields are required.'}, status=400)

        try:
            price = float(price)  # Convert 'price' to a float (assuming it's a numeric field)

            # Create the churro instance and save it to the database
            churro = Churro(name=name, description=description, price=price, imageUrl=imageUrl)
            churro.save()

            # Return a JsonResponse with a success message
            return JsonResponse({'message': 'Churro created successfully!'}, status=201)

        except ValueError:
            return JsonResponse({'error': 'Invalid price format.'}, status=400)

    else:
        
        return JsonResponse({'error': 'Unsupported method.'}, status=405)


@csrf_exempt
@require_http_methods(["POST"])
def submit_survey(request):
    try:
        data = json.loads(request.body)
        experience = data.get('experience')
        feedback = data.get('feedback')
        new_survey = Survey(experience=experience, feedback=feedback)
        new_survey.save()  
        return JsonResponse({'message': 'Survey submitted successfully'}, status=201)
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    

from django.core.files.base import ContentFile
import os

@csrf_exempt
@require_http_methods(["POST"])
def submit_career(request):
    try:
        name = request.POST.get('name')
        email = request.POST.get('email')
        resume = request.FILES.get('resume')

        if not name or not email or not resume:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        # Extract file extension and create a resume filename
        _, ext = os.path.splitext(resume.name)
        resume_filename = f'{name}_Resume{ext}'

        # Save the resume to the default storage
        resume_path = default_storage.save('resumes/' + resume_filename, resume)

        # Create a Career object
        Career.objects.create(name=name, email=email, resume=resume_path)

        # Return a success response
        return JsonResponse({'message': 'Application submitted successfully'}, status=201)

    except Exception as e:
        # Log the exception for debugging
        print(f"An error occurred: {e}")
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def submit_contact(request):
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body)

        # Extract data from the parsed JSON
        method = data.get('method')
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        if not method or not message or (method == 'email' and not email) or (method == 'message' and not name):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        # Create a Contact object and save it
        Contact.objects.create(method=method, name=name, email=email, message=message)

        # Return a success response
        return JsonResponse({'message': 'Contact message sent successfully'}, status=201)

    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        # Log the exception for debugging
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def submit_order(request):
    print("Received data:", request.body.decode('utf-8')) 
    try:
        data = json.loads(request.body)
        order_items_data = data.get('order')
        
        if not order_items_data:
            return JsonResponse({'error': 'No order items provided'}, status=400)

        new_order = Order.objects.create()

        for item_name, quantity in order_items_data.items():
            print(f"Processing item: {item_name}")  # Debugging line
            menu_item = MenuItem.objects.filter(name=item_name.strip()).first()

            if not menu_item:
                print(f"Menu item {item_name} not found")  # Debugging line
                return JsonResponse({'error': f'Menu item {item_name} not found'}, status=400)

            if quantity > 0:
                OrderItem.objects.create(
                    order=new_order,
                    item=menu_item,
                    quantity=quantity
                )

        return JsonResponse({'message': 'Order submitted successfully', 'order_id': new_order.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)



@csrf_exempt
@require_http_methods(["POST"])
def submit_booking(request):
    try:
        data = json.loads(request.body)

        name = data.get('name')
        email = data.get('email')
        eventType = data.get('eventType')
        date = data.get('date')
        additionalInfo = data.get('additionalInfo')

        if not all([name, email, eventType, date]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        Booking.objects.create(
            name=name,
            email=email,
            eventType=eventType,
            date=date,
            additionalInfo=additionalInfo
        )

        return JsonResponse({'message': 'Booking submitted successfully'}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
