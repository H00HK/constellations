from html.parser import HTMLParser
from html.entities import name2codepoint
import re
import glob

class MyHtmlParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.flag=False
    self.mydata = ''
  def handle_starttag(self, tag, attrs):
    if tag == "body":
      self.flag =True
  def handle_endtag(self,tag):
    if tag == "body":
      self.flag =False  
    if tag=="p" or tag=="div":
      self.mydata += '\n'
  def handle_data(self,data):
    if self.flag:
      self.mydata += data
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

def run(fname):
  html = str(open(fname).read())
  html = html.replace('\\n','\n')
  html = html.replace('\\t','\t')
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
  #html=remove_refs(html)  
  parser = MyHtmlParser()
  parser.feed(html)
  s = '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><div style="white-space: pre-wrap;">'+parser.mydata+'</div></body></html>'
  s = s.replace('[edit]','')
  s = s.replace("\\'","'")
  s = re.sub('\[\d+\]','',s)
  open('../wikidata/' + fname,'w').write(s)

def main():
  flist = glob.glob('*.html')
  for f in flist:
    run(f)
    print('done ' + f)    
  
    
if __name__ == '__main__':
  main()
                      