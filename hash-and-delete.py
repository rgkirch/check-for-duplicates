# Written by Richard Kirchofer.

# How to hash a file.
# http://www.pythoncentral.io/finding-duplicate-files-with-python/
# A function to convert bytes into something more readable.
# http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size

import os
import sys
import hashlib

# os.makedirs(dir) to make a dir
# os.stat(path).st_size for file size
# os.remove(path)
# os.rename(path)
# hashfile source
# http://www.pythoncentral.io/finding-duplicate-files-with-python/

# returns the file hash as hex
# path <str>, blocksize <int>
def hashfile(path, blocksize = 65536):
    infile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = infile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = infile.read(blocksize)
    infile.close()
    return hasher.hexdigest()


# http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


 #***********code above here can be considered golden

# returns a string that is the dir to use
def choose_root_directory():
    print "default dir is current dir (./)"
    raw = raw_input("enter alternate dir: ")
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

# we want to make sure that the input is valid (not out of range)
# also, if they choose to delete all then make sure they really intend to delete all
# uses: check_inputs_in_range()
# input_variable_type <str>, length <int>
def duplicate_check_input_dialogue(length):
    while True:
        ones_to_delete = [int(x) for x in raw_input("Enter the numbers of the ones that you want to mark for deletion separated by spaces.\n").strip().split()]

        if not ones_to_delete:
            print "You didn't enter anything. Skipping..."
            return []

        if not check_inputs_in_range(ones_to_delete, length):
            print "Your input was invalid."
            continue

        if len(ones_to_delete) == length:
            are_you_sure = raw_input("You have selected to delete all of the files. Are you sure you want to do this?\n (y/n) ")
            # print type(are_you_sure)
            if are_you_sure != "y":
                continue

        return ones_to_delete

# returns false if any of the inputs were invalid
def check_inputs_in_range(ones_to_delete, length):
    for x in ones_to_delete:
        if int(x) > int(length)-1:
            print "Your inputs must be less than", length, "."
            return False
        elif int(x) < 0:
            print "Your inputs must be greater than 0."
            return False
    return True

def print_list_of_dir_tups(list_of_dirs_tups):
    if not list_of_dirs_tups:
        return
    max_level = len(list_of_dirs_tups[0])
    for item in list_of_dirs_tups:
        if len(item) < max_level:
            max_level = len(item)

        fname = os.path.join(item[0], item[1])
        fname = fname.split('/')

        # print index, fname, os.stat(fname).st_size


if __name__ == '__main__':
    root_directory = choose_root_directory()
    all_hashes_once = {}
    all_duplicates = {}
    duplicate_size = 0
    duplicate_count = 0

#########################################
# walk through the dirs, hash the files #
#########################################

    # os.walk will return a tuple
    # you may modify os.walk()[1] to change which dirs it decends into
    for current_dir, dirs_in_current_dir, files_in_current_dir in os.walk(root_directory):
        print "checking", current_dir
        # exclude dirs that begin with a period
        dirs_in_current_dir[:] = [x for x in dirs_in_current_dir if not x[0] == "."]

        # hash the paths and add it to all_hashes_once if it's new or to all_duplicates if it's a duplicate
        # the files are stored as tuples of the dir and file name
        for file_name in files_in_current_dir:
            path = os.path.join(current_dir, file_name)
            file_hash = hashfile(path)

            if file_hash in all_hashes_once:
                size = int(os.stat(path).st_size)
                duplicate_size += size
                duplicate_count += 1
                print ">", sizeof_fmt(size), "\t", file_name
                # add the thing to the right list
                if file_hash in all_duplicates:
                    all_duplicates[file_hash].append((current_dir, file_name))
                else:
                    all_duplicates[file_hash] = [all_hashes_once[file_hash], (current_dir, file_name)]
            else:
                all_hashes_once[file_hash] = (current_dir, file_name)

    print "Found", duplicate_count, "duplicate file(s). Duplicate space", sizeof_fmt(duplicate_size)

##################################################################
# print each set of duplicate files, choose which ones to delete #
##################################################################

    if not all_duplicates:
        print "No duplicate files found."
    else:
        # for each duplicate file
        for hash_value in all_duplicates:
            files_to_delete = []
            print "\nduplicate hash", hash_value
            duplicate_file_list = all_duplicates[hash_value]

            print_list_of_dir_tups(duplicate_file_list)
            indicies_for_deletion = duplicate_check_input_dialogue(len(duplicate_file_list))

            if not indicies_for_deletion:
                continue

            indicies_for_deletion.sort()
            for index in range(len(duplicate_file_list)):
                if indicies_for_deletion and index == indicies_for_deletion[0]:
                    files_to_delete.append(duplicate_file_list[indicies_for_deletion.pop(0)])

                print "\nThis will keep:"
                for x in duplicate_file_list:
                    if x not in files_to_delete:
                        print x
                print "\nThis will delete:"
                for x in files_to_delete:
                    print x
                print "Is this correct?"
                response = raw_input("[return] to accept (anything else to skip)")
                if response:
                    print "skip"
                else:
                    for x in files_to_delete:
                        print "deleting", x

prompt = raw_input("done")








