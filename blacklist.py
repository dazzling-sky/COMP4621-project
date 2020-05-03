import sys

def in_black_list(serverhostname):
    f = open("blacklist.txt", "r")
    line = f.readline()

    while(line):
        if serverhostname == line.strip():
            return True
        
        line = f.readline()
    
    return False

