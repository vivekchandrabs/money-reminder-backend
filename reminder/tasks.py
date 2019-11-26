from __future__ import absolute_import, unicode_literals
from celery import task
from dateutil import relativedelta

from django.utils import timezone

from money_reminder.celery import app
from reminder.interest_calculator import fd
from reminder.models import Interest, FDAccountDetail


@app.task
def calculate_interest(arguments, fd_instance):
    principal = arguments["principal"]
    type_of_interest = int(arguments["type_of_interest"])
    rate_of_interest = int(arguments["rate_of_interest"])
    time_of_interest = int(arguments["time_of_interest"])
    period = int(arguments["period"])

    interest_calculator_instance = fd()

    date = timezone.now()

    for month_number in range(1,period+1):
        interest_calculator_instance.fill(principal,
                                            rate_of_interest,
                                            (type_of_interest),
                                            (time_of_interest),
                                            (period),
                                            month_number)

        interest_amt = interest_calculator_instance.clacu()

        if type_of_interest == 2:
            principal = interest_amt

        date = date + relativedelta.relativedelta(months=1)
        interest_instance = Interest.objects.create(fd=fd_instance, interest_amt=interest_amt, month=date)

        interest_calculator_instance.refill()
    return


@app.task
def update_interest(arguments, interest_instances):
    principal = arguments["principal"]
    type_of_interest = int(arguments["type_of_interest"])
    rate_of_interest = int(arguments["rate_of_interest"])
    time_of_interest = int(arguments["time_of_interest"])
    period = int(arguments["period"])

    interest_instances = list(interest_instances)

    if period == len(interest_instances):
        pass
    
    elif period > len(interest_instances):
        difference = period - len(interest_instances)
        
        date = interest_instances[-1].month

        for i in range(difference):
            date = date + relativedelta.relativedelta(months=1)
            interest_instance = Interest.objects.create(fd=interest_instances[0].fd,
                                                        interest_amt=0, month=date)
            interest_instances.append(interest_instance)
            
    elif period < len(interest_instances):
        difference = len(interest_instances) - period
        
        for i in range(difference):
            interest_instance_to_delete = interest_instances.pop()
            interest_instance_to_delete.delete()

    interest_calculator_instance = fd()

    for month_number, interest_instance in zip(range(1,period+1), interest_instances):
        interest_calculator_instance.fill(principal,
                                        rate_of_interest,
                                        (type_of_interest),
                                        (time_of_interest),
                                        (period),
                                        month_number)

        interest_amt = interest_calculator_instance.clacu()

        if type_of_interest == 2:
            principal = interest_amt

        interest_instance.interest_amt = interest_amt
        interest_instance.save()

        interest_calculator_instance.refill()
    return


@app.task
def send_interest_reminder(fd_primary_key, months):
    fd_instance = FDAccountDetail.objects.get(pk=fd_primary_key)
    
    interest_instances = Interest.objects.filter(fd=fd_instance, is_sent=False)

    if interest_instances.exists():
        interest_instance = interest_instances.first()
        print(fd_primary_key)
        
        interest_instance.is_sent = True
        interest_instance.save()

    if len(interest_instances) == 0:
        fd_instance.periodic_task.enabled = False
        fd_instance.periodic_task.save()

        

        
        
        
        
    



    



    