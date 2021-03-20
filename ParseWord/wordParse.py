#! /usr/local/bin/python3
from xml.dom.minidom import parse

def getData(node):
    return node.childNodes[0].data

def getTextElements(dom):
    TEXT_TAG = 'w:t'
    return dom.getElementsByTagName(TEXT_TAG)

def parseWord(dom):
    # returns the text of all text elements in the dom
    return  list(map(getData, getTextElements(dom)))

def parseDom(url):
    return parseWord(parse(url))


