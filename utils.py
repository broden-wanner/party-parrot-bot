from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from typing import List

BASE_URL = 'https://cultofthepartyparrot.com'

class Parrot:
    """
    Parrot class used for storing data on the party parrots
    """

    def __init__(self, name: str, url: str, id: str):
        self.name = name
        self.url = url
        self.id = id

    def __str__(self):
        return f'Parrot({self.name}, {self.url})'

    def __repr__(self):
        return self.__str__()

def get_parrots_from_site() -> List[Parrot]:
    """
    Parses the cult of the party parrots site for the complete list of all
    party parrots
    """

    # Get the current cult of the party parrots site
    req = Request(BASE_URL, headers={'User-Agent': 'Mozilla/5.0'})
    webpage_text = urlopen(req).read()

    # Parse for the imgaes
    page = BeautifulSoup(webpage_text, 'html.parser')
    images = page.select('ul li img')

    # Create a list of parrot objects
    parrot_list = []
    for img in images:
        parrot = Parrot(
            name=img['alt'], 
            url=f"{BASE_URL}{img['data-src']}",
            id=img['alt'].lower().replace(' ', '')
        )
        parrot_list.append(parrot)

    return parrot_list

if __name__ == "__main__":
    get_parrots_from_site()