from Dbs import Dbs
from Notdbs import Notdbs
import datetime
import time

def userlogin(username, password):
    if len(username) == 9:
        if username[0].isalpha():
            if username[0].upper() == 'S' or username[0].upper() == 'T' :
                if  username[8].isalpha():
                    if username[1:8].isdigit():
                        username[0].upper()
                        username[-1].upper()
                        u_file = open('portfolio.txt', 'r')
                        user = ''
                        latestdate = ''
                        latesttime = ''
                        name = ''
                        for user in u_file:
                            list = user.split(',')
                            if username == list[2] and password == list[1]:
                                name = list[0]
                                if latestdate == '' and latesttime == '':
                                    latestdate = list[3]
                                    latesttime = list[4]
                                else:
                                    newdate1 = time.strptime(latestdate, "%d/%m/%Y")
                                    newdate2 = time.strptime(list[3],"%d/%m/%Y")
                                    if newdate1 < newdate2:
                                        latestdate = list[3]
                                        newtime1 = time.strptime(latesttime, "%H:%M")
                                        newtime2 = time.strptime(list[4], "%H:%M")
                                        if newtime1<newtime2:
                                            latesttime = list[4]
                        user=[name, latestdate, latesttime]
                        return user
    else:
        return 'Invalid nric'

def update_lastlogin(userid, username, password):
    j_file = open('portfolio.txt', 'a')
    a_file = open('portfolio.txt', 'r')
    hello = []
    for a in a_file:
        list = a.split(',')
        if userid == list[0]:
            monthly = list[5]
            age = list[6]
            hello.append(monthly)
            hello.append(age)
    currentdatetime = datetime.datetime.now()
    current_date = str(currentdatetime.day) + "/" + str(currentdatetime.month) + "/" + str(currentdatetime.year)
    current_time = str(currentdatetime.hour) + ":" + str(currentdatetime.minute)
    j_file.writelines('\n' + userid + ',' + password + ',' + username + ',' + current_date + ',' + current_time + ',' + hello[0] + ',' + hello[1] + ',')

def applicationdetail(object, username):
    current = object.get_created_date()
    t = datetime.datetime.strptime(current, "%d/%m/%Y")
    future = t + datetime.timedelta(+30)
    j=str(future.day)+'/'+str(future.month)+'/'+str(future.year)
    if isinstance(object, Dbs):
        applicationdata = username + ', ' + object.get_overdrafttype() + ', ' + object.get_acctype() + ', ' + object.get_salarycreditacc() + ', ' + object.get_creditlimit() + ', ' + object.get_created_date() + ', ' + j + ', ' + object.get_file1() + ', ' + object.get_file2() + '\n'
    else:
        applicationdata =  username + ', ' + object.get_overdrafttype() + ', ' + object.get_acctype() + ', ' + object.get_salarycreditacc() + ', ' + object.get_creditlimit() + ', ' + object.get_created_date() + ', ' + j + ', ' + object.get_file1() + ', ' + object.get_file2() + ', ' + object.get_document() + '\n'
    user_file = open('application.txt', 'a')
    user_file.write(applicationdata)

def nextmonth(user):
    now = datetime.datetime.now()
    nowdate = str(now.day) + "/" + str(now.month) + "/" + str(now.year)
    pastdate=''
    f_file=open('application.txt', 'r')
    for o in f_file:
        n=o.split(', ')
        if user==n[1]:
            pastdate = n[5]

    newdate1 = time.strptime(pastdate, "%d/%m/%Y")
    newdate2 = time.strptime(nowdate, "%d/%m/%Y")

    if newdate1 == newdate2:
        future = now + datetime.timedelta(+30)
        j = str(future.day) + '/' + str(future.month) + '/' + str(future.year)
        return j
    else:
        return False


def eligibility(username):
    a_file = open('portfolio.txt', 'r')
    a=''
    for g in a_file:
        list = g.split(',')
        if username == list[0]:
            if 20000< int(list[5])*12 < 30000 and int(list[6]) >= 21:
                a= 'ocbc easicredit and dbs cashline'
            elif int(list[5])*12 >= 30000 and int(list[6]) >= 21:
                a= 'ocbc easicredit, dbs cashline and uob cashplus'
            elif int(list[6])<21:
                a= 'Age not met'
            else:
                a= 'Annual income not met'

    return a

def show_interest(username, acctype):
    g_file = open('application.txt', 'r')
    a_file = open('portfolio.txt', 'r')
    #now = datetime.datetime.now()
    #what = str(now.day) + "/" + str(now.month) + "/" + str(now.year)
    callist = []

    for app in g_file:
        ocbc = {}
        dbs = {}
        uob = {}
        list = app.split(', ')
        if list[0] == username:
            if acctype == 'OCBC Easicredit':
                for i in a_file:
                    list1 = i.split(',')
                    if list1[0] == username:
                        if 20000<int(list1[5])*12<30000:
                            interest_rate = 0.298
                            monthlyrepayment1 = 0.05
                            monthlyrepayment2 = 50
                            latepayment = 80
                            maximum = 2
                        elif 30000<=int(list1[5])*12<120000:
                            interest_rate = 0.1795
                            monthlyrepayment1 = 0.03
                            monthlyrepayment2 = 50
                            latepayment = 0.25
                            maximum = 4
                        else:
                            interest_rate = 0.1795
                            monthlyrepayment1 = 0.03
                            monthlyrepayment2 = 50
                            latepayment = 0.25
                            # with min 85 and max 125
                            maximum = 6
                        creditlimit = maximum * int(list[5])
                        ocbc['interest_rate'] = interest_rate
                        ocbc['monthlyrepayment1'] = monthlyrepayment1
                        ocbc['monthlyrepayment2'] = monthlyrepayment2
                        ocbc['latepayment'] = latepayment
                        ocbc['maximum'] = maximum
                        ocbc['creditlimit'] = creditlimit
                callist.append(ocbc)
            elif acctype == 'DBS Cashline':
                for i in a_file:
                    list1 = i.split(',')
                    if list1[0] == username:
                        if 20000<int(list1[5])*12<30000:
                            interest_rate = 0.298
                            monthlyrepayment1 = 0.025
                            monthlyrepayment2 = 50
                            latepayment = 105
                            latepayment_interest = 0.358
                            maximum = 4
                        elif int(list1[5])*12<20000:
                            interest_rate = 0.198
                            monthlyrepayment1 = 0.025
                            monthlyrepayment2 = 50
                            latepayment = 105
                            latepayment_interest = 0.258
                            maximum = 4
                        else:
                            interest_rate = 0.198
                            monthlyrepayment1 = 0.025
                            monthlyrepayment2 = 50
                            latepayment = 105
                            latepayment_interest = 0.258
                            maximum = 6
                        creditlimit = maximum * int(list[5])
                        dbs['interest_rate'] = interest_rate
                        dbs['monthlyrepayment1'] = monthlyrepayment1
                        dbs['monthlyrepayment2'] = monthlyrepayment2
                        dbs['latepayment'] = latepayment
                        dbs['latepayment_interest'] = latepayment_interest
                        dbs['maximum'] = maximum
                        dbs['creditlimit'] = creditlimit
                callist.append(dbs)
            else:
                interest_rate = 0.198
                monthlyrepayment1 = 0.025
                monthlyrepayment2 = 30
                latepayment = 90
                latepayment_interest = 0.258
                maximum = 6
                creditlimit = maximum * int(list[5])
                #or 200000 for investments, holiday, renovation, education or dream wedding
                uob['interest_rate'] = interest_rate
                uob['monthlyrepayment1'] = monthlyrepayment1
                uob['monthlyrepayment2'] = monthlyrepayment2
                uob['latepayment'] = latepayment
                uob['latepayment_interest'] = latepayment_interest
                dbs['maximum'] = maximum
                dbs['creditlimit'] = creditlimit
                callist.append(uob)
    return callist
print(show_interest('Lin MengFang', 'OCBC Easicredit')[0])
def maximum_creditlimit(maximum, user):
    d_file=open('portfolio.txt', 'r')
