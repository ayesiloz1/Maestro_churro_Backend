
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChurroViewSet, submit_survey, submit_career, submit_contact, submit_order, home, submit_booking

router = DefaultRouter()
router.register(r'churros', ChurroViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('submit-survey/', submit_survey, name='submit_survey'),
    path('submit-career/', submit_career, name='submit_career'),
    path('submit-contact/', submit_contact, name='submit_contact'),
    path('submit-order/', submit_order, name='submit_order'),
    path('submit-booking/', submit_booking, name='submit_booking'),
    path('home/', home, name='home'),  # Assuming you want a separate endpoint for home
]