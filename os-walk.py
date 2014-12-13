import os

startDir = "/home/HDD/Documents/Programming/Languages/Python/os/"

for dirName, dirList, fileList in os.walk(startDir):
    print "in ", dirName, "you have these files:", fileList, "and these directories:", dirList
