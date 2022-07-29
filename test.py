import requests
import random
import time

# get request
def get_request(url):
    try:
        response = requests.get(url)
        return response.text
    except:
        return None

# get random number between 0 and 1
def get_random_number():
    return random.randint(0,1)

# get metrics request
def get_metrics(url):
    try:
        response = requests.get(url)
        return response.text
    except:
        return None
    
# main loop to get random number and post it to the server
def main():
    while True:
        get_request("http://localhost:5081/payload?'key%s=value%s&key%s=value%s'" % (get_random_number(),get_random_number(),get_random_number(),get_random_number()))
        print(get_metrics("http://localhost:5081/metrics"))
        time.sleep(0.001)

if __name__ == '__main__':
    main()