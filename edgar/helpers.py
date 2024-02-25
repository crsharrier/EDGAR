import time
import requests
from typing import Optional
from colorama import Fore

DEBUG = Fore.GREEN
DEBUG_HEADER = Fore.LIGHTGREEN_EX
ERROR = Fore.RED
TIMER = Fore.BLUE
SUCCESS = Fore.MAGENTA

class Colour:
    def __init__(self, colour: str):
        self.colour = colour

    def __enter__(self):
        print(self.colour, end='')

    def __exit__(self, exc_type, exc_value, traceback):
        print(Fore.RESET, end='')

class Timer:
    def __init__(self,  title: Optional[str]=None):
        if title:
            self.title = Fore.YELLOW + title + ': ' + Fore.RESET
        else:
            self.title = '' 

    def __enter__(self):
        self.start_time = time.time()
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        print(self.title, end='')
        with Colour(TIMER):
            if self.duration < 60.0:
                print(f"Time taken: {self.duration: .5f} seconds")
            else:
                mins = self.duration // 60
                min_word = 'mins' if mins > 1 else 'min'
                secs = self.duration % 60
                print(f"Time taken: {mins} {min_word} {secs: .5f} secs")


# def save_response(url, path):
#     response = requests.get(url, headers=DataSource.headers)
#     if response.status_code != 200:
#         print(f"Failed to retrieve the HTTP response. Status code: {response.status_code}")
#         return
#     with open(path, 'w', encoding='utf-8') as f:
#         f.write(response.content.decode('utf-8'))