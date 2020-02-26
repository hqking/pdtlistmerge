#!/usr/bin/python

import sys
import xml.etree.ElementTree as ET

def readPdtlist(xmlfile, boardDict):
    tree = ET.parse(xmlfile)
    boardNode = tree.getroot()

    for board in boardNode:
        if board.tag != "board":
            continue

        boardtype = "None"
        cpts = set()
        hardtypes = set()
        cputype = "noarch"

        for child in board:
            if child.tag == "boardtype":
                boardtype = child.text

            if child.tag == "hardtype":
                for hardtype in child.text.split(','):
                    hardtypes.add(hardtype)

            if child.tag == "cputype":
                cputype = child.text

            if child.tag == "cpt":
                for cpt in child.text.split(','):
                    cpts.add(cpt)
        
        for hardtype in hardtypes:
            if not boardDict.has_key(hardtype):
                boardDict[hardtype] = {
                    'boardtype': boardtype,
                    'cpts':set(), 
                    'hardtype': hardtype, 
                    'cputype': cputype
                }
            # else: check compatibility
            for cpt in cpts:
                boardDict[hardtype]['cpts'].add(cpt)

def createPdtlist(xmlfile, boardDict):
    boards = ET.Element("boards")

    for hardtype, board in boardDict.items():
        boardNode = ET.SubElement(boards, "board")

        boardtypeNode = ET.SubElement(boardNode, "boardtype")
        boardtypeNode.text = board['boardtype']

        hardtypeNode = ET.SubElement(boardNode, "hardtype")
        hardtypeNode.text = board['hardtype']

        cputypeNode = ET.SubElement(boardNode, "cputype")
        cputypeNode.text = board['cputype']

        cptNode = ET.SubElement(boardNode, "cpt")
        cptNode.text = ','.join(board['cpts'])

    tree = ET.ElementTree(boards)
    tree.write(xmlfile)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "Usage:\n\t", sys.argv[0], " pdt_list_out.xml pdt_list_in1.xml pdt_list_in2.xml ..."

    boardDict = dict()
    for pdtlist in sys.argv[2:]:
        readPdtlist(pdtlist, boardDict)

    createPdtlist(sys.argv[1], boardDict)

