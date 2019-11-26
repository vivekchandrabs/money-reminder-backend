from rest_framework.routers import DefaultRouter

from django.urls import path, include

from reminder.viewsets import SignUpViewSet, FixedDepositViewSet

router = DefaultRouter()
router.register(r'signup', SignUpViewSet, base_name="SignUp")
router.register(r'fd', FixedDepositViewSet, base_name="FixedDeposit")

urlpatterns=[
	path('',include(router.urls))
]

