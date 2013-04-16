def entered(request):

    if 'q' in request.GET:
        zipcode=request.GET['q']
        #message = 'You searched for: %r' % request.GET['q']
        providers=tvguide_helperfunctions.return_providers(zipcode)

    elif 'mydropdown' in request.GET:
        #providers=providers[request.GET['mydropdown']]
        providers=request.GET['mydropdown']

        zip_headend=request.GET['mydropdown'].split(" ")
        zipcode=zip_headend[0]
        headend=zip_headend[1]
       # message=providers["Verizon Fios Philadelphia (Philadelphia)"]
        workingwith_newdb.main(zipcode,headend)
        return(messingwithdb1_filtered(request,zipcode,headend))

    else:
        message = 'You submitted an empty form.'


    channel_filter=request.GET
    now = datetime.datetime.now()
    return render(request,'entered.html', {'providers':providers,'zipcode':zipcode, 'current_date':now,'channel_filter':channel_filter})


def messingwithdb1_filtered(request):
    channels_filtered=request.GET.getlist('channels')
    token=request.COOKIES['csrftoken']
    now = datetime.today()
    hour=now.hour
    minutes=now.minute
    print now
    if minutes>30:
        startmin=30
        endmin=60-minutes
        timedeltastart=minutes-startmin
    else:
        startmin="00"
        endmin=30-minutes
        timedeltastart=minutes-int(startmin)
    timetostart=("%s:%s"%(hour,startmin))
    print timetostart
    #now=datetime.strptime(now, '%I:%M%p')
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

    print start_times
    print end_times
    print list_of_displaytimes
  #  currently_on_titles=Titls.objects.filter(time__gt=(datetime.now().time()))
    config = RequestConfig(request,paginate={"per_page":25})

    #code in order to make a 24 hour time frame work with greater and less then
    time_back=datetime.now()-timedelta(minutes=60+5)
    time_back_minutes=time_back.minute
    time_back_hour=time_back.hour
    difference_in_hours=hour-time_back_hour
    print ('hour %s')%hour
    print ('time_back %s')%time_back
    print ('differnce in hours %s')%difference_in_hours
    print start_times[2]
    print end_times[2]

    if difference_in_hours<0 and start_times[0].hour==23:
        print "doing code inside differnce of hours and 23"
        filtered_object=Titles.objects.filter(time__gte=(datetime.now()-timedelta(minutes=60+5)).time(),csrftoken=token)
        filtered_objects=filtered_object
    elif difference_in_hours<0 and start_times[0].hour!=23:
        print "doing code inside differnce of hours and not 23"
        filtered_object=Titles.objects.filter(time__gte=(datetime.now()-timedelta(minutes=60+5)).time(),csrftoken=token)
        filtered_object_one=Titles.objects.filter(time__lt=(start_times[0]),csrftoken=token)
        filtered_objects=filtered_object|filtered_object_one
    else:
        print 'doing code in else'
        filtered_objects=''
        filtered_objects=Titles.objects.filter(time__gte=(datetime.now()-timedelta(minutes=60+5)),time__lt=(start_times[0]))


 
    if channels_filtered:

        #filters out any channel that was passed in the Get request as checkmarked
        #channels_removed_obj_list = [obj for obj in Titles.objects.all() if any(name in obj.channel for name in channels_filtered)]

        ob_list_channelsremoved = Titles.objects.exclude(reduce(lambda x, y: x | y, [Q(channel__contains=word) for word in channels_filtered]))



        table1= TitlesTable(ob_list_channelsremoved.filter(time__lt=(start_times[0]), time__gte=(datetime.now()-timedelta(minutes=120+5)).time(),csrftoken=token), prefix="1-")
        #table2 = TitlesTable(Titles.objects.filter(time__gte=(start_times[0]), time__lt=(end_times[0]),zipcode=zipc,headend=head).exclude(channel__contains='tbs'), prefix="2-")
        table2 = TitlesTable(ob_list_channelsremoved.filter(time__gte=(start_times[0]), time__lt=(end_times[0]),csrftoken=token), prefix="2-")
        table3= TitlesTable(ob_list_channelsremoved.filter(time__gte=(start_times[1]), time__lt=(end_times[1]),csrftoken=token), prefix="3-")
        table4 = TitlesTable(ob_list_channelsremoved.filter(time__gte=(start_times[2]), time__lt=(end_times[2]),csrftoken=token), prefix="4-")
        table5 = TitlesTable(ob_list_channelsremoved.filter(time__gte=(start_times[3]), time__lt=(end_times[3]),csrftoken=token), prefix="5-")
    else:
        table1= TitlesTable(filtered_objects,prefix="1-")
        #table2 = TitlesTable(Titles.objects.filter(time__gte=(start_times[0]), time__lt=(end_times[0]),zipcode=zipc,headend=head).exclude(channel__contains='tbs'), prefix="2-")
        table2 = TitlesTable(Titles.objects.filter(time__gte=(start_times[0]), time__lt=(end_times[0]),csrftoken=token), prefix="2-")
        table3= TitlesTable(Titles.objects.filter(time__gte=(start_times[1]), time__lt=(end_times[1]),csrftoken=token), prefix="3-")
        table4 = TitlesTable(Titles.objects.filter(time__gte=(start_times[2]), time__lt=(end_times[2]),csrftoken=token), prefix="4-")
        table5 = TitlesTable(Titles.objects.filter(time__gte=(start_times[3]), time__lt=(end_times[3]),csrftoken=token), prefix="5-")

    config.configure(table1)
    config.configure(table2)
    config.configure(table3)
    config.configure(table4)
    config.configure(table5)
    #table.columns['first_name'].header="shit"

    return render(request, 'dbinteraction_djangotables2.html', {'table1':table1, 'table2':table2, 'table3':table3, 'table4': table4, 'table5':table5,
        'current_date':now, 'list_of_hours':list_of_displaytimes,'list_of_endtimes':end_times})

