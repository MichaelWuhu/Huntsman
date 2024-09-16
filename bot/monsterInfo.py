import requests  
from bs4 import BeautifulSoup  
import pandas as pd
    
def getdata(url):  
    r = requests.get(url)  
    return r.text  

def getMonsterImage(monster_name): 
    htmldata = getdata(f"https://monsterhunter.fandom.com/wiki/{monster_name}")  
    soup = BeautifulSoup(htmldata, 'html.parser')  
    image = soup.find('a', class_='image image-thumbnail')['href']
    print(image)
    return image

def getMonsterHP(monster_name, rank): # rank = low, high, master
    htmldata = getdata(f"https://monsterhunter.fandom.com/wiki/MHWI:_Monster_HP")
    soup = BeautifulSoup(htmldata, 'html.parser')
    table = soup.find('table', class_='article-table')
    # print(table)
    for row in table.find_all('tr')[1:]:  # Skip the header row
        cols = row.find_all('td')
        if cols[0].text.strip() == monster_name:
            values = [int(col.text.strip()) if col.text.strip() != 'N/A' else col.text.strip() for col in cols[1:4]]
    
    # print(values)

    if rank == "low":
        hp = values[0]
        if hp == 'N/A':
            if values[1] == 'N/A':
                hp = values[2] // 9
            else:
                hp =  values[1] // 2
    elif rank == "high":
        hp= values[1]
        if hp == 'N/A':
            if values[0] == 'N/A':
                hp = values[2] // 2
            else:
                hp = values[0] * 3
    elif rank == "master":
        hp = values[2]
        if hp == 'N/A':
            if values[0] == 'N/A':
                hp = values[1] * 3
            else:
                hp = values[0] * 9
    
    return hp


def getMonsterElement(monster_name):
    # Read the CSV file into a pandas DataFrame
    elementsheet = pd.read_csv('MH Element Sheet.csv')

    # Initialize dictionaries to store monsters for each element
    element_dict = {
        'Fire': [],
        'Water': [],
        'Thunder': [],
        'Ice': [],
        'Dragon': []
    }

    # Iterate over each column (element) and its corresponding monsters
    for column in elementsheet.columns:
        element_monsters = elementsheet[column].dropna().tolist()
        element_dict[column] = element_monsters

    # Check if the monster exists in any of the element lists
    for element, monsters in element_dict.items():
        if monster_name in monsters:
            return element

    # If the monster is not found, return None
    print(f"element not found for monster: {monster_name}")
    return 'Not Found'

def getMonsterElementEmoji(element):
    
    element_emojis = {
        'Fire':'<:fire:1242956619512287403>',
        'Water':'<:water:1242956617255878758>',
        'Thunder':'<:thunder:1242956615687209020>',
        'Ice':'<:ice:1242956614164549682>',
        'Dragon':'<:dragon:1242956612340023438>',
        'Non-Elemental':'🦴',
    }

    return element_emojis[element]