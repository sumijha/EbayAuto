import os, sys, inspect
import codecs
import time
from selenium import webdriver
from log import logger
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Common():

    def __init__(self, driver=None):

        self.logger = logger()
        self.driver = driver
        wait = None

    # @property
    def launch(self):
        

        try:
            print("--------------------------")
            # self.report.report()
            print("launch")
            # DesiredCapabilities
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--ignore-ssl-errors')
            options.add_argument('--start-maximized')
            #options.add_argument("--user-data-dir=C:\\Users\\sujha\\AppData\\Local\Google\\Chrome\\User Data\\Default")
            chromedriver = os.getcwd() + "/driver/chromedriver"
            os.environ["webdriver.chrome.driver"] = chromedriver
            print("driver initiated")
            self.driver = webdriver.Chrome(options=options, executable_path=chromedriver)


            # launch Application
            # self.logger.info('************Launch website**************')
           

            return self.driver

        except Exception as e:
            print(e)
            # self.logger.error(e)
            return False

    def login(self):
        try:
            self.waitforElement("")
            self.setValue("", "")
            self.click("")
            self.logger.info("*******LOGIN Successfull***********")
            return True
        except Exception as e:
            self.logger.error(e)
            return False

    def waitforElement(self, slocator):
        try:
            # Declaration of WebDriverWait
            self.wait = WebDriverWait(self.driver, 20)

            # findByXpath:
            self.logger.info("waiting for element " + slocator)
            self.wait.until(EC.visibility_of_element_located(By.XPATH, slocator))

        except Exception as e:
            print(e)
            self.logger.error(e)

    def click(self, loc):

        try:
            self.waitforElement(loc)
            self.getElement(loc).click()

        except Exception as e:
            self.logger.error(e)

    def setValue(self, loc, value):
        try:
            self.getElement(loc).clear()
            self.getElement(loc).send_keys(value)

        except Exception as e:
            self.logger.error(e)

    def getElement(self, slocator):

        element = None
        try:
            # findByXpath
            element = self.driver.find_element(By.XPATH, slocator)

            return element

        except Exception as e:
            self.logger.error(e)
            print(e)
            return element

    # Select CheckBox
    def selectChkBox(self,locator):

        element = None
        try:
            if not (self.getElement(locator).is_selected()):
                self.click(locator)
            else:
                self.click(locator)
        except Exception as e:
            print(e)


    def getElements(self, slocator):

        #	elements=None
        try:
            # findByXpath
            elements = self.driver.find_elements(By.XPATH, slocator)

            return elements

        except Exception as e:
            print(e)
            self.logger.error(e)
            return element

    def closeBrowser(self):
        try:
            self.driver.close()
        except Exception as e:
            print(e)

    # Searching Item in Ebay
    def ebayItemSrch(self,url):
        
        ebayURL = "https://www.ebay.de/myb/Summary"
        inpUsername="//input[@id='userid']"
        inpPwd="//input[@id='pass']"
        btnLogin = "//button[@id='sgnBt']"

        userNameEBay = "troedelbucht32"
        passwordEBay="9R7PKDRj"
        itemSrch = "//input[@class='find-product']"
        itemVal = "Grundkochbuch von Dr.Oetker"
        btnItemSrch = "//button[contains(@id,'find-product')]"



        try:
            self.driver.get("https://www.iaai.com/Vehicle?itemID=30897142&amp;RowNumber=0")
            completeName = os.path.join("C:\\Users\\sujha\\Documents\\HtaEdit","page.html")
            file_object = codecs.open(completeName, "w", "utf-8")
            html = self.driver.page_source
            file_object.write(html)
            self.driver.get(ebayURL)
            self.setValue(inpUsername,userNameEBay)
            self.setValue(inpPwd,passwordEBay)
            self.click(btnLogin)
            time.sleep(4)
            self.driver.get(url)

            time.sleep(2)

            self.driver.switch_to.frame("findprod_iframe")
            self.setValue(itemSrch,itemVal)
            self.click(btnItemSrch)
            time.sleep(4)
            self.driver.switch_to.default_content()
        except Exception as e:
            print(e)

    # Adding Product to the list
    def addEbayProd(self):
        addtoLst="(//div[@class='actions']/button[@class='btn btn--primary'])[1]"
        addDieses="(//div[@class='dialog__footer']/button[@class='btn btn--primary'])[1]"
        inpChkBarz="//input[@id='pmCashOnPickup']"
        inpChkSiehe="//input[@id='pmSeeDesc']"
        inpChkAbholung="//input[@id='localPickup']"
        expndAndern = "//a[@id='anLocId']"
        inpPostal = "//input[@id='itemPostalCode']"
        inpFileUpload = "//a[contains(@style,'block')]//input[@class='upl-fileInp']"
        lnk_Alleanhemen="//a[text()='Alle annehmen']"

        postalCode = "12345"
        imgKeyword = "TestImage"
        inpTxtBox = "TestBodyText"

        try:
            self.driver.switch_to.frame("findprod_iframe")
            self.click(addtoLst)
            time.sleep(4)
            self.click(addDieses)
            time.sleep(6)
            self.selectChkBox(inpChkBarz)
            self.selectChkBox(inpChkSiehe)
            self.selectChkBox(inpChkAbholung)
            time.sleep(1)
            self.click(expndAndern)
            if(self.getElement(inpPostal).get_attribute("value") == ""):
                self.setValue(inpPostal,postalCode)
            time.sleep(4)
            imgList = self.getImages(imgKeyword)
            self.driver.switch_to.default_content()
            self.setHTMLBody("TestHTML")
            time.sleep(2)
            self.driver.switch_to.frame("uploader_iframe")
            time.sleep(2)
           # self.setValue(inpFileUpload,"C:\\Users\\sujha\\PycharmProjects\\eBayAuto\\src\\images\\TestImage1.png")
            for images in imgList:
                self.setValue(inpFileUpload,images)
                time.sleep(6)
            self.driver.switch_to.default_content()
        except Exception as e:
            print(e)

    # Get Images with Keyword
    def getImages(self,keyword):
        filepath=[]
        try:
            imgLst = os.listdir(os.getcwd() +"\images")
            for img in imgLst:
                print(img)
                print(keyword)
                print(img.find(keyword))
                if(img.startswith(keyword)):
                    filepath.append(os.getcwd()+"\\images\\"+img)

        except Exception as e:
            print(e)

        return filepath

    # Setting HTML Text Body
    def setHTMLBody(self,value):
        lnk_HTMLBox = "//div[@id='descDiv']//a[@title='HTML']"

        try:
            self.driver.switch_to.frame("v4-26txtEdit_st")
            self.click(lnk_HTMLBox)
            time.sleep(1)
            self.driver.execute_script("document.body.innerHTML = '" + value + "'")
            self.driver.switch_to.default_content()
        except Exception as e:
            print(e)

    def gmx(self,url):
    
        condition="absence enabled"
        textForCondition="TEXT TO BE ENTERED"
        userName="christian.ganslmayer78@gmx.de"
        password="a1KSDFu7"
        loc_username = "//*[@id='freemailLoginUsername']"
        loc_password="//*[@id='freemailLoginPassword']"
        loc_loginBtn="//*[@id='freemailLoginPassword']/ancestor::fieldset//input[@value='Login']"

        loc_einstellungen=  "//a[@title='Einstellungen']"
        loc_ZudenEinstellungen = "//*[text()='Zu den Einstellungen']"
        loc_Abwesenheitsnotiz="//*[text()='Abwesenheitsnotiz']"
        loc_textarea="//*[@name='textAreaFieldSet:textAreaFormItem:textAreaFormItem_body:textArea:textarea']"
        loc_radio_ausgeschaltet="//*[text()='ausgeschaltet']/preceding-sibling::input"
        loc_radio_immer_eingeschaltet="//*[text()='immer eingeschaltet']/preceding-sibling::input"
        loc_save="//*[@name='buttonContainer:container:buttonContainer_body:submitButton']"


        self.driver.get(url)
        try:
            #self.driver.switch_to.frame("findprod_iframe")
            self.waitforElement(loc_username)
            element = self.getElement(loc_username)
            self.driver.execute_script("return arguments[0].scrollIntoView();", element)
            self.setValue(loc_username,userName)
            self.setValue(loc_password, password)
            self.click(loc_loginBtn)

            time.sleep(8)
            self.driver.switch_to.frame("thirdPartyFrame_home")
            self.click(loc_einstellungen)
            self.click(loc_ZudenEinstellungen)
            time.sleep(3)

            self.driver.switch_to.default_content()
            self.driver.switch_to.frame("thirdPartyFrame_mail")
            self.click(loc_Abwesenheitsnotiz)
            time.sleep(4)
            if(condition.lower()=="absence enabled"):
                self.click(loc_radio_immer_eingeschaltet)
                self.setValue(loc_textarea,textForCondition)
            elif(condition.lower()=="absence disabled"):
                self.click(loc_radio_ausgeschaltet)
            self.click(loc_save)

            time.sleep(4)

        except Exception as e:
            print(e)


