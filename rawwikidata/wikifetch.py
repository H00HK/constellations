# -*- coding: utf-8 -*-

# run with python3. 

import urllib.request
import time 

def gettext(html):
  soup = BeautifulSoup(html)
  return(str(soup.body))


def write_file(filename, text):
    '''Utility function to write a unicode file '''
    with open(filename, mode='w') as f:
        f.write(text)

def main():
  baseurl = 'http://en.wikipedia.org/wiki/'
  headers = {'User-Agent' : 'datapull by gituser1357 (nologin)'}
  constellations1 = [
    'Antlia','Apus',
    'Bootes','Caelum','Camelopardalis','Canes_Venatici','Canis_Major','Canis_Minor',
    'Capricornus',
    'Centaurus','Cetus','Chamaeleon',
    'Coma_Berenices','Corona_Australis','Corona_Borealis',
    'Crux','Delphinus','Dorado',
    'Equuleus','Fornax',
    'Horologium','Hydrus',
    'Lacerta',
    'Leo_Minor','Lyra',
    'Microscopium','Monoceros','Musca',
    'Octans','Ophiuchus',
    'Pictor','Piscis_Austrinus','Puppis','Pyxis','Reticulum','Sagitta','Scorpius',
    'Scutum',
    'Serpens','Sextans',
    'Telescopium','Triangulum','Triangulum_Australe','Tucana','Ursa_Major','Ursa_Minor',
    'Volans','Vulpecula']; 
  constellations2 = ['Andromeda',
    'Aquarius',
    'Aquila','Ara','Aries',
    'Auriga','Cancer',
    'Carina',
    'Cassiopeia','Cepheus','Circinus',
    'Columba','Corvus',
    'Crater',
    'Cygnus','Draco',
    'Eridanus','Gemini','Grus','Hercules',
    'Hydra','Indus',
    'Leo',
    'Lepus','Libra',
    'Lupus','Lynx','Mensa','Norma',
    'Orion','Pavo',
    'Pegasus',
    'Perseus','Phoenix',
    'Pisces','Sagittarius',
    'Sculptor',
    'Taurus',
    'Vela','Virgo'];      
  for c in constellations1:
    url = baseurl + c  
    req = urllib.request.Request(url,None,headers)
    res = urllib.request.urlopen(req)
    htmldata = str(res.read())
    write_file((c).replace('_','') + '.html',htmldata)
    time.sleep(5)
  for c in constellations2:
    url = baseurl + c + '_(constellation)'
    req = urllib.request.Request(url,None,headers)
    res = urllib.request.urlopen(req)
    htmldata = str(res.read())
    write_file((c).replace('_','') + '.html',htmldata)
    time.sleep(5)    
    


if __name__ == '__main__':
  main()
  

