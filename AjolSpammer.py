import requests
import random
from time import sleep, time

# ===== UTILITY FUNCTIONS =====

# Encodes the given values into a list of valid url params.
def encode(*arr: str):
    return [value.replace(" ", "+").replace("'", "%27") for value in arr]

# Generates a random boolean.
def randbool():
    return bool(random.getrandbits(1))

# Clamps a numeric value to a min and max value.
def clamp(value: int, lower_limit: int, upper_limit: int):
    return max(lower_limit, min(upper_limit, value))

# Returns a small variant of the given value.
def variate(value: int, lower_limit: int, upper_limit: int):
    i = random.randint(0, 2)
    if i == 0: return value
    return clamp(value - 1 if i == 1 else value + 1, lower_limit, upper_limit)
    
# Sleeps for an exact duration given a start time.
def wait(delay: float, start: float):
    now = time()
    elapsed = now - start
    remaining = max(0, delay - elapsed)
    sleep(remaining)
    return now

# ===== CONSTANTS =====

base_url = "https://docs.google.com/forms/d/e/1FAIpQLScZ_EuVy1EZv6_TJ6HsRY7MUgVfXyHc1guXJnY-X10QOc_THQ/formResponse"
delay = 0.4

# The possible choices for text-based answers.
age_ranges = encode("11-21", "22-34")
education_levels = encode("Less than high school", "High school graduate", "College", "Bachelor's degree")
years = encode("6-10 years", "More than 10 years")
air_change = encode("Worsened", "A little bit improved", "Remained the same", "Improved a lot")
participation = encode("Never", "Rarely", "Occasionally", "Frequently", "Always")

# ===== ANSWER GENERATION =====

def generate_answers() -> 'dict[str, str]':
    # Ajol wants only answers from younger people.
    is_teenager = randbool()
    age_range = age_ranges[0] if is_teenager else age_ranges[1]
    education_level = education_levels[random.randint(0, 2)] if is_teenager else education_levels[3]

    # It would make more sense if most answer "More than 10 years".
    how_long_in_jkt = years[0] if random.random() < 0.1 else years[1]

    # Random answers are fine for these.
    bothered = random.randint(1, 5)
    industrial_emissions = random.randint(1, 5)
    vehicle_traffic = random.randint(1, 5)
    waste_burning = random.randint(1, 5)
    agriculture = random.randint(1, 5)
    construction = random.randint(1, 5)
    news_outlets = random.randint(1, 5)
    social_media = random.randint(1, 5)
    government = random.randint(1, 5)
    organizations = random.randint(1, 5)
    mobile_apps = random.randint(1, 5)

    # These should match the "bothered" scale to make sense.
    concerned = variate(bothered, 1, 5)
    rating = 6 - variate(bothered, 1, 5)

    # More random answers.
    improvement = air_change[random.randint(0, 3)]
    awareness = random.randint(1, 5)
    participated = participation[random.randint(0, 4)]
    believe_strict = random.randint(1, 5)
    education_campaigns = random.randint(1, 5)
    community_workshops = random.randint(1, 5)
    strict_enforcement = random.randint(1, 5)
    media_strategies = random.randint(1, 5)
    sustainable_transport = random.randint(1, 5)

    # Map the answers onto their corresponding form IDs.
    return {
        '1017145759': age_range,
        '248027451': education_level,
        '854228483': how_long_in_jkt,
        '493925594': bothered,
        '2048542365': industrial_emissions,
        '299781081': vehicle_traffic,
        '1433369133': waste_burning,
        '336665674': agriculture,
        '1112590324': construction,
        '713798989': news_outlets,
        '897598844': social_media,
        '2024742825': government,
        '1102258965': organizations,
        '124867909': mobile_apps,
        '1567909505': concerned,
        '386123517': rating,
        '704504329': improvement,
        '22713487': awareness,
        '916972995': participated,
        '670200831': believe_strict,
        '1977100364': education_campaigns,
        '1100815261': community_workshops,
        '814292055': strict_enforcement,
        '2026794329': media_strategies,
        '1179792701': sustainable_transport
    }

# Formats the data into a URL to submit the form data.
def generate_url(data: 'dict[str, str]'):
    url = base_url + "?pageHistory=0"
    for key, value in data.items():
        url += "&entry." + key + "=" + str(value)
    return url

# ===== THE ACTUAL PROGRAM LOOP =====

count = 0
last_request = time()

while True:
    try:
        data = generate_answers()
        url = generate_url(data)
        response = requests.get(url)
        if response.ok:
            count += 1
            print("Submitted " + str(count) + " times.")
            last_request = wait(delay, last_request)
        else: 
            print(response.reason)
            break
    except Exception as error:
        print(error)
        break
