# Create your views here.
import sys

from django.db.models import Q
from django.shortcuts import render
from django_tables2   import RequestConfig
from titles.models  import Titles, Ondemand_Titles
from titles.tables  import TitlesTable,TestTable,OndemandTable
from imdb_guide.forms import ContactForm


from datetime import datetime
from datetime import timedelta
sys.path.append('C:/Users/josh/Documents/coding/django_stuff/imdb_guide/helperfunctions')




def guide(request, *args):
    """provides all guide content in 5 tables

    """
    print request
    channels_filtered=request.GET.getlist('channels')
    now = datetime.today()
    hour=now.hour
    minutes=now.minute
    if hour>12:
        hour=hour-12
    if minutes>30:
        startmin=30
        endmin=60-minutes
        timedeltastart=minutes-startmin
    else:
        startmin="00"
        endmin=30-minutes
        timedeltastart=minutes-int(startmin)
    timetostart=("%s:%s"%(hour,startmin))
    hour_list=[timetostart,hour,hour+1]
    start_times=[]
    end_times=[]
    increment=30
    howmanytables=4
    list_of_displaytimes=[]
    for a in xrange(0,howmanytables):
        start_times.append((datetime.now()-timedelta(minutes=timedeltastart+5-increment*a)).time())
        end_times.append((datetime.now()+timedelta(minutes=endmin-1+increment*(a))).time())
        displaytime=(datetime.now()-timedelta(minutes=timedeltastart-increment*a)).time()
        list_of_displaytimes.append(displaytime)



    config = RequestConfig(request,paginate={"per_page":25})

    table1= TitlesTable(Titles.objects.filter(time__lt=(start_times[0]), time__gte=(datetime.now()-timedelta(minutes=120+5)).time()),  prefix="1-")
    table2 = TitlesTable(Titles.objects.filter(time__gte=(start_times[0]), time__lt=(end_times[0])), prefix="2-")
    table3= TitlesTable(Titles.objects.filter(time__gte=(start_times[1]), time__lt=(end_times[1])), prefix="3-")
    table4 = TitlesTable(Titles.objects.filter(time__gte=(start_times[2]), time__lt=(end_times[2])), prefix="4-")
    table5 = TitlesTable(Titles.objects.filter(time__gte=(start_times[3]), time__lt=(end_times[3])), prefix="5-")

    config.configure(table1)
    config.configure(table2)
    config.configure(table3)
    config.configure(table4)
    config.configure(table5)
    
    return render(request, 'guide.html', {'table1':table1, 'table2':table2, 'table3':table3, 'table4': table4, 'table5':table5,
        'current_date':now, 'list_of_hours':list_of_displaytimes,'list_of_endtimes':end_times})



def ondemand(request):
    """provides on demand portion of site

    """
    now = datetime.today()
    channels_filtered=request.GET.getlist('channels')

    type_filtered=request.GET.get('type')

    #switch the value of type filtered to the other so that it can properly exclude the opposite value
    if type_filtered=="Tv":
        type_filtered="Movie"
    elif type_filtered=="Movie":
        type_filtered="Tv"

    if channels_filtered:
        #filters out any channel that was passed in the Get request as checkmarked
        #channels_removed_obj_list = [obj for obj in Titles.objects.all() if any(name in obj.channel for name in channels_filtered)]

        ob_list_channelsremoved = Ondemand_Titles.objects.exclude(reduce(lambda x, y: x | y, [Q(channel__contains=word) for word in channels_filtered]))
    else:
        ob_list_channelsremoved=Ondemand_Titles.objects.all()


    config = RequestConfig(request,paginate={"per_page":40   })
    table1= OndemandTable(ob_list_channelsremoved)
    config.configure(table1)
    return render(request, 'ondemand.html', {'table1':table1,'current_date':now,})




def guide_filtered(request):
    """provides guide content which is filtered by channel, showtype and cookies
    """
    token=request.COOKIES['csrftoken']
    print "Cookies!!!!!!!!!!!!!!!!!!!!!"
    print request.COOKIES
    channels_list=["HBO","MAX","SHO","Starz","Encore"]
    channels_filtered=request.GET.getlist('channels')

    print channels_list
    type_filtered=request.GET.get('type')

    #switch the value of type filtered to the other so that it can properly exclude the opposite value
    if type_filtered=="Tv":
        type_filtered="Movie"
    elif type_filtered=="Movie":
        type_filtered="Tv"
        
    for a in channels_filtered:
        channels_list.pop(channels_list.index(a))

    print 'DATETIME'
    print datetime
    print 'Timesec'
    print 'converted time'
    
    #now = datetime.fromtimestamp(time_sec).today()
    now = datetime.today()
    hour=now.hour
    minutes=now.minute
    if minutes>30:
        startmin=30
        endmin=60-minutes
        timedeltastart=minutes-startmin
    else:
        startmin="00"
        endmin=30-minutes
        timedeltastart=minutes-int(startmin)
    timetostart=("%s:%s"%(hour,startmin))

    hour_list=[timetostart,hour,hour+1]
    start_times=[]
    end_times=[]
    increment=30
    howmanytables=4
    list_of_displaytimes=[]
    for a in xrange(0,howmanytables):
        start_times.append((datetime.now()-timedelta(minutes=timedeltastart+5-increment*a)).time())
        end_times.append((datetime.now()+timedelta(minutes=endmin-1+increment*(a))).time())
        list_of_displaytimes.append((datetime.now()-timedelta(minutes=timedeltastart-increment*a)).time())


    #filters out any channel that was passed in the Get request as checkmarked
    if channels_filtered:        
        ob_list_channelsremoved = Titles.objects.exclude(reduce(lambda x, y: x | y, [Q(channel__contains=word) for word in channels_filtered]))
    else:
        ob_list_channelsremoved=Titles.objects.all()

    if type_filtered:
        ob_list_channelsremoved = ob_list_channelsremoved.exclude(showtype__contains=type_filtered)



    config = RequestConfig(request,paginate={"per_page":25})

    #following code is used to allow for comparison in a 24hour format, without dates.  Does so by checking to see if it is near midnight. 
    time_back=datetime.now()-timedelta(minutes=60+5)
    time_back_minutes=time_back.minute
    time_back_hour=time_back.hour
    difference_in_hours=hour-time_back_hour

    if difference_in_hours<0 and start_times[0].hour==23:
        print "doing code inside differnce of hours and 23"
        filtered_object=ob_list_channelsremoved.filter(time__gte=(datetime.now()-timedelta(minutes=60+5)).time(),csrftoken=token)
        filtered_objects=filtered_object
    elif difference_in_hours<0 and start_times[0].hour!=23:
        print "doing code inside differnce of hours and not 23"
        filtered_object=ob_list_channelsremoved.filter(time__gte=(datetime.now()-timedelta(minutes=60+5)).time(),csrftoken=token)
        filtered_object_one=ob_list_channelsremoved.filter(time__lt=(start_times[0]),csrftoken=token)
        filtered_objects=filtered_object|filtered_object_one
    else:
        print 'doing code in else'
        filtered_objects=''
        filtered_objects=ob_list_channelsremoved.filter(time__gte=(datetime.now()-timedelta(minutes=60+5)),time__lt=(start_times[0]),csrftoken=token)



#used to go through each list and determine if a new day has occurred, if so it runs a query for it else runs a regular query
    tables_list=[]

    for a in xrange(0,len(start_times)):
        start_end_difference=start_times[a].hour-end_times[a].hour
        if start_end_difference>0:
            print "problem with table %s"%a
            filtered_object=ob_list_channelsremoved.filter(time__gte=(start_times[a]),csrftoken=token)
            filtered_object_one=ob_list_channelsremoved.filter(time__lt=(end_times[a]),csrftoken=token)
            adjusting_midnight=filtered_object|filtered_object_one
            tables_list.append(adjusting_midnight)
        else:
            print "no problem with table %s"%a
            adjusting_midnight = ob_list_channelsremoved.filter(time__gte=(start_times[a]), time__lt=(end_times[a]),csrftoken=token)
            tables_list.append(adjusting_midnight)


    table1= TitlesTable(filtered_objects,prefix="1-")
    titles_tables=[]
    for a in xrange(0,len(tables_list)):
        tables=TitlesTable(tables_list[a], prefix='%s-'%a)
        titles_tables.append(tables)


    config.configure(table1)
    config.configure(titles_tables[0])
    config.configure(titles_tables[1])
    config.configure(titles_tables[2])
    config.configure(titles_tables[3])

    return render(request, 'guide.html', {'table1':table1, 'table2':titles_tables[0], 'table3':titles_tables[1], 'table4': titles_tables[2], 'table5':titles_tables[3],
        'current_date':now, 'list_of_hours':list_of_displaytimes,'list_of_endtimes':end_times})


