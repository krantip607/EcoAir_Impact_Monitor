import requests

def get_live_data(city_name, token):
    url = f"https://api.waqi.info/feed/{city_name}/?token={token}"
    try:
        r = requests.get(url).json()
        if r['status'] == 'ok':
            d = r['data']
            return {
                "name": d['city']['name'],
                "aqi": d.get('aqi', 0),
                "pm25": d['iaqi'].get('pm25', {'v': 0})['v'],
                "so2": d['iaqi'].get('so2', {'v': 0})['v'],
                "humidity": d['iaqi'].get('h', {'v': 0})['v']
            }
    except Exception: return None