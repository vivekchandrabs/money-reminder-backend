from rest_framework import viewsets
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from djcelery.models import PeriodicTask, IntervalSchedule, CrontabSchedule
import json
import random


from django.contrib.auth.models import User

from reminder.models import FDAccountDetail, Interest
from reminder.serializers import FDSerializer
from reminder.tasks import calculate_interest, send_interest_reminder, update_interest


def create_periodic_schedule():
    cron_tab = CrontabSchedule.objects.create(day_of_month=1, hour=12, minute=15)

    return cron_tab

class SignUpViewSet(viewsets.ModelViewSet):
    
    def create(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        user = User.objects.filter(username=email)

        if user.exists():
            return Response({"error":"Username already exists"}, status=406)
        
        user = User.objects.create_user(email=email,
                                   username=email,
                                   password=str(password))

        token = Token.objects.create(user=user)
        return Response({"token":token.key})


class FixedDepositViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = FDSerializer
    # queryset = FDAccountDetail.objects.all()

    def create_periodic_task(self, fd, fd_name, period, cron_tab):
        app_dict = {"months":str(period), "fd_primary_key":fd.pk}
        app_json = json.dumps(app_dict)

        periodic_task = PeriodicTask.objects.create(name=fd_name, 
                                                    task="reminder.tasks.send_interest_reminder",
                                                    crontab = cron_tab,
                                                    enabled=True,
                                                    kwargs=app_json)
        return periodic_task
    
    def create(self, request):
        user = request.user
        fd_name = request.data.get("fd_name")
        principal = request.data.get("principal")
        type_of_interest = request.data.get("type_of_interest")
        rate_of_interest = request.data.get("rate_of_interest")
        time_of_interest = request.data.get("time_of_interest")
        period = request.data.get("period")
        bank = request.data.get("bank")
        branch = request.data.get("branch")

        arguments = {}
        arguments["principal"] = request.data.get("principal")
        arguments["type_of_interest"] = request.data.get("type_of_interest")
        arguments["rate_of_interest"] = request.data.get("rate_of_interest")
        arguments["time_of_interest"] = request.data.get("time_of_interest")
        arguments["period"] = request.data.get("period")

        fd = FDAccountDetail.objects.create(user=user,
                                            fd_name=fd_name,
                                            principal=int(principal),
                                            type_of_interest=int(type_of_interest),
                                            period=int(period),
                                            rate_of_interest=rate_of_interest,
                                            time_of_interest=time_of_interest,
                                            bank=bank,
                                            amount=principal,
                                            branch=branch)



        cron_tab = create_periodic_schedule()
        fd.cron_tab = cron_tab

        while True:
            try:
                fd.periodic_task = self.create_periodic_task(fd, fd_name, period, cron_tab=cron_tab)
                break
            except:
                fd_name = fd_name + str(int(random.random()*1000000))

        fd.save()
        serialized_data = FDSerializer(fd).data

        calculate_interest.delay(arguments, fd)

        return Response(serialized_data)

    def list(self, request):
        user = request.user        
        fd_instances = FDAccountDetail.objects.filter(user=user)        
        serialized_data = FDSerializer(fd_instances, many=True).data
        
        return Response(serialized_data)

    def partial_update(self, request, pk):
        user = request.user
        fd_instance = FDAccountDetail.objects.get(pk=pk)

        if user == fd_instance.user:            
            serializer = FDSerializer(fd_instance, request.data, partial=True)

            if serializer.is_valid():
                serializer.save()

                arguments = {}
                arguments["principal"] = fd_instance.principal
                arguments["type_of_interest"] = fd_instance.type_of_interest
                arguments["rate_of_interest"] = fd_instance.rate_of_interest
                arguments["time_of_interest"] = fd_instance.time_of_interest
                arguments["period"] = fd_instance.period
                
                interest_instances = Interest.objects.filter(fd=fd_instance)
                update_interest.delay(arguments, interest_instances)

            return Response(serializer.data)
        
        return Response({"Error":"Your not allowed to perform this operation"}, status=401)

    def destory(self, request):
        user = request.user
        fd_pk = request.data.get("fd_pk")
        fd_instance = FDAccountDetail.objects.get(pk=fd_pk)
        
        if user == fd_instance.user:
            fd_instance.delete()
        
            return Response({"message":"Sucessfully deleted the FD"})

        return Response({"error":"Your not allowed to perform this operation"}, status=401)


class InterestViewSet(viewsets.ModelViewSet):
    
    def list(self, request):
        user = request.user
        fd_pk = request.GET.get("fd_pk")
        fd_instance = FDAccountDetail.objects.get(pk=fd_pk)
        
        interest_instances = Interest.objects.filter(fd=fd_instance)

        serialized_data = InterestSerializer(interest_instances, many=True).data

        return Response(serialized_data)
    
    def create(self, request):
        pass

    def destory(self, request):
        pass

    def partial_update(self, request):
        pass        

        



            
        
        

        

    