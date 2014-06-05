from html.parser import HTMLParser
from html.entities import name2codepoint

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
    self.mydata += c
  def handle_charref(self,name):
    if name.startswith('x'):
      c=chr(int(name[1:],16))
    else:
      c=chr(int(name))
    self.mydata += c
  def handle_decl(self,data):
    pass

def main():
  html = str(open('Andromeda.html').read())
  html = html.replace('\\n','\n')
  html = html.replace('\\t','\t')
  parser = MyHtmlParser()
  parser.feed(html)
  s= '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><div style="white-space: pre-wrap;">'+parser.mydata+'</div></body></html>'
  open('../wikidata/Andromeda.html','w').write(s)
    
if __name__ == '__main__':
  main()
                      