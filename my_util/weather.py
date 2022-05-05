import requests

def get_weather(lat=37.311494, lng=127.075369):
    with open('./static/keys/openweatherkey.txt') as key_fd:
        oweather_key = key_fd.read()

    open_weather = 'http://api.openweathermap.org/data/2.5/weather'
    url = f'{open_weather}?lat={lat}&lon={lng}&appid={oweather_key}&units=metric&lang=kr'
    result = requests.get(url).json()

    desc = result['weather'][0]['description']
    icon_code = result['weather'][0]['icon']
    icon_url = f'http://openweathermap.org/img/w/{icon_code}.png'
    temp = result['main']['temp']
    temp_min = result['main']['temp_min']
    temp_max = result['main']['temp_max']
    temp = round(float(temp)+0.01, 1)

    html = f'''<img src="{icon_url}" height="32"><strong>{desc}</strong>, 
                온도: <strong>{temp:.1f}&#8451</strong>, {temp_min:.1f}/{temp_max:.1f}&#8451'''
    return html