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

# which directory should we look in?
def which_dir():
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
# uses: inputs_out_of_range()
# input_variable_type <str>, length <int>
def duplicate_check_input_dialogue(input_variable_type, length):
    if input_variable_type == "int":
        ones_to_delete = [int(x) for x in raw_input("Enter the numbers of the ones that you want to mork for deletion separated by spaces.\n").strip().split()]

        if not ones_to_delete:
            print "You didn't enter anything. Skipping..."
            return []

        # remove the inputs that are out of range
        trim_inputs_out_of_range(ones_to_delete, length)

        # if it's empty because all were removed (because all were out of range)
        while not ones_to_delete:
            try_again = raw_input("All of your inputs were invalid. Do you want to try again?\n (y/n) ")
            if try_again == "y":
                ones_to_delete = [int(x) for x in raw_input("Re-enter the numbers of the ones that you want to delete separated by spaces.\n").strip().split()]
                inputs_out_of_range(ones_to_delete, length)
            else:
                print "Not going to try again. Skipping..."
                return []

        ## assuming that all in ones_to_delete are valid, if the length is equal then that means they are all marked for deletion
        if len(ones_to_delete) == length:
            first_pass = True
            delete_all = False
            # to move on you are either sure that you want to delete all of them or you have no longer selected all of them for deletion
            while not delete_all and len(ones_to_delete) == length:
                if not first_pass:
                    ones_to_delete = [int(x) for x in raw_input("Re-enter the numbers of the ones that you want to delete separated by spaces.\n").strip().split()]
                first_pass = False
                inputs_out_of_range(ones_to_delete, length)
                if len(ones_to_delete) == length:
                    are_you_sure = raw_input("You have selected to delete all of the files. Are you sure you want to do this?\n (y/n) ")
                    if are_you_sure == "y":
                        delete_all = True
    ## end if variable_type == "int"
    return ones_to_delete
    # elif

# removes the inputs that are out of range
def trim_inputs_out_of_range(ones_to_delete, length):
    ## I must work backwards because if I delete the thing at index 0 then what was as index 1 is now at index 0. This could then skip some values.
    # print range(len(ones_to_delete)-1, -1, -1)
    for x in range(len(ones_to_delete)-1, -1, -1):
        if int(ones_to_delete[x]) > int(length)-1:
            ones_to_delete.pop(x)
            print "Your inputs must be less than", length, "."
            # print "Your inputs must not be greater than", length, "."
        elif int(ones_to_delete[x]) < 0:
            ones_to_delete.pop(x)
            print "Your inputs must be greater than 0."
            # print "Your input must not be less than 0."

# returns false if any of the inputs were invalid
def check_inputs_out_of_range(ones_to_delete, length):
    for x in ones_to_delete:
        if int(x) > int(length)-1:
            print "Your inputs must be less than", length, "."
            return False
        elif int(x) < 0:
            print "Your inputs must be greater than 0."
            return False
    return True

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
                print ">", filename
                if file_hash in all_duplicates:
                    all_duplicates[file_hash].append(path)
                else:
                    all_duplicates[file_hash] = [all_hashes_once[file_hash], path]
            else:
                all_hashes_once[file_hash] = path

    # print all_hashes_once
    print "done checking"


    for hash_value in all_duplicates:
        print "duplicate hash", hash_value
        duplicate_file_list = all_duplicates[hash_value]
        for index, duplicate_file in enumerate(duplicate_file_list):
            print index, duplicate_file
        ones_to_delete = duplicate_check_input_dialogue("int", len(duplicate_file_list))
        if not ones_to_delete:
            continue
        ones_to_delete.sort()
        for index in range(len(duplicate_file_list)):
            if index == ones_to_delete[0]:
                print "delete", duplicate_file_list[index]
                ones_to_delete.pop(0)






