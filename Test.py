import requests

url = "https://docs.google.com/forms/d/e/1FAIpQLSefg4JHV8-zY05Ci4lHKzHep6pWTgASqFaX5fWQVGL13UINsw/formResponse"

# 1235143921 column 1
# 1113394580 column 2
# 208278402 next steps
# 1847757769 column 1

# 1650249198 column 2
# 629967779 next steps

# 671632207 email option

data = {
    "1235143921": "2020-01-02",
    "1113394580": "Option 2",
    "208278402": "Complete",
    "1847757769": "balalaika",

    "1650249198": "bocca della verita",
    "629967779": "Complete",

    "671632207": "This is Final",
}

url += "?pageHistory=0,1,2"
url += "&submit=Submit"

for key, value in data.items():
    url += "&entry." + key + "=" + value.replace(" ", "+")

requests.get(url)
print("Sending " + url)