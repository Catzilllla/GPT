# import argparse

# parser = argparse.ArgumentParser(description='Process some integers.')
# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')

# args = parser.parse_args()
# print(args.accumulate(args.integers))



# # cli.py
# import click

# @click.command()
# def main():
#     print("I'm a beautiful CLI ✨")

# if __name__ == "__main__":
#     main()



import requests
import click

SAMPLE_API_KEY = '9957efde1fb27b62cf554f1c0e13e4ad'

def current_weather(location, api_key=SAMPLE_API_KEY):
    url = 'http://samples.openweathermap.org/data/2.5/weather'

    query_params = {
        'q': location,
        'appid': api_key,
    }

    response = requests.get(url, params=query_params)

    return response.json()['weather'][0]['description']

@click.command()
@click.argument('location')
def main(location):
    weather = current_weather(location)
    print(f"The weather in {location} right now: {weather}.")