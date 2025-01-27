from django.shortcuts import redirect, render, HttpResponse
import requests
import json
import requests
from bs4 import BeautifulSoup
from requests.api import request
from django.http import HttpResponseRedirect
from geopy.geocoders import Nominatim
from time import sleep
import joblib
import pandas as pd
from .task import *
import warnings
warnings.filterwarnings("ignore")
import numpy as np
# import cv2
# import tensorflow as tf
from django.http import HttpResponse
from django.views.generic import View
from django.conf import settings

#importing get_template from loader
from django.template.loader import get_template
 
#import render_to_pdf from util.py 
 
# from apscheduler.schedulers.background import BackgroundScheduler

print("============================================================= Lets Start Project =============================================================")
# Create your views here.

loaded_model = joblib.load('models/model1.sav')

# def saveme(cough,fever,sore_throat,shortness_of_breath,head_ache,age_60_and_above,gender,abroad,contact_with_covid_patient,prob,prediction,email, country):
#     try:
#         tempo=(cough,fever,sore_throat,shortness_of_breath,head_ache,age_60_and_above,gender,abroad,contact_with_covid_patient,prob,prediction,email, country)
#         query1='''Insert into phase1 values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
#         cursor.execute(query1,tempo)
#         print("Data has been Saved Successfully...!!")
#     except mysql.connector.Error as e:
#         print(e)
#     mydb.commit()
        # return redirect()

def get_prediction(data, loaded_model=loaded_model):
    data_model = {
        'cough': data['Cough'],
        'fever': data['Fever'],
        'sore_throat': data['Sore_Throat'],
        'shortness_of_breath': data['Shortness_of_Breath'],
        'head_ache': data['Headache'],
        'age_60_and_above': data['age'],
        'gender': data['Gender'],
        'abroad': data['Abroad'],
        'contact_with_covid_patient': data['contact_Patient']
    }
    df = pd.DataFrame(data_model, index=[0])
    print(df)
    prediction = loaded_model.predict(df.values)
    pred_prob = loaded_model.predict_proba(df.values)
    print(prediction, pred_prob)
    for x in data_model.keys():
        if(x == 'gender'):
            if(data_model['gender'] == '1'):
                data_model[x] = "Male"
            else:
                data_model[x] = "Female"
        else:
            if(data_model[x] == '1'):
                data_model[x] = "Yes"
            else:
                data_model[x] = "No"
    data_model['prob'] = str(int(pred_prob[0][1]*100))+" %"
    data_model['prediction'] = str(prediction[0])
    data_model['email'] = data['email']
    data_model['country'] = data['country']
    if(data_model['country'] == ''):
        data_model['country'] = "Not Given"
    data_model['one'] = ['Yes', '1']
    send_mail_task.delay(data_model)
    # ctx = {
    #     'data': data,
    # }
    # messageContent = get_template('email.html').render(ctx)
    # file = open("templates/report_one.html","w")
    # file.write(str(messageContent))
    # file.close()
    # print(str(messageContent))
    # print(data_model)
    # saveme(data_model['cough'], data_model['fever'], data_model['sore_throat'], data_model['shortness_of_breath'], data_model['head_ache'], data_model['age_60_and_above'], data_model['gender'], data_model['abroad'], data_model['contact_with_covid_patient'], data_model['prob'], data_model['prediction'], data_model['email'], data_model['country'])
    saveme.delay(data_model['cough'], data_model['fever'], data_model['sore_throat'], data_model['shortness_of_breath'], data_model['head_ache'], data_model['age_60_and_above'], data_model['gender'], data_model['abroad'], data_model['contact_with_covid_patient'], data_model['prob'], data_model['prediction'], data_model['email'], data_model['country'])
    return data_model

def welcome(request):
    return render(request, 'welcome.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def update_it():
    URL = "https://www.worldometers.info/coronavirus/"
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html5lib')
    nums = soup.find_all('div', attrs={'class': 'maincounter-number'})
    wdata = []
    for tag in nums:
        wdata.append(tag.text.strip())
    d = {
        'cases': wdata[0],
        'deaths': wdata[1],
        'recovered': wdata[2]
    }
    f = open("static/tmp/data.json", "w")
    f = json.dump(d, f)
    return None

def update(request):
    from datetime import datetime
    import time
    t1=datetime.now()
    update_it()
    t2=datetime.now()
    diff=(t2-t1).total_seconds()
    if(diff<7):
        time.sleep(7-diff)
    return redirect('home')


def home(request):
    # global wdata
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formFour':
            model_data = request.POST
            context = {
                'model_pred': get_prediction(model_data)
            }
            return render(request, 'results.html', context)
    else:
        # global update_date
        world_data.delay(0)
        f = open("static/tmp/data.json", "r")
        d = json.load(f)
        # d["update_dt"]=update_date[0]
        # d["update_mn"]=update_date[1]
        # d["update_yr"]=update_date[2]
        return render(request, 'index.html', d)
        # return render(request, 'index.html')


def contact(request):
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formFour':
            model_data = request.POST
            context = {
                'model_pred': get_prediction(model_data)
            }
            return render(request, 'results.html', context)
    return render(request, 'contact.html')


def vaccine(request):
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formFour':
            model_data = request.POST
            context = {
                'model_pred': get_prediction(model_data)
            }
            return render(request, 'results.html', context)
        elif request.POST.get("form_type") == 'formFive':
            pincode = request.POST['pincode']
            date = request.POST['date']
            context = vaccine_tracker(pincode, date)
            return render(request, 'vaccine.html', context)
    else:
        return render(request, 'vaccine.html')


def vaccine_tracker(pincode, date):
    try:
        date = str(date)
        temp = list(date.split('-'))
        temp.reverse()
        date = "-".join(temp)
        params = {'pincode': pincode, 'date': date}
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        }
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin"
        # URL="https://cdn-api.co-vin.in/api/v2/appointment/centers/public/findByLatLong"
        # params={'lat':28.72,'long':77.14}
        response = requests.get(url=URL, params=params,headers=headers)  # headers=headers
        data = response.json()
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(pincode)
        # print(location.address)
        display_data = []
        l = data['sessions'][0].keys()
        data = data['sessions']
        for i in range(len(data)):
            d = dict()
            d['Date'] = str(data[i]['date'])
            d['Vaccine'] = str(data[i]['vaccine'])
            d['Cost'] = "INR / Rs." + \
                str(data[i]['fee'])+" "+str(data[i]['fee_type'])
            d['Age'] = str(data[i]['min_age_limit'])+"+"
            d['Center Name'] = str(data[i]['name'])
            # d['Address'] = str(data[i]['name'])+" "+str(data[i]['address'])+" "+str(data[i]['block_name']) + \
            #     " "+str(data[i]['district_name'])+" "+str(data[i]
            #                                               ['state_name'])+" "+str(data[i]['pincode'])
            d['Available Dose 1 Quantity'] = str(
                data[i]['available_capacity_dose1'])
            d['Available Dose 2 Quantity'] = str(
                data[i]['available_capacity_dose2'])
            sub_data=[]
            for hell in list(data[i]['slots']):
                t=[]
                t.append(hell['time'])
                t.append(hell['seats'])
                sub_data.append(t)
            d['Slots'] = [['Time','Seats'],sub_data]
            display_data.append(d)
        l = list(display_data[0].keys())
        context = {
            'data': display_data,
            'lc': location.address,
            'l': l,
            'slot': 'Slots',
        }
    except:
        print("Invalid Operation...!!!")
        context = {'error': 'No Data Available'}
    return context

def img_process(img,email):
    model_1 = tf.keras.models.load_model('models/cnn_model.h5')
    z_img = cv2.imread(img)
    z_img = cv2.resize(z_img, (70, 70)) / 255.0
    z_img = z_img.reshape(1, z_img.shape[0], z_img.shape[1], z_img.shape[2])
        
    z = model_1.predict(z_img)
    z = np.argmax(z, axis = 1)
    data={'email':email,'output':str(z[0]),'img':img}
    send_img_mail_task.delay(data)
    return z

def img_process2(img,email):
    model_1 = tf.keras.models.load_model('models/CNN_1.h5')
    z_img = cv2.imread(img)
    z_img = cv2.resize(z_img, (70, 70)) / 255.0
    z_img = z_img.reshape(1, z_img.shape[0], z_img.shape[1], z_img.shape[2])
        
    z = model_1.predict(z_img)
    z = np.argmax(z, axis = 1)
    if(z[0]==1):
        res="Positive"
    else:
        res="Negative"
    savemyimg2.delay(email,img,res)
    return z

from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
def predictors(request):
    flag_it=0
    zero=0
    one=1
    two=2
    three=3
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formFour':
            flag_it=1
            model_data = request.POST
            context = {
                'data': get_prediction(model_data),
                'zero':one,
                'one':one,
                'flag_it':flag_it,
            }
            return render(request, 'predictors.html', context)
        if request.POST.get("form_type") == 'formSeven' and request.FILES['image']:
            whatsup = request.POST.get('whatisit')
            filename = request.FILES['image']
            filename=str(filename)
            file_data=request.FILES['image'].read()
            temp=filename.index(".")
            img="static/tmp/image"+str(filename[temp:])
            print(img)
            with open("static/tmp/image"+str(filename[temp:]), "wb") as outfile:
                outfile.write(file_data)
            if whatsup:
                flag_it=3
                imgpred=img_process2(img,request.POST['img_email'])
                file_n="static/tmp/image"+str(filename[temp:])
                tk=[1]
                print("Its CT Scan...!!!!")
                return render(request, 'predictors.html',{'imgpred':imgpred[0],'img_result':file_n,'tk':tk,'zero':one,
                    'flag_it':flag_it,'three':three})
            else:
                flag_it=2
                imgpred=img_process(img,request.POST['img_email'])
                file_n="static/tmp/image"+str(filename[temp:])
                tk=[1]
                print("Its X-Ray...!!!")
                return render(request, 'predictors.html',{'imgpred':imgpred[0],'img_result':file_n,'tk':tk,'zero':one,
                    'flag_it':flag_it,'two':two})
    return render(request, 'predictors.html',{'flag_it':flag_it,'zero':zero})
