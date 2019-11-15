# Gerry M duplicate image finder/removal
import os
import sys
import hashlib
from collections import defaultdict
import io

def gethash (myfile):   # create the md5 hash - get the file in chunks and update the hash
                        # dude m once the entire file is read in the hash dude will compute the hash

    m = hashlib.md5()

    with open(myfile,'rb') as f: 
        for chunk in iter(lambda: f.read(8192), b''): 
            m.update(chunk)
    return(m.digest())
    
if __name__ == '__main__':
    hash_file = defaultdict(list) # group a sequence of key-value pairs into a dictionary of lists

#    for root, dirs, files in os.walk('c:\\users\\Student\\Pictures\\', topdown=False):
 #   print(sys.argv[0], sys.argv[1], "argv0 and 1")
    for root, dirs, files in os.walk(sys.argv[1], topdown=False):

        for pname in files:
            name = os.path.join(root, pname)
            md5_hash = gethash(name)
            ctime = os.stat(name).st_ctime
            hash_file[md5_hash].append((ctime, name)) # use the hash as the key and the create time, end as data

    for md5_hash, dict_pair in hash_file.items():
#        print(md5_hash, dict_pair)
        if len(dict_pair) == 1:     #if there is only 1 entry for the hash move on to the next one
            continue

    # Keep the oldest file between the duplicates.
        dict_pair = sorted(dict_pair)
        name = [data[1] for data in dict_pair]

    # list of files. The first in the list is kept, the others are
    # removed.
        print ("%s: %s" % (md5_hash, ','.join('"%s"' % n for n in name)))

        original = name.pop(0)
        for n in name:
            print ("%s->%s" % (n, original))
            print("Removing %s\n" % n)
#            os.remove(n)