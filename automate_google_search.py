from selenium import webdriver
import selenium.common.exceptions as exception
from bs4 import BeautifulSoup
import time
import csv


# firefox web driver for selenium
driver = webdriver.Firefox(executable_path=r"C:\Users\shree\Downloads\geckodriver-v0.23.0-win64\geckodriver.exe")
# urls from google search
links = []
# google search pages
pages = 1
# creating csv/excel workbook
file = open('url_details.csv', 'a')
writer = csv.writer(file)
writer.writerow(['website', 'category'])


def search_by_name():
    company_name = input('Enter company name:')
    company_name = company_name.replace(' ', '+')
    # initial url
    search_url = 'https://www.google.co.in/search?q=' + company_name
    return search_url


def search_by_image_url():
    try:
        image_icon = driver.find_element_by_xpath('//*[@id="qbi"]')
        image_icon.click()
        image_url = driver.find_element_by_xpath('//*[@id="qbui"]')
        url_path = input("Paste image url")
        image_url.send_keys(url_path)
        search_image = driver.find_element_by_xpath('//*[@id="qbbtc"]/input')
        search_image.click()
    except exception.NoSuchElementException:
        print("google image page error(Image URL)")
    return driver.current_url


def search_by_image_path():
    try:
        image_link = driver.find_element_by_xpath('//*[@id="qbi"]')
        image_link.click()
        upload_image = driver.find_element_by_xpath('//*[@id="qbug"]/div/a')
        upload_image.click()
        image_file = driver.find_element_by_name('encoded_image')
        image_path = input("Enter image location on computer:")
        image_file.send_keys(image_path)
        time.sleep(15)
    except exception.NoSuchElementException:
        print("google image page error(System path)")
    return driver.current_url


# scrape google search page
def get_links(search_google):
    search_google = search_google
    global pages
    try:
        driver.get(search_google)
        time.sleep(15)
        while True:
            print("Crawling URLS of page " + str(pages))
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'lxml')
            # The Search Results resides in the div tag with class = rc or h3 tag with class = r
            elements = soup.find_all("div", {"class": "rc"})
            for element in elements:
                # Extract href from the result
                link = element.find("a")['href']
                links.append(link)
            try:
                next_page = driver.find_element_by_xpath('//*[@id="pnnext"]/span[2]')
                next_page.click()
                time.sleep(15)
                pages = pages + 1
                # print(next_page_url)
            except exception.NoSuchElementException:
                print("Last page of google search")
                break
    except exception.WebDriverException:
        print("Error accessing browser")


choice = int(input("Search by:\n 1. Keyword \n 2. Image = "))
print(choice)
if choice == 1:
    google_url = search_by_name()
elif choice == 2:
    # initial url
    google_image_url = 'https://www.images.google.com'
    driver.get(google_image_url)
    choose = int(input(print("1. Paste image URL\n2. Paste system path of image:")))
    if choose == 1:
        google_url = search_by_image_url()
    elif choose == 2:
        google_url = search_by_image_path()
    else:
        print("invalid choice")
else:
    print("invalid choice")
# call function
get_links(google_url)


# categorise URL
def url_details():
    print("----------Categorising URL--------------")
    i = 1
    for url in links:
        try:
            site_review_url = "https://sitereview.bluecoat.com/#/"
            driver.get(site_review_url)
            path = driver.find_element_by_xpath('//*[@id="txtSearch"]')
            path.send_keys(url)
            time.sleep(10)
            get_button = driver.find_element_by_xpath('//*[@id="btnLookupSubmit"]')
            get_button.click()
            time.sleep(20)
            # result_page---><span> class=ng-star-inserted ---> <a>.text
            soup = BeautifulSoup(driver.page_source, 'lxml')
            span = soup.find_all('div', class_='panel-body')
            data = span[1].find_all('a')
            for s in data:
                print(str(++i) + "." + url + "------->" +s.text)
                writer.writerow([url, s.text])
        except exception.InvalidSelectorException:
            print("HTML element not found(URL review page)")
        except exception.ElementClickInterceptedException:
            print("Click disable")


print("Total number of URL collected: " + str(len(links)))
# get url category from sitereview.bluecoat.com
url_details()

# close firefox
driver.quit()

