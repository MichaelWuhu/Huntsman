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

