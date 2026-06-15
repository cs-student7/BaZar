from django.shortcuts import render, get_object_or_404, redirect
from .models import Bike ,TestRide
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
import json
from .models import BikeDesign
from django.db import models
from django.db.models import Q


BIKES = [
    {
        "name": "Yamaha R15",
        "type": "sports",
        "price": 450000,
        "mileage": "40 km/l",
        "engine": "155cc",
        "top_speed": "140 km/h"
    },
    {
        "name": "TVS iQube",
        "type": "electric",
        "price": 300000,
        "mileage": "100 km/charge",
        "engine": "Electric",
        "top_speed": "80 km/h"
    },
    {
        "name": "Royal Enfield Classic 350",
        "type": "cruiser",
        "price": 550000,
        "mileage": "35 km/l",
        "engine": "349cc",
        "top_speed": "120 km/h"
    }
]


def bike_list(request):
    query = request.GET.get('search', '').strip()

    if query:
        bikes = Bike.objects.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(description__icontains=query)
        ).distinct()
    else:
        bikes = Bike.objects.all()

    return render(request, 'bike.html', {
        'bikes': bikes,
        'query': query,
        'results_count': bikes.count(),
    })  

def background(request):
    query = request.GET.get('search', '').strip()
    bikes = Bike.objects.all()

    if query:
        bikes = bikes.filter(
            models.Q(name__icontains=query) |
            models.Q(brand__icontains=query)
        )

    return render(request, 'base.html', {
        'query': query,
        'bikes': bikes,
    })

def learn_more(request):
    return render(request, 'learn_more.html')

def bike_detail(request, bike_id):
    # This looks for the bike with the ID from the URL
    bike = get_object_or_404(Bike, pk=bike_id) 
    return render(request, 'details.html', {'bike': bike})

def test_ride(request):
    if request.method == "POST":
        TestRide.objects.create(
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),

            city=request.POST.get('city'),
            address=request.POST.get('address'),

            license_number=request.POST.get('license_number'),
            license_expiry=request.POST.get('license_expiry'),
            preferred_bike=request.POST.get('preferred_bike'),

            preferred_date=request.POST.get('preferred_date'),
            preferred_time=request.POST.get('preferred_time'),

            message=request.POST.get('message'),
            agree_terms=True if request.POST.get('agree_terms') else False
        )

        return redirect('success')  # create this page later

    return render(request, 'test_ride.html')


def add_to_cart(request, bike_id):
    cart = request.session.get('cart', [])

    # add new item without deleting old ones
    cart.append(bike_id)

    request.session['cart'] = cart

    return redirect('cart')


def cart(request):
    cart_ids = request.session.get('cart', [])

    bikes = Bike.objects.filter(id__in=cart_ids)

    return render(request, 'cart.html', {'bikes': bikes})


# open designer page
@csrf_protect
def design_bike(request):
    """
    Display the bike design studio page
    """
    return render(request, 'bike_design.html')
 
 
@require_http_methods(["POST"])
@csrf_protect
def save_design(request):
    """
    Save a bike design to the database
    Expects JSON POST data with 'name' and 'design_data' fields
    """
    try:
        # Parse JSON data from request body
        data = json.loads(request.body)
        
        name = data.get('name', '').strip()
        design_data = data.get('design_data', '')
 
        # Validation
        if not name:
            return JsonResponse({
                'status': 'error',
                'message': 'Design name is required'
            }, status=400)
 
        if not design_data:
            return JsonResponse({
                'status': 'error',
                'message': 'Design data is missing'
            }, status=400)
 
        if len(name) > 100:
            return JsonResponse({
                'status': 'error',
                'message': 'Design name is too long (max 100 characters)'
            }, status=400)
 
        # Save the design
        design = BikeDesign.objects.create(
            name=name,
            design_data=design_data
        )
 
        return JsonResponse({
            'status': 'saved',
            'design_id': design.id,
            'message': f'Design "{name}" saved successfully!'
        })
 
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON data'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=500)
 
 
def design_list(request):
    """
    Display all saved bike designs
    Returns JSON with list of designs
    """
    try:
        designs = BikeDesign.objects.all().order_by('-created_at')
        
        # Prepare data
        designs_data = [{
            'id': design.id,
            'name': design.name,
            'created_at': design.created_at.isoformat(),
        } for design in designs]
        
        return JsonResponse({
            'status': 'success',
            'designs': designs_data,
            'count': len(designs_data)
        })
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=500)
 
 
def get_design(request, design_id):
    """
    Get a single design by ID
    Returns JSON with design details
    """
    try:
        design = BikeDesign.objects.get(id=design_id)
        
        return JsonResponse({
            'status': 'success',
            'id': design.id,
            'name': design.name,
            'design_data': design.design_data,
            'created_at': design.created_at.isoformat()
        })
    
    except BikeDesign.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Design not found'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=500)
 
 
@require_http_methods(["POST"])
@csrf_protect
def delete_design(request, design_id):
    """
    Delete a design
    """
    try:
        design = BikeDesign.objects.get(id=design_id)
        design_name = design.name
        design.delete()
        
        return JsonResponse({
            'status': 'deleted',
            'message': f'Design "{design_name}" deleted successfully!'
        })
    
    except BikeDesign.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Design not found'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=500)
 
 
@require_http_methods(["POST"])
@csrf_protect
def update_design(request, design_id):
    """
    Update an existing design
    """
    try:
        data = json.loads(request.body)
        
        design = BikeDesign.objects.get(id=design_id)
        
        # Update name if provided
        if 'name' in data and data['name'].strip():
            design.name = data['name'].strip()
        
        # Update design data if provided
        if 'design_data' in data:
            design.design_data = data['design_data']
        
        design.save()
        
        return JsonResponse({
            'status': 'updated',
            'message': f'Design "{design.name}" updated successfully!'
        })
    
    except BikeDesign.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Design not found'
        }, status=404)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON data'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=500)