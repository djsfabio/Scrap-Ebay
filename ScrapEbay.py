import urllib
import os
from selenium import webdriver
import time
from termcolor import colored
import pyfiglet
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options

ascii_banner = pyfiglet.figlet_format("Scrapping Ebay!", font="slant")
print(colored(ascii_banner, "cyan"))

options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(
    ChromeDriverManager().install(), chrome_options=options)

rechercheEbay = str(input("Que souhaitez-vous rechercher ? \n"))
driver.get('https://www.ebay.fr/')
driver.find_element_by_xpath(
    '/html/body/header/table/tbody/tr/td[3]/form/table/tbody/tr/td[1]/div[1]/div/input[1]').send_keys(rechercheEbay)
time.sleep(0.5)
driver.find_element_by_xpath(
    '/html/body/header/table/tbody/tr/td[3]/form/table/tbody/tr/td[3]/input').click()
time.sleep(2)
try:
    driver.find_element_by_id('gdpr-banner-accept').click()
except Exception:
    print('Pas de bannière de cookie')

resultats = driver.find_element_by_id('srp-river-results')
listDesResultats = resultats.find_elements_by_tag_name('li')

nomDossier = str(input(
    "Comment souhaitez-vous nommer votre dossier pour stocker les ressources : \n"))
# Création d'un dossier avec le même nom que la recherche
try:
    os.makedirs(nomDossier)
    print("Directory ", nomDossier,  " Created ")
except FileExistsError:
    print("Directory ", nomDossier,  " already exists")

incrementation = 0
myfile = open("./" + nomDossier + "/" +
              str(input("Comment voulez vous nommer votre fichier ? ")) + ".txt", 'w')
for i in listDesResultats:
    try:
        img = i.find_element_by_tag_name('img')
        src = img.get_attribute('src')
        print(img.get_attribute('src'))
        urllib.request.urlretrieve(str(
            src), "./" + nomDossier + "/Fichier_image_" + rechercheEbay + str(incrementation) + ".png")
        myfile.writelines("Image associée : Fichier_image_" +
                          rechercheEbay + str(incrementation) + ".png\n")
        myfile.writelines(i.text)
        myfile.writelines("\n\n\n")
        print(i.text)
        print("\n\n\n")
        incrementation += 1
    except Exception:
        continue

myfile.close()
