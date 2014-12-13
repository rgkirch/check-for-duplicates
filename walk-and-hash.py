import os
import sys
import hashlib

# os.makedirs(dir) to make a dir
# hashfile source
# http://www.pythoncentral.io/finding-duplicate-files-with-python/

def hashfile(path, blocksize = 65536):
    infile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = infile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = infile.read(blocksize)
    infile.close()
    return hasher.hexdigest()

def which_dir():
    print "default dir is current dir (./)"
    raw = raw_input("enter alternate dir:")
    if raw:
        if os.path.exists(str(raw)):
            print "path exists"
            return str(raw)
        elif os.access(os.path.dirname(str(raw)), os.W_OK):
            print "path does not exist but write privileges are given"
            return str(raw)
        else:
            print "error, invalid path"
            print "must have write privileges"
    else:
        print "using default dir (./)"
        return "./"

if __name__ == '__main__':
    startDir = which_dir()
    all_hashes_once = {}
    all_duplicates = {}
    for dirName, dirList, fileList in os.walk(startDir):
        print "checking", dirName
        for filename in fileList:
            # print filename
            path = os.path.join(dirName, filename)
            # file_hash = hashfile(dirName + "/" + filename)
            file_hash = hashfile(path)
            if file_hash in all_hashes_once:
                print "->", filename
                if file_hash in all_duplicates:
                    all_duplicates[file_hash].append(path)
                else:
                    all_duplicates[file_hash] = [all_hashes_once[file_hash], path]
            else:
                all_hashes_once[file_hash] = path

    # print all_hashes_once
    print "done checking"
    if all_duplicates:
        print "duplicates found"
    else:
        print "no duplicates found"

    print

    for hash_value in all_duplicates:
        for item in all_duplicates[hash_value]:
            print item
        print
    print

