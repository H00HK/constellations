#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from xml.dom.minidom import parse, parseString

def remove_refs(text):
    '''Function to remove all references '''
    p = re.compile(r'<ref .*?/>', re.M|re.U|re.I|re.S)
    text = p.sub(u'', text)    
    p = re.compile(r'<ref.*?</ref>', re.M|re.U|re.I|re.S)
    text = p.sub(u'', text)
    return text
    
def remove_sup(text):
    '''Function to remove sup tags'''
    p = re.compile(r'<sup>', re.M|re.U|re.I|re.S)
    text = p.sub(u'', text)    
    p = re.compile(r'</sup>', re.M|re.U|re.I|re.S)
    text = p.sub(u'', text)
    return text
    
def remove_heading_markup(text):
    '''Function to remove wiki heading markup '''
    p = re.compile(r'^=+|=+$', re.M|re.U|re.I)
    text = p.sub(u'', text)
    return text

def remove_list_markup(text):   
    '''Function to remove wiki list markup. Loops through till no more matches are found (since
    the lists can be embedded in each other)
     '''
    done = False
    while not done:
        p = re.compile(r'^\:+', re.M|re.U|re.I)
        (text,num1) = p.subn(u'', text)
        p = re.compile(r'^\*+', re.M|re.U|re.I)
        (text,num2) = p.subn(u'',text)
        p = re.compile(r'^\#+', re.M|re.U|re.I)
        (text,num3) = p.subn(u'', text)
        tot_replacements = num1 + num2 + num3
        if tot_replacements == 0:
            done = True
    return text

def remove_apostrophe_seqs(text):
    '''Function to remove wiki apostrophe markup '''
    p = re.compile(r'\'{2,}', re.M|re.U|re.I)
    text = p.sub(u' ', text)
    return text

def remove_braces(text):
    '''Function to remove wiki braces markup. Loops through till no more matches are found
    (since braces can be embedded in braces)
    '''
    done = False
    while not done:
        p = re.compile(r'\{\{\{[^\{]*?\}\}\}', re.M|re.U|re.I|re.S)  #this can span multiple lines
        (text,num) = p.subn(u'', text)
        if num == 0:
            done = True
    done = False
    while not done:
        p = re.compile(r'\{\{[^\{]*?\}\}', re.M|re.U|re.I|re.S)  
        (text,num) = p.subn(u'', text)
        if num == 0:
            done = True
    p = re.compile(r'\{\{*?\}\}', re.M|re.U|re.I|re.S)  
    text = p.sub(u'', text)
    return text

def remove_wiki_tables(text):
    '''Function to remove wiki table data '''
    done = False
    while not done:
        p = re.compile(r'\{\|[^\{]*?\|\}', re.M|re.U|re.I|re.S)
        (text,num) = p.subn(u'', text)
        if num == 0:
            done = True
    return text

def transform_internal_links(text):
    '''Function which runs through various steps to transform wiki internal links '''
    wiki_langs = ['aa', 'ab', 'ace', 'af', 'ak', 'als', 'am', 'an', 'ang', 'ar', 'arc', 
        'arz', 'as', 'ast', 'av', 'ay', 'az', 'ba', 'bar', 'bat-smg', 'bcl', 'be', 'be-x-old', 
        'bg', 'bh', 'bi', 'bjn', 'bm', 'bn', 'bo', 'bpy', 'br', 'bs', 'bug', 'bxr', 'ca', 'cbk-zam', 
        'cdo', 'ce', 'ceb', 'ch', 'cho', 'chr', 'chy', 'ckb', 'closed-zh-tw', 'co', 'cr', 'crh', 
        'cs', 'csb', 'cu', 'cv', 'cy', 'cz', 'da', 'de', 'diq', 'dk', 'dsb', 'dv', 'dz', 'ee', 
        'el', 'eml', 'en', 'eo', 'epo', 'es', 'et', 'eu', 'ext', 'fa', 'ff', 'fi', 'fiu-vro', 'fj', 
        'fo', 'fr', 'frp', 'frr', 'fur', 'fy', 'ga', 'gan', 'gd', 'gl', 'glk', 'gn', 'got', 'gu', 
        'gv', 'ha', 'hak', 'haw', 'he', 'hi', 'hif', 'ho', 'hr', 'hsb', 'ht', 'hu', 'hy', 'hz', 'ia', 
        'id', 'ie', 'ig', 'ii', 'ik', 'ilo', 'io', 'is', 'it', 'iu', 'ja', 'jbo', 'jp', 'jv', 'ka', 
        'kaa', 'kab', 'kg', 'ki', 'kj', 'kk', 'kl', 'km', 'kn', 'ko', 'koi', 'kr', 'krc', 'ks', 
        'ksh', 'ku', 'kv', 'kw', 'ky', 'la', 'lad', 'lb', 'lbe', 'lg', 'li', 'lij', 'lmo', 'ln', 
        'lo', 'lt', 'lv', 'map-bms', 'mdf', 'mg', 'mh', 'mhr', 'mi', 'minnan', 'mk', 'ml', 'mn', 
        'mo', 'mr', 'mrj', 'ms', 'mt', 'mus', 'mwl', 'my', 'myv', 'mzn', 'na', 'nah', 'nan', 'nap', 
        'nb', 'nds', 'nds-nl', 'ne', 'new', 'ng', 'nl', 'nn', 'no', 'nov', 'nrm', 'nv', 'ny', 'oc', 
        'om', 'or', 'os', 'pa', 'pag', 'pam', 'pap', 'pcd', 'pdc', 'pi', 'pih', 'pl', 'pms', 'pnb', 
        'pnt', 'ps', 'pt', 'qu', 'rm', 'rmy', 'rn', 'ro', 'roa-rup', 'roa-tara', 'ru', 'rw', 'sa', 
        'sah', 'sc', 'scn', 'sco', 'sd', 'se', 'sg', 'sh', 'si', 'simple', 'sk', 'sl', 'sm', 'sn', 
        'so', 'sq', 'sr', 'srn', 'ss', 'st', 'stq', 'su', 'sv', 'sw', 'szl', 'ta', 'te', 'tet', 'tg', 
        'th', 'ti', 'tk', 'tl', 'tn', 'to', 'tpi', 'tr', 'ts', 'tt', 'tum', 'tw', 'ty', 'udm', 'ug', 
        'uk', 'ur', 'uz', 've', 'vec', 'vi', 'vls', 'vo', 'wa', 'war', 'wo', 'wuu', 'xal', 'xh', 'yi', 
        'yo', 'za', 'zea', 'zh', 'zh-cfr', 'zh-classical', 'zh-min-nan', 'zh-yue', 'zu']
    for ln in wiki_langs:
        p = re.compile('^\\[\\[%s:.*?\\]\\]' % ln, re.M|re.U|re.I)
        text = p.sub(u'', text)
    print ' done int. links part 1'
    done2 = False
    while not done2:
        done = False
        while not done:
            p = re.compile(r'\[\[[^\[\]]*?\|', re.M|re.U|re.I)
            (text,num) = p.subn(u'[[',text)
            if num == 0: 
                done = True
        done = False
        while not done:
            p = re.compile(r'\[\[[^\[\]]*?:', re.M|re.U|re.I)
            (text,num) = p.subn(u'[[',text)
            if num == 0: 
                done = True
        p = re.compile(r'(\[\[)([^\[\]]*?)(\]\])', re.M|re.U|re.I)
        (text,num) = p.subn(ur'\2',text)
        if num == 0:
            done2 = True
    print ' done int. links part 2'
    return text

def transform_external_links(text):
    '''Function that transforms wiki external link markup '''
    p = re.compile(r'\[http.*?\s([^\[]*?)\]', re.M|re.U|re.I)
    text = p.sub(ur'\1', text)
    p = re.compile(r'\[(http.*?)\]', re.M|re.U|re.I)
    text = p.sub(ur'\1', text)
    return text

def remove_px_details(text):
    '''This removes some image markup not cleaned by the other methods '''
    p = re.compile(r'[0-9]+px|left|right|thumb', re.M|re.U|re.I)
    text = p.sub(u'', text)
    return text   

def remove_redirects(text):
    '''This removes wiki redirect markup '''
    return text.replace('#REDIRECT', '')  

def convert_ampersand(text):
    '''Function to replace ampersand in the corpus text. Uses python string replace.'''
    entities = {'&':'och' }
    for k,v in entities.items():
        text = text.replace(k, v)
        text = text.replace(k.upper(), v)
    return text  

def remove_wiki_markup(text):
    '''Function which runs throuh various steps to clean wiki markup from input text '''
    print 'removing wiki markup..'
    text = remove_refs(text)
    print ' done refs'
    text = remove_sup(text)
    print ' done sup'    
    text = remove_heading_markup(text)
    print ' done headings'
    text = remove_list_markup(text)
    print ' done lists'
    text = remove_apostrophe_seqs(text)
    print ' done apostrophes'
    text = remove_braces(text)
    print ' done braces'
    text = remove_wiki_tables(text)
    print ' done tables'
    text = transform_internal_links(text)
    print ' done int. links'
    text = transform_external_links(text)
    print ' done ext. links'
    text = remove_px_details(text)
    print ' done px details'
    text = remove_redirects(text)
    print ' done redirects'
    text = convert_ampersand(text)
    print ' done ampersand'
    print '...done'
    return text

def read_file(filename):
    '''Utility function to read a unicode file '''
    with open(filename) as f:
        text = f.read().decode('UTF-8')
    return text

def write_file(filename, text):
    '''Utility function to write a unicode file '''
    with open(filename, mode='w') as f:
        f.write(text.encode('UTF-8'))

'''From http://www.textfixer.com/resources/common-english-words.txt'''
stopwords = ['a','able','about','across','after','all','almost','also','am','among','an','and','any','are','as','at','be','because','been','but','by','can','cannot','could','dear','did','do','does','either','else','ever','every','for','from','get','got','had','has','have','he','her','hers','him','his','how','however','i','if','in','into','is','it','its','just','least','let','like','likely','may','me','might','most','must','my','neither','no','nor','not','of','off','often','on','only','or','other','our','own','rather','said','say','says','she','should','since','so','some','than','that','the','their','them','then','there','these','they','this','tis','to','too','twas','us','wants','was','we','were','what','when','where','which','while','who','whom','why','will','with','would','yet','you','your']

def main():
    '''Main function of the program. It reads the downloaded wiki xml file and cleans 
    the html and wiki markup and writes the data to another file for further processing.
    '''
    print 'reading file t022.txt'
    fname = 't022.txt'
    wiki_text = read_file(fname)
    clean_text = remove_wiki_markup(wiki_text)
    print 'writing to Antlia.html'
    write_file('Antlia.html', '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><div style="white-space: pre-wrap;">' +clean_text+'</div></body></html>')
    print 'done'
    

if __name__ == "__main__":
    main()

