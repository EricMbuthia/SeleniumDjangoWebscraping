from django.http.response import JsonResponse
import tabula
import pandas as pd
import urllib.request
import PyPDF2
import io
import sys
import  numpy as np

from pathlib import Path
from datetime import datetime
from dateutil import tz
from selenium import webdriver
from selenium.webdriver.firefox import firefox_profile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from django.shortcuts import render
# Create your views here.
from .models import ScrapeRecordsInventory,ScrapeRecords,UndoneNotices
BASE_DIR = Path(__file__).resolve().parent.parent

def clean_time(raw_date, raw_time):
    aquired_time = datetime.strptime(raw_date+" "+raw_time+":00", '%Y-%m-%d %H:%M:%S')
    aquired_time_tz = datetime.astimezone(aquired_time,tz=tz.gettz())
    print("aquired time: "+ str(aquired_time_tz))
    return aquired_time_tz

def get_tax_value(tax_value_link):
    req = urllib.request.Request(tax_value_link, headers={'User-Agent' : "Magic Browser"})
    remote_file = urllib.request.urlopen(req).read()
    remote_file_bytes = io.BytesIO(remote_file)
    pdfdoc_remote = PyPDF2.PdfFileReader(remote_file_bytes)
    req_str = ""
    for i in range(pdfdoc_remote.numPages):
        current_page = pdfdoc_remote.getPage(i)
        
        str_in_qtn = current_page.extractText()
        if i == 0:
            offset = str_in_qtn.find('Amount Due')+11
            offset2 = str_in_qtn.find('Please pay')
            print(str_in_qtn.find('Amount Due'))
            print("========================================For the TAX=================================")
            req_str = str_in_qtn[offset:offset2]
            print(req_str)    
            

    # print("=========================================Tax Value Link============================================")
    # print(tax_value_link)
    return req_str

def get_property_value(property_value_link):
    property_value_dict = {}
    dfs3 = tabula.read_pdf(property_value_link,  pages='3')
    print("Property Value")
    print("==============Property Value Current Year: "+ str(dfs3[0]["Current Year (2020-21)"][0]))
    print("==============Property Next Year: "+ str(dfs3[0]["Next Year (2021-22)"][0]))
    print("========================================Property Value Link========================================")
    print(property_value_link)
    property_value_dict["Current Year (2020-21)"] = dfs3[0]["Current Year (2020-21)"][0]
    property_value_dict["Next Year (2021-22)"] = dfs3[0]["Next Year (2021-22)"][0]

    return property_value_dict
def my_timer(limit):
    
    wait_time = np.random.randint(1,limit) 
    print("Limit time is: "+str(limit)+", Wait time is: "+str(wait_time))
    return wait_time


def nyc_spider(notice_recs, record_id):
    req_values_list = []
    profile = webdriver.FirefoxProfile()

    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.socks", "127.0.0.1")
    profile.set_preference("network.proxy.socks_port", 9150)
    profile.set_preference("network.proxy.socks_version", 5)
    profile.update_preferences()
    # my_url ="https://a836-pts-access.nyc.gov/care/Search/Disclaimer.aspx?FromUrl=../search/commonsearch.aspx?mode=address"
    # service = Service(browser_path)                                            
    my_url ="https://a836-pts-access.nyc.gov/care/Search/Disclaimer.aspx?FromUrl=../search/commonsearch.aspx?mode=persprop"

    options = Options()
    # options.set_preference('profile', profile)

    # driver = webdriver.Firefox(firefox_profile=profile, options=options)

    scrapeRecordsInventoryRef =  ScrapeRecordsInventory.objects.get(id = record_id)
    with webdriver.Firefox(firefox_profile = profile, options= options) as driver:
        driver.get(my_url)
        # Setup wait for later
        wait = WebDriverWait(driver, 70)
        wait.until(EC.element_to_be_clickable((By.ID, 'btAgree')))
        driver.find_element(By.ID, "btAgree").click() 
        
        count = 0
        for index, rec in notice_recs.iterrows():
            print("++++==============================================================")
            try:
                count = count+1
                print("--------------------------------------------------------------------------------------------------")
                print("Rec total number = "+ str(len(notice_recs))+" remaining records = "+ str(len(notice_recs)-count))
                print("Count = "+str(count))
                print("--------------------------------------------------------------------------------------------------")
                wait2 = WebDriverWait(driver, 100)
                wait2.until(EC.element_to_be_clickable((By.XPATH,"//div[@id ='secondarytopmenu']/ul/li[2]/a")))
                driver.find_element(By.XPATH, "//div[@id ='secondarytopmenu']/ul/li[2]/a").click()
            # Store the ID of the original window
            # original_window = driver.current_window_handle

            # Check we don't have other windows open already
            # assert len(driver.window_handles) == 1

            # Click the link which opens in a new window
            # wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'selenium-webdriver')))
            # driver.find_element(By.CLASS_NAME, "selenium-webdriver").click()
            
            
                wait.until(EC.element_to_be_clickable((By.ID, 'btSearch')))
                # driver.find_element(By.ID,"inpStreet").send_keys("All")
                borough_dropdown = Select(driver.find_element(By.ID,"inpParid"))
                borough_dropdown.select_by_index(rec["borough"])
                driver.find_element(By.ID,"inpTag").send_keys(str(rec["block"]))
                driver.find_element(By.ID, "inpStat").send_keys(str(rec["lot"]))
                driver.find_element(By.ID, "btSearch").click()
                wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[@class='navigation']/li[1]")))
                owner_name = driver.find_element(By.XPATH, "//table[@id='Property Owner(s)']/tbody/tr[2]/td").text
                # owner_name = driver.find_element(By.XPATH, "//table[@id='Property sdsdOwner(s)']/tbody/tr[2]/td").text

                wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[@class='navigation']/li[6]")))

            # //table[@id="Property Owner(s)"]/tbody/tr[2]/td
            
                driver.find_element(By.XPATH, "//ul[@class='navigation']/li[6]").click()
                wait.until(EC.element_to_be_clickable((By.XPATH,"//table[@id='Notices of Property Value']/tbody/tr[2]/td[2]/a[@href]")))
                property_value_link = driver.find_element(By.XPATH,"//table[@id='Notices of Property Value']/tbody/tr[2]/td[2]/a").get_attribute('href')

                # //table[@id='Notices of Property Value']/tbody/tr[2]/td[2]/a[@href]
                driver.find_element(By.XPATH, "//ul[@class='navigation']/li[7]").click()
                tax_value_link = driver.find_element(By.XPATH, "//table[@id='Property Tax Bills']/tbody/tr[2]/td[3]/a").get_attribute('href')
                print("Propert Value Link")
                print(property_value_link)
                print("Tax Value Link")
                print(tax_value_link)
                print("Owner Name")
                print(owner_name)    
                tax_value = get_tax_value(tax_value_link)
                property_value = get_property_value(property_value_link)
                print("propert value")
                print(property_value)
                print("Tax Value")
                print(tax_value)
                req_values_list.append(owner_name)
                req_values_list.append(tax_value)
                req_values_list.append(property_value)
                ## First Table
                # scrapeRecordsInventoryRef =  ScrapeRecordsInventory.objects.get(id = record_id)
                ##Get rec from first table and use it to reference this

                if "street_name" in notice_recs.columns:
                    scrapeRecords =    ScrapeRecords(owners_name = owner_name,property_value_current_year=property_value["Current Year (2020-21)"],
                    property_value_next_year = property_value["Next Year (2021-22)"],tax_value = tax_value,
                    billing_address = str(rec["house_number"])+ " "+str(rec["street_name"]) ,link = tax_value_link,
                    borough = rec["borough"] ,block= rec["block"],
                    lot = rec["lot"],record_ref = scrapeRecordsInventoryRef)   
                    scrapeRecords.save()        
                elif "billing_address" in notice_recs.columns:
                    scrapeRecords =    ScrapeRecords(owners_name = owner_name,property_value_current_year=property_value["Current Year (2020-21)"],
                    property_value_next_year = property_value["Next Year (2021-22)"],tax_value = tax_value,
                    billing_address = rec["billing_address"] ,link = tax_value_link,
                    borough = rec["borough"] ,block= rec["block"],
                    lot = rec["lot"],record_ref = scrapeRecordsInventoryRef)   
                    scrapeRecords.save() 
            except:
                    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    print(sys.exc_info())                
                    if "street_name" in notice_recs.columns:
                        try:
                            print("EXCEPT EXCEPT STREET NAME")
                            undoneNotices = UndoneNotices(borough = rec["borough"],block = rec["block"],lot = rec["lot"]
                                            ,exception_type = str(sys.exc_info()[0])[8:-2],billing_address = str(rec["house_number"])+ " "+str(rec["street_name"])
                                            ,scrape_rec = scrapeRecordsInventoryRef, exception_info = str(sys.exc_info())) 
                            undoneNotices.save()   
                        except:
                            print("exc dkdkdkdk")
                            print(sys.exc_info())     
                    elif "billing_address" in notice_recs.columns:
                        try:
                            print("EXCEPT EXCEPT BILLING ADDRESS")
                            
                            undoneNotices =    UndoneNotices(borough = rec["borough"],block = rec["block"],lot = rec["lot"]
                                            ,exception_type = str(sys.exc_info()[0])[8:-2],billing_address = str(rec["billing_address"])
                                            ,scrape_rec = scrapeRecordsInventoryRef, exception_info = str(sys.exc_info())) 
                            undoneNotices.save()
                        except:
                            print("djdjjdjdjdj")
                            print(sys.exc_info())

                    else:
                        print("EXCEPT EXCEPT")
                
            # finally:
            #         if "street_name" in notice_recs.columns:
            #             print("FINALLY FINALLY STREET NAME")
            #             print(rec)
            #             undoneNotices = UndoneNotices(borough = rec["borough"],block = rec["block"],lot = rec["lot"]
            #                             ,exception_type = str(sys.exc_info()[0])[8:-2],billing_address = str(rec["house_number"])+ " "+str(rec["street_name"])
            #                             ,scrape_rec = scrapeRecordsInventoryRef, exception_info = str(sys.exc_info())) 
            #             undoneNotices.save()        
            #         elif "billing_address" in notice_recs.columns:
            #             print("FINALLY FINALLY BILLING ADDRESS")
            #             undoneNotices =    UndoneNotices(borough = rec["borough"],block = rec["block"],lot = rec["lot"]
            #                             ,exception_type = str(sys.exc_info()[0])[8:-2],billing_address = str(rec["billing_address"])
            #                             ,scrape_rec = scrapeRecordsInventoryRef, exception_info = str(sys.exc_info())) 
            #             undoneNotices.save()
            #         else:
            #             print("FINALLY FINALLY")
            #         continue
    # return req_values_list

def home(request):
    # notice_df = pd.read_excel("notice.xlsx", sheet_name="web_file",names = column_values)
    # query_parameters = notice_df[["borough","block","lot","house_number","street_name"]]
    # # nyc_spider(query_parameters.loc[9:10], 1)
    # # for
    # # print(len(query_parameters.loc[7:10]))
    # # print(query_parameters.loc[7:10])
    # notice =  ScrapeRecords.objects.all().values()
    # notice_db_df = pd.DataFrame(notice)
    # print(notice_db_df)
    # notice_db_df.to_excel("notice_ouput.xlsx", sheet_name="notice1")

    # print(notice_df.info())
    try:
        if request.method == "GET":
            scrapeRecordsInventory = ScrapeRecordsInventory.objects.all()
            return render(request, "home.html", {"scrape_inventory_recs":scrapeRecordsInventory})
        
    except:
        print("Exception Found: "+ str(sys.exc_info()))
        return render(request, 'home.html',{'inv_recs_error': "Could not Fetch"})
def inv_rec_detail(request, pk):
    try:

        inventory_notice_rec = ScrapeRecordsInventory.objects.get(id = pk)
        inv_rec = ScrapeRecords.objects.filter(record_ref = pk)
        
        inv_rec_dict = {'id':pk, "time_rec":inventory_notice_rec.time_rec, "rec_date":inventory_notice_rec.rec_date,"incv_rec":inv_rec}
        print(inv_rec_dict)
        return render (request, "inventory_rec.html", {'inv_recs': inv_rec_dict})
    except:
        print(Exception)
        print("Errors", sys.exc_info())
        return render(request, 'inventory_rec.html',{'inv_recs_error': "Could not Fetch"})
def inv_rec_update(request):
    column_values = ["borough", "block", "lot", "tax_class_code", "building_class","community_board","council_board", "house_number","street_name","zip_code","water_db"] 
    try:
        if request.method == "POST":
                input_file_name = request.POST.get("input_file_name", "None")
                origin_input_file_name = BASE_DIR / 'input_folder'/ input_file_name
                notice_id = request.POST.get("notice_id", "None")
                print(notice_id)
                notice_df = pd.read_excel(origin_input_file_name, sheet_name="web_file",names = column_values)
                query_parameters = notice_df[["borough","block","lot","house_number","street_name"]]
                nyc_spider(query_parameters[11:20], notice_id)
                response_data = {'recieved': True, 'status': "ok"}
                return JsonResponse(response_data)
    except:
        print("Inv Rec", sys.exc_info())
        response_data = {"received": False, 'status': "error"}
        return JsonResponse(response_data)

def create_db_notice(request):
    try:
        if request.method == "POST":
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            scrapeRecordsInventory = ScrapeRecordsInventory(rec_date = str(current_time))
            scrapeRecordsInventory.save()
            response_data = {'recieved': True, 'status': "ok"}
            return JsonResponse(response_data)
    except:
        response_data = {"received": False, 'status': "error"}
        return JsonResponse(response_data)
    # if request.method == "GET":
    #     return render(request, "home.html")
    # #Receives destination address and queries API
    # elif request.method =="POST":
    #     #Initialize CLient to get the distances from Google
    #     #Get destination inputs
    #     # raw_date = request.POST.get("date","None") 
    #     # raw_time = request.POST.get("time","None")
    #     # aquired_time_tz = clean_time(raw_date, raw_time)
    #     now = datetime.now()
    #     current_time = now.strftime("%H:%M:%S")
    #     scrapeRecordsInventory = ScrapeRecordsInventory(rec_date = str(current_time))
    #     scrapeRecordsInventory.save()
def write_notices_to_file(request):
    try:
        if request.method == "POST":
            ref_id = request.POST.get("ref_id", "None")
            print("ref_id"+ str(ref_id))
            output_filename = request.POST.get("output_filename", "None")
            notice = ScrapeRecords.objects.filter(record_ref = ref_id).values()
            notice_db_df = pd.DataFrame(notice)
            sub_dir = BASE_DIR / 'output_folder'
            file_name = output_filename+".xlsx"
            notice_db_df.to_excel(sub_dir /file_name, sheet_name="notice")
            response_data = {"received": True, 'status': "ok"}
            return JsonResponse(response_data)
    except:
        response_data = {"received": False, 'status': "error"}
        return JsonResponse(response_data)
def undone_recs_detail(request, ll):
    try:
        if request.method == "GET":
            undoneNotices = UndoneNotices.objects.filter(scrape_rec = ll).values()
            inventory_notice_rec = ScrapeRecordsInventory.objects.get(id = ll)
        undone_rec_dict = {'id':ll, "time_rec":inventory_notice_rec.time_rec, "rec_date":inventory_notice_rec.rec_date,"undone_rec":undoneNotices}
        print(undoneNotices)
        return render(request, "undone_recs.html", {"undone_notices":undone_rec_dict})
        
    except:
        print("Exception Found undone recs detail: "+ str(sys.exc_info()))
        return render(request, 'undone_recs.html',{'undone_notices_errors': "Could not Fetch"})
# def undone_rec(request, pk):
#     try:

#         inventory_notice_rec = UndoneNotices.objects.get(id = pk)
#         inv_rec = UndoneNotices.objects.filter(record_ref = pk)
       
#         inv_rec_dict = {'id':pk, "time_rec":inventory_notice_rec.time_rec, "rec_date":inventory_notice_rec.rec_date,"incv_rec":inv_rec}
#         print(inv_rec_dict)
#         return render (request, "inventory_rec.html", {'inv_recs': inv_rec_dict})
#     except:
#         print(Exception)
#         print("Errors", sys.exc_info())
#         return render(request, 'inventory_rec.html',{'inv_recs_error': "Could not Fetch"})

def handle_undone_notices(request, ref_id):
    try:
        undone_notices = UndoneNotices.objects.filter(scrape_rec= ref_id).values()


        undone_notices_df = pd.DataFrame(undone_notices)
        print("Undone Notices ")
        print(undone_notices_df)
        nyc_spider(undone_notices_df, ref_id)
        for index, rec in undone_notices_df.iterrows():
            record = UndoneNotices.objects.get(id = rec["id"])
            record.delete()

    except:
        print("Exception found: "+ str(sys.exc_info()))  
def inv_rec(request):
    return render (request,"inventory_rec.html")  

        

