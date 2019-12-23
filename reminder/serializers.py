from rest_framework import serializers

from django.contrib.auth.models import User

from reminder.models import FDAccountDetail, Interest, TYPE_OF_INTEREST, TIME_OF_INTEREST

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ("id", "username", "email")


class FDSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    type_of_interest = serializers.SerializerMethodField()
    time_of_interest = serializers.SerializerMethodField()

    def get_user(self, obj):
        return UserSerializer(obj.user).data

    def get_type_of_interest(self, obj):
        return TYPE_OF_INTEREST[obj.type_of_interest-1][1]

    def get_time_of_interest(self, obj):
        return TIME_OF_INTEREST[obj.time_of_interest-1][1]
        
    class Meta:
        model = FDAccountDetail
        fields = ("id", "user", "fd_name", "principal", 
                    "type_of_interest", "period", "amount", 
                      "time_of_interest", "rate_of_interest", 
                      "bank", "branch")

class InterestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Interest
        fields = ("id", "interest_amt", "month", "is_sent")
        depth = 1
