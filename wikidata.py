# -*- coding: utf-8 -*-

# run with python3. 

from html.parser import HTMLParser
from html.entities import name2codepoint
import re
import glob
import urllib.request
import time 

class MyHtmlParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.flag=False
    self.nottocflag = True
    self.mydata = ''
  def handle_starttag(self, tag, attrs):
    if tag == "body":
      self.flag =True
    if tag in ('div', 'h1','h2','h3'):
      self.mydata += '\n'      
    for attr in attrs:
      if attr[1] in ('toc', 'toctitle','tocnumber','toctext'):  
        self.nottocflag = False
  def handle_endtag(self,tag):
    if tag == "body":
      self.flag =False  
    elif tag in ("p","div",'tr','li','h1','h2','h3'):
      self.mydata += '\n'
    elif tag == 'th':
      self.mydata += ': '  
    elif tag == 'td':
      self.mydata +='    '
    elif tag == 'br':
      self.mydata += ' '     
  def handle_data(self,data):
    if self.flag and self.nottocflag:
      self.mydata += data
    self.nottocflag = True
  def handle_comment(self,comment):
    pass
  def handle_entityref(self,name):
    c=chr(name2codepoint[name])
    if self.flag:
      self.mydata += c
  def handle_charref(self,name):
    if name.startswith('x'):
      c=chr(int(name[1:],16))
    else:
      c=chr(int(name))
    if self.flag:
      self.mydata += c
  def handle_decl(self,data):
    pass

def cleanup(html):
  html = html.replace('\\n','')
  html = html.replace('\\t','')
  p=re.compile(r'(\\x[a-f0-9][a-f0-9])+')
  flag = True
  while flag:
    hx = p.search(html)
    if hx:
      h1 = html[hx.span(0)[0]:hx.span(0)[1]]
      h2=h1.replace('\\x','')
      h3 = bytes.fromhex(h2).decode('utf-8')
      html = html[:hx.span(0)[0]] + bytes.fromhex(h2).decode('utf-8') + html[hx.span(0)[1]:]
    else:
      flag = False      
  parser = MyHtmlParser()
  parser.feed(html)
  s = parser.mydata
  index = s.find('Abbreviation')
  if index != -1:  
    s = s[index:]
  index = s.find('Retrieved from')
  index2 = s.find('\n',index)
  if index != -1 and index2 != 1:  
    link = s[index:index2]
  index = s.rfind('External links')
  if index != -1:
    s= s[:index]
  s += '\n' + link + '\n'
  s = '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><div style="white-space: pre-wrap;">\n' + s + '</div></body></html>'
  s = s.replace('[edit]','')
  s = s.replace("\\'","'")
  s = re.sub('\[\d+\]','',s)
  s = re.sub('\n(\s)+\n','\n',s)
  s = re.sub('\n(\n)+','\n\n',s)
  return s    
                      
def write_file(filename, text):
    '''Utility function to write a unicode file '''
    with open(filename, mode='w', encoding='utf-8') as f:
        f.write(text)

def process(c, url):
  print(c)
  headers = {'User-Agent' : 'datapull by gituser1357 (nologin)'}
  req = urllib.request.Request(url,None,headers)
  res = urllib.request.urlopen(req)
  htmldata = str(res.read())
  htmldata = cleanup(htmldata)
  write_file('wikidata/' + (c).replace('_','') + '.html',htmldata) 
  time.sleep(5)      

def main():
  baseurl = 'http://en.wikipedia.org/wiki/'
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
  c = 'Andromeda'
  url = baseurl + c + '_(constellation)'  
  process(c, url)
  '''for c in constellations1:
    url = baseurl + c  
    process(c, url)
  for c in constellations2:
    url = baseurl + c + '_(constellation)'
    process(c, url)'''      

if __name__ == '__main__':
  main()
  

