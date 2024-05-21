import requests  
from bs4 import BeautifulSoup  
    
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