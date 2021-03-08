from selenium.webdriver import ChromeOptions, Chrome
import time
import pandas as pd
import json
import requests

email = input("Linkedin Mail adresiniz: ")
parola = input("Linkedin Şifreniz: ")
keyword = input("Aramak istediğiniz iş ilanı: ")
location = input("Aramak istediğiniz lokasyon: ")

driver = Chrome("C:\\chromedriver\\chromedriver.exe")

driver.get("https://www.linkedin.com/jobs")

log_in = driver.find_element_by_class_name("nav__button-secondary")
log_in.click()

time.sleep(1)
username = driver.find_element_by_id("username")
username.clear()
time.sleep(1)
username.send_keys(email)

password = driver.find_element_by_id("password")
password.send_keys(parola)

log_in_button = driver.find_element_by_class_name("btn__primary--large")
log_in_button.click()
print("linkedin'e girildi")

time.sleep(3)
print("Job sekmesine girildi")
search_and_location = driver.find_elements_by_class_name("jobs-search-box__text-input")

search_box = search_and_location[0]
search_box.send_keys(keyword)

time.sleep(2)
location_box = driver.find_element_by_xpath("/html/body/div[8]/div[3]/div/section/section[1]/div/div[2]/div[2]/div/div/div/input")
location_box.send_keys(location)
time.sleep(2)
search_button = driver.find_element_by_class_name("jobs-search-box__submit-button")
driver.execute_script("arguments[0].click();", search_button)

print("iş araması yapıldı")

time.sleep(5)

jscode = """
let scroll = document.querySelector(".jobs-search-results")
scroll.scrollTo({top: scroll.scrollHeight, behavior: 'smooth'});
"""

description_list = []
company_names_list = []

count_pages = 0

for i in driver.find_elements_by_xpath("/html/body/div[8]/div[3]/div[3]/div/div/section[1]/div/div/section[2]/div/ul/li"):
    count_pages += 1

for page in range(1, count_pages):
    if page != 1:
        bas = driver.find_element_by_xpath(f"/html/body/div[8]/div[3]/div[3]/div/div/section[1]/div/div/section[2]/div/ul/li[{page}]/button")
        bas.click()
    driver.execute_script(jscode)

    time.sleep(2)
    jobs = driver.find_elements_by_class_name("job-card-list__title")



    for i in range(len(jobs)):
        jobs[i].click()
        company = driver.find_element_by_class_name("jobs-details-top-card__company-info").text

        content = driver.find_element_by_class_name("jobs-description-content__text").text

        description_list.append(content)
        company_names_list.append(company)
        print(i, company, " eklendi")
        print("*****")

        time.sleep(1)

dataframe = pd.DataFrame({"Company Name": company_names_list, "Description": description_list})
dataframe.to_csv(f'linkedin_jobs_{keyword}.txt', header=True, index=False, sep='\t', mode='a')
print(dataframe)
result = dataframe.to_json(orient="columns")
parsed = json.loads(result)
dumped = json.dumps(parsed, indent=4)
with open(f'linkedin_{keyword}.json', 'w') as outfile:
    json.dump(parsed, outfile)
print("**********************")
print(dumped)
driver.close()

response = requests.post('https://httpbin.org/post', json=result)

print("Status code: ", response.status_code)
print("Printing Entire Post Request")
print(response.json())