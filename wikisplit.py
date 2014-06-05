#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.dom.minidom import parse, parseString

def read_file(filename):
    with open(filename) as f:
        text = f.read().decode('UTF-8')
    return text

def write_file(filename, text):
    with open(filename, mode='w') as f:
        f.write(text.encode('UTF-8'))

def main():
    xml_file_name = 'Wikipedia-20140601045748.xml'
    tlist = parse(xml_file_name).getElementsByTagName('text')
    for i,t in enumerate(tlist):
      text = t.childNodes[0].nodeValue
      fname = 't' + str(i).zfill(3) + '.txt'
      print 'writing to ', fname
      write_file(fname, text)
    print 'done'
    

if __name__ == "__main__":
    main()

