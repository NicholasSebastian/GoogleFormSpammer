import requests
import json
import random
from sys import exit

# Won't work if the form has multiple pages.

url = "https://docs.google.com/forms/d/e/1FAIpQLSf7IoLBMXSbKt4QE6AUGDdjkpGgHi80s3y3vJaSrfG5G3bJBw/formResponse"

user_agent = {
    'Referer': 'https://docs.google.com/forms/d/e/1FAIpQLSf7IoLBMXSbKt4QE6AUGDdjkpGgHi80s3y3vJaSrfG5G3bJBw/viewform',
    'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36"
}

response = requests.get("https://randomuser.me/api/")
if (response.status_code != 200):
    print("Unable to fetch random user data.")
    exit()
    
data = response.json()['results'][0]
person = {
    "name": (data["name"]["first"] + " " + data["name"]["last"]).title(),
    "age": str(data["dob"]["age"]),
    "gender": data["gender"].title()
}

pageHistory = "0"
know_peduli_lindugi = bool(random.getrandbits(1))

form_data = {
    'entry.664858686': person["name"], # your name
    'entry.1306454953': person["age"], # your age
    'entry.1413967570': person["gender"], # your gender
    'entry.1820600566': "Yes" if know_peduli_lindugi else "No", # know the app
    'entry.1406398408': "Yes" if bool(random.getrandbits(1)) else "No", # smartphone
    'entry.1972733197': "Yes" if bool(random.getrandbits(1)) else "No" # internet
}

if (know_peduli_lindugi):
    pageHistory += ",1"
    use_peduli_lindungi = bool(random.getrandbits(1))

    form_data.update({
        'entry.442098967': "Yes" if use_peduli_lindungi else "No", # use the app
        'entry.140291473': "Yes" if bool(random.getrandbits(1)) else "No", # easy to register
        
    })

form_data.update({ 
    'draftResponse': '[]',
    'pageHistory': pageHistory 
})

print(form_data)

# requests.post(url, data = form_data, headers = user_agent)

# name: 664858686
# age: 1306454953
# gender: 1413967570
# know: 1820600566
# smartphone: 1406398408
# internet: 1972733197

# IF YOU KNOW PEDULI LINDUNGI
# use: 442098967
# register: 140291473
# useful: 127619935
# personal: 700607532
# outcome: 634635597
# reliable: 1477133041
# monitoring: 1793079760
# difficulties: 1867664525
# user_interface: 679963689
# policies: 2135580095

# IF YOU'RE NOT USING PEDULI LINDUNGI
# why_not_use: 1013960538

# IF YOU READ THE POLICIES
# policies_agree: 1430203499
# not_agree_reason: 835960768
# handled_safely: 600062886
# ask_others: 1222898751
# believe_help: 823211194

# IF YOU DON'T KNOW PEDULI LINDUNGI
# useful: 570946958
# breach: 1549030096

# EVERYONE
# inappropriate: 1018401778
# for_registration: 790967436