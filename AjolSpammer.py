import requests
from random import random, randint, getrandbits, choices
from time import sleep, time

# ===== UTILITY FUNCTIONS =====

# Clamps a numeric value to a min and max value.
def clamp(value: int, lower_limit: int, upper_limit: int):
    return max(lower_limit, min(upper_limit, value))

# Generates a random boolean.
def randbool():
    return bool(getrandbits(1))

# Generates a random numeric value biased towards the given value.
class BiasedRandom:
    def __init__(self, bias: int, lower_limit: int, upper_limit: int, bias_factor = 2):
        if lower_limit > bias or upper_limit < bias: 
            raise Exception("Cannot create an instance of BiasedRandom with invalid arguments.")
        dist = max(upper_limit - bias, bias - lower_limit)
        self.population = range(lower_limit, upper_limit + 1)
        self.weights = [(dist - abs(value - bias)) * bias_factor for value in self.population]
    
    def randint(self):
        elements = choices(self.population, self.weights, k = 1)
        return elements[0]

# Returns a small variant of the given value.
def variate(value: int, lower_limit: int, upper_limit: int):
    offset = randint(-1, 1)
    return clamp(value + offset, lower_limit, upper_limit)
    
# Sleeps for an exact duration given a start time.
def wait(delay: float, start: float):
    now = time()
    elapsed = now - start
    remaining = clamp(delay - elapsed, 0, delay)
    sleep(remaining)
    return now

# Encodes the given values into a list of valid url params.
def encode(*arr: str):
    return [value.replace(" ", "+").replace("'", "%27") for value in arr]

# ===== CONSTANTS =====

base_url = "https://docs.google.com/forms/d/e/1FAIpQLScZ_EuVy1EZv6_TJ6HsRY7MUgVfXyHc1guXJnY-X10QOc_THQ/formResponse"
delay = 0.4
no_of_submissions = 50
bias4 = BiasedRandom(4, 1, 5)

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
    education_level = education_levels[randint(0, 2)] if is_teenager else education_levels[3]

    # It would make more sense if most answer "More than 10 years".
    how_long_in_jkt = years[0] if random() < 0.1 else years[1]

    # Random answers are fine for these.
    bothered = bias4.randint()
    industrial_emissions = randint(1, 5)
    vehicle_traffic = randint(1, 5)
    waste_burning = randint(1, 5)
    agriculture = randint(1, 5)
    construction = randint(1, 5)
    news_outlets = randint(1, 5)
    social_media = randint(1, 5)
    government = randint(1, 5)
    organizations = randint(1, 5)
    mobile_apps = randint(1, 5)

    # These should match the "bothered" scale to make sense.
    concerned = variate(bothered, 1, 5)
    rating = 6 - variate(bothered, 1, 5)

    # More random answers.
    improvement = air_change[randint(0, 3)]
    awareness = randint(1, 5)
    participated = participation[randint(0, 4)]
    believe_strict = randint(1, 5)
    education_campaigns = randint(1, 5)
    community_workshops = randint(1, 5)
    strict_enforcement = randint(1, 5)
    media_strategies = randint(1, 5)
    sustainable_transport = randint(1, 5)

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

last_request = time()

for i in range(no_of_submissions):
    try:
        data = generate_answers()
        url = generate_url(data)
        response = requests.get(url)
        if response.ok:
            print("Submitted " + str(i) + " times.")
            last_request = wait(delay, last_request)
        else: 
            print(response.reason)
            break
    except Exception as error:
        print(error)
        break
