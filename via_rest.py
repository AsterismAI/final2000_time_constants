import requests

if __name__ == "__main__":
    _URL = "https://datacenter.iers.org/data/9/finals2000A.all"
    data = requests.get( _URL, verify=False )
    lines = data.text.split('\n')
    new_lines = reformatLines( lines )
    print(new_lines)
