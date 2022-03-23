from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from win10toast import ToastNotifier
from datetime import datetime
from platform import system
import time
from webdriver_manager.chrome import ChromeDriverManager
import os


driver = webdriver.Chrome(ChromeDriverManager().install())
string0 = "İstanbul(Söğütlü Ç.)"#kalkiş istasyonu
string1 = "ERYAMAN YHT"#variş istasyonu
date = "23.03.2022" #Gidis tarihi eger bugunse None, degilse '22.11.2019' formatinda yaz
#fullness = '2' #Kapasite bu sayidan farkli olursa bana bildirim at
hour = "19:15" #Sefer saati format '14:35'
gender=1  #erkek 1 kadin 2
# index = 5 #Sefer listesinde trenin gozuktugu sira
def notify_windows(title, text):
    toast = ToastNotifier()
    toast.show_toast(title,text,duration=20)
def sayfaKontrol(selfie,timer):
        
            elem = WebDriverWait(selfie, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='mainTabView:gidisSeferTablosu:1:j_idt109:0:somVagonTipiGidis1_label']")))
            if elem != "":
                for row in range(1, 15):
                    try:
                        if timer == selfie.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div/div/form/div[1]/div/div[1]/div/div/div/div[1]/div/div/div/table/tbody/tr[{0}]/td[1]/span'.format(row)).text:
                            now = datetime.now()
                            print("Time: " + now.strftime("%m/%d/%Y, %H:%M:%S"))
                            message=selfie.find_element_by_xpath('//*[@id="mainTabView:gidisSeferTablosu:{0}:j_idt109:0:somVagonTipiGidis1_label"]'.format(row - 1)).text
                            if message[22] != '0' and message[22]!='1' and message[22]!='2':
                                
                                print(message)
                                btnText='/html/body/div[3]/div[2]/div/div/div/div/form/div[1]/div/div[1]/div/div/div/div[1]/div/div/div/table/tbody/tr[{0}]/td[7]/div'.format(row)
                                print(btnText)
                                secBtn=driver.find_element_by_xpath(btnText)
                                # secBtn= wait.until(EC.presence_of_element_located((By.XPATH, btnText)))
                                secBtn.click()
                                time.sleep(2)
                                devamBtnTxt='/html/body/div[3]/div[2]/div/div/div/div/form/div[1]/div/div[1]/div/div/div/table[2]/tbody/tr/td[2]/button/span'
                                devamBtn=driver.find_element_by_xpath(devamBtnTxt)
                                devamBtn.click()
                                notify_windows("bilet bulundu koş", message)
                                return False
                            elif message[23]!=')':
                                print(message)
                                btnText='/html/body/div[3]/div[2]/div/div/div/div/form/div[1]/div/div[1]/div/div/div/div[1]/div/div/div/table/tbody/tr[{0}]/td[7]/div'.format(row)
                                print(btnText)
                                secBtn=driver.find_element_by_xpath(btnText)
                                # secBtn= wait.until(EC.presence_of_element_located((By.XPATH, btnText)))
                                secBtn.click()
                                time.sleep(2)
                                devamBtnTxt='/html/body/div[3]/div[2]/div/div/div/div/form/div[1]/div/div[1]/div/div/div/table[2]/tbody/tr/td[2]/button/span'
                                devamBtn=driver.find_element_by_xpath(devamBtnTxt)
                                devamBtn.click()
                                time.sleep(2)
                                inputs=driver.find_elements_by_css_selector("input[type='checkbox']")
                                if(len(inputs)>2):
                                    inputs[3].click()
                                    time.sleep(3)
                                    cinsiyetForm= driver.find_element_by_id("cinsiyet_secimi_form")
                                    divs=cinsiyetForm.find_elements_by_tag_name('div')
                                    divs[gender].click()
                                elif(len(inputs)<3):
                                    inputs[0].click()
                                    time.sleep(3)
                                    cinsiyetForm= driver.find_element_by_id("cinsiyet_secimi_form")
                                    divs=cinsiyetForm.find_elements_by_tag_name('div')
                                    divs[gender].click()
                                    notify_windows("bilet bulundu ama engelli bölümü olabilir.", message)

                                notify_windows("bilet bulundu koş", message)
                                return False
                            else:
                                print(message)
                                
                                print("Aradiğiniz seferde boş yer yok...")
                                return True
                    except Exception as inst:
                        print(inst)  
                        print ("Saatinizde hata var...")
                        return True

                      
                    

            else:
                print("Aradiğiniz seferde boş yer yoktur...")
                return True
                
     
def notify_mac(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}" sound name "default"'
              """.format(text, title))



i = 0
RES=True
while RES:
    try:
        driver.get("https://ebilet.tcddtasimacilik.gov.tr/view/eybis/tnmGenel/tcddWebContent.jsf")
        os_type = system()
        wait = WebDriverWait(driver, 10)

        from_x = '//*[@id="nereden"]'
        from_box = wait.until(EC.presence_of_element_located((By.XPATH, from_x)))
        from_box.clear()
        from_box.send_keys(string0)

        to_x = '//*[@id="nereye"]'
        to_box = wait.until(EC.presence_of_element_located((By.XPATH, to_x)))
        to_box.clear()
        to_box.send_keys(string1)

        if date:
            date_x = '//*[@id="trCalGid_input"]'
            date_box = wait.until(EC.presence_of_element_located((By.XPATH, date_x)))
            date_box.clear()
            date_box.send_keys(date)

            date_close_x = '//*[@id="ui-datepicker-div"]/div[2]/button[2]'
            date_close_button = wait.until(EC.presence_of_element_located((By.XPATH, date_close_x)))
            date_close_button.click()

            time.sleep(1)
        search = '//*[@id="btnSeferSorgula"]'
        search_box = wait.until(EC.presence_of_element_located((By.XPATH, search)))
        search_box.click()

        time.sleep(5)
        RES=sayfaKontrol(driver,hour)
        
        i += 1
    except Exception as exc:
        print(exc)
        continue
