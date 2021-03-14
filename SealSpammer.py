import requests
import json
import random
from sys import exit

url = "https://docs.google.com/forms/d/e/1FAIpQLSf7IoLBMXSbKt4QE6AUGDdjkpGgHi80s3y3vJaSrfG5G3bJBw/formResponse"

# "How did you find it useful?" question options.
useful_options = [
    "Because it will help the prevention of covid",
    "Because I can see the data the amount of people who are infected, cured and deceased",
    "Because I can see the areas of the map where there are a high concentration of infected people",
    "Not useful but government recomended"
]

# "With the use of this app what may be the possible problems you may have to face?" question options.
problems_options = [
    "privacy of information",
    "Security problems through location and other details collected",
    "Need to buy a new device to use the app",
    "Consumes lot of battery",
    "Continuous internet connection requires",
    "Data provided is not always correct"
]

# "If you are using PeduliLindungi what are the difficulties that you have faced?" question options.
difficulties_options = [
    "Hard to use",
    "Consumes battery",
    "Datas were not accurate",
    "Lack of users"
]

# "What is the reason of not using the app?" question options.
why_not_options = [
    "It may lead to sharing my personal information with others",
    "Security is not implemented in the app",
    "There is no clear information about the who and how the data will be handled",
    "not interested in these app",
    "Do not trust these apps",
    "data is not reliable and does not really help in giving the required information",
    "will not help in reducing the infection of the disease"
]

# "If you dont agree to the policies state the reason" question options.
why_not_agree_options = [
    "Too long to read",
    "Not clear with the terms",
    "data collected violates the privacy of our information",
    "Others"
]

# "What do you think of the use of mobile phone number and full name for the registration of the app?" question options.
for_registration_options = [
    "It is insecure",
    "It lacks privacy",
    "Why do they need it?",
    "It is completely fine"
]

def createFilledURL():
    # Get random person data.
    response = requests.get("https://randomuser.me/api/")
    if (response.status_code != 200):
        print("Unable to fetch random user data.")
        exit()
        
    data = response.json()['results'][0]
    person_name = (data["name"]["first"] + " " + data["name"]["last"]).title()
    person_age = str(data["dob"]["age"])
    person_gender = data["gender"].title()

    # Create the data to be submitted to the form.
    pageHistory = "0"
    know_peduli_lindugi = bool(random.getrandbits(1))
    form_data = {
        '664858686': person_name,
        '1306454953': person_age,
        '1413967570': person_gender,
        '1820600566': "Yes" if know_peduli_lindugi else "No", # know the app
        '1406398408': "Yes" if bool(random.getrandbits(1)) else "No", # smartphone
        '1972733197': "Yes" if bool(random.getrandbits(1)) else "No" # internet
    }

    if (know_peduli_lindugi):
        pageHistory += ",1"
        use_peduli_lindungi = bool(random.getrandbits(1))
        know_policies = bool(random.getrandbits(1))
        form_data.update({
            '442098967': "Yes" if use_peduli_lindungi else "No", # use the app
            '140291473': "Yes" if bool(random.getrandbits(1)) else "No", # easy to register
            '127619935': useful_options[random.randint(0, 3)], # useful
            '700607532': "Yes" if bool(random.getrandbits(1)) else "No", # use with personal device
            '634635597': problems_options[random.randint(0, 5)], # possible problems
            '1477133041': "Yes" if bool(random.getrandbits(1)) else "No", # reliable
            '1793079760': "Yes" if bool(random.getrandbits(1)) else "No", # monitoring
            '1867664525': difficulties_options[random.randint(0, 3)], # difficulties
            '679963689': "Yes" if bool(random.getrandbits(1)) else "No", # user interface
            '1174718006': "Yes" if bool(random.getrandbits(1)) else "No", # bluetooth
            '1819983885': "Yes" if bool(random.getrandbits(1)) else "No", # antivirus
            '2135580095': "Yes" if know_policies else "No" # policies
        })

        if (not know_policies):
            pageHistory += ",2"
            form_data.update({
                '1013960538': why_not_options[random.randint(0, 6)] # why not use
            })
        else:
            pageHistory += ",3"
            policies_agree = bool(random.getrandbits(1))
            form_data.update({
                '1430203499': "Yes" if policies_agree else "No", # agree with policies
                '600062886': "Yes" if bool(random.getrandbits(1)) else "No", # handled safely
                '1222898751': "Yes" if bool(random.getrandbits(1)) else "No", # ask others
                '823211194': "Yes" if bool(random.getrandbits(1)) else "No" # believe has helped
            })
            if (policies_agree):
                form_data.update({
                    '835960768': why_not_agree_options[random.randint(0, 3)] # reason for not agreeing
                })
    else:
        pageHistory += ",4"
        form_data.update({
            '570946958': "Yes" if bool(random.getrandbits(1)) else "No",
            '1549030096': "Yes" if bool(random.getrandbits(1)) else "No"
        })

    pageHistory += ",5"
    form_data.update({
        '1018401778': "Yes" if bool(random.getrandbits(1)) else "No",
        '790967436': for_registration_options[random.randint(0, 3)]
    })

    new_url = url + "?submit=Submit" + "&pageHistory=" + pageHistory

    for key, value in form_data.items():
        new_url += "&entry." + key + "=" + value.replace(" ", "+")

    return new_url

count = 0
while True:
    filled_url = createFilledURL()
    requests.get(filled_url)
    count += 1
    print("Sent " + str(count) + " Data")

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
# bluetooth: 1174718006
# antivirus: 1819983885
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