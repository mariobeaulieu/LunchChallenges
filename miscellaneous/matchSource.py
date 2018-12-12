#!/usr/bin/python
import sys
import getopt
import os.path
import random

def usage():
    print """
    This program verifies that all data blocks found in destination files come from a source file.
    
    Usage: python matchSource.py [-v] [-h] <-b blockSize> <-s sourceFile> <-d destFile1> [-d destFile2 [-d destFile3 ... ]] [-c size]
    
    Required parameters are:
      -b blocksize  where blocksize is the size in bytes of each data block
      -s sourceFile where sourceFile is the name of the master file from where all data come from
      -d destFile   where destFile is the file name of a destination file that got data blocks from the source file
                    There can be as many destination files as needed
    Optional parameters are:
      -h            Prints this help and exits
      -v            Increments verbosity (use twice to max verbosity)
      -c size       is the option to generate test files, the source file being "size" bytes
                    and it creates 3 destination files: dest1, dest2, dest3
                    Those file names are hardcoded.
                    When this option is used, the program creates these 4 test files and exits.
"""    

        
def main():
    opts=[]
    try: opts, args = getopt.getopt(sys.argv[1:], "hs:d:vb:c:", ['help', 'source=', 'destination=', 'verbose', 'blocksize='])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
  
    nbDest=0
    src = None
    dest=[]
    bs=0
    err=0
    verbose=0
    
    for o, a in opts:
        if   o in ("-v", "--verbose"):
            verbose+=1
        elif o in ("-b", "--blocksize"):
            if a>0:
                bs=int(a)
            else:
                print "<",a,"> is not a value >0 for block size"
                err=1
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-d","--destination"):
            if os.path.isfile(a):
                dest.append(a)
                nbDest+=1
            else:
                print "<",a,"> is not a binary file to read as destination"
                err=1
        elif o in ("-s", "--source"):
            if os.path.isfile(a):
                src=a
            else:
                print "<",a,"> is not a binary file to use as source"
                err=1
        elif o=='-c':
            srcSize=int(a)
            print "Creating test data files of ",srcSize," bytes"
            if bs==0:
                print "Please set block size first"
                sys.exit(2)
            count=0
            c=0
            s=open("source", "wb")
            f=[]
            f.append(open("dest1", "wb"))
            f.append(open("dest2", "wb"))
            f.append(open("dest3", "wb"))
            while count<srcSize:
                if count*10/srcSize > c:
                    c=count*10//srcSize
                    print c*10,"%"
                n=random.randrange(0,4)
                if n==3:
                    # Discarded byte
                    v=[random.randrange(0,256)]
                    s.write(bytearray(v))
                    count+=1
                else:
                    v=[random.randrange(0,256) for i in range(bs)]
                    f[n].write(bytearray(v))
                    s.write(bytearray(v))
                    count+=bs
            print "File <source> now contains ",count," bytes that have been distributed in files dest1, dest2, and dest3 in blocks of ",bs," bytes."
            sys.exit(0)
        else:
            assert False, "Invalid option"
            
    if nbDest == 0:
        print "You need to specify at least 1 destination file (option -d)"
        err=1
    if src == None:
        print "You need to specify the source file (option -s)"
        err=1
    if bs == 0:
        print "You need to specify a block size >0 (option -b)"
        err=1
    if err == 1:
        usage()
        sys.exit(1)
    
    if verbose != 0:
        print "Opening source file ", src
    try:
        src_fd = open(src, 'rb')
    except:
        print "Error opening source file <",src,">"
        sys.exit(1)
        
    dest_fd=[]
    destCount=0
    for d in dest:
        if verbose != 0:
            print "Opening destination file ", d
        try:
            dest_fd.append(open(d, 'rb'))
            destCount+=1
        except:
            print "Error opening destination file <",d,">"
            sys.exit(1)
    print destCount," destination files were opened"

    srcData=bytes()
    # Read a block from source
    try:
        srcData = src_fd.read(bs)
        if len(srcData) < bs:
            print "FAIL -- End of file reached while reading the source file"
            sys.exit(1)
    except:
        print sys.exc_info()
        sys.exit(1)
    
    # Read a block from each destination file
    dstData=[]
    doneFlag=[]
    dstHits=[]
    doneCount=0
    totalHits=0
    for n in range(nbDest):
        # Each destination has a doneFlag to indicate when it's completed
        doneFlag.append(False)
        # Initialize dst_data[n]
        dstData.append('')
        # Read bs values from the destination file
        try:
            dstData[n] = dest_fd[n].read(bs)
            if len(dstData[n]) < bs:
                doneFlag[n]=True
                doneCount+=1
                print "Done with dest file ", dest[n]
                if verbose>1:
                    print "New dest data is <",dstData[n],">"
        except:
            print sys.exc_info()
            sys.exit(1)
        # Also have a count of hits for each data file
        dstHits.append(0)
    
    # Now we should have bs bytes from the source and bs bytes from each dest file
    # Match data from files until all dest files are matched (i.e. until doneCount == nbDest)
    while doneCount < nbDest:
        matchFound=False
        for n in range(nbDest):
            if not doneFlag[n]:
                if dstData[n] == srcData:
                    matchFound=True
                    dstHits[n]+=1
                    totalHits+=1
                    if verbose>1:
                        print "Just got a hit for dest file ",dest[n]
                        print "Src=<",srcData,">"
                        print "Dst=<",dstData[n],">"
                    try:
                        dstData[n] = dest_fd[n].read(bs)
                        if len(dstData[n]) < bs:
                            doneFlag[n]=True
                            doneCount+=1
                            print "Done with dest file ", dest[n]
                            if doneCount == nbDest:
                                print "Done with ",doneCount," files out of ",nbDest
                                break
                            if verbose>1:
                                print "New dest data is <",dstData[n],">"
                    except:
                        print sys.exc_info()
                        sys.exit(1)
                    
                    if verbose>1:
                        print "Reading ",bs," bytes from the source file"
                    try:
                        srcData = src_fd.read(bs)
                        if len(srcData) < bs:
                            print "FAIL -- End of file reached while reading the source file"
                            sys.exit(1)
                    except:
                        print sys.exc_info()
                        sys.exit(1)
                    
                    break
                
        if matchFound == False:
            # Read 1 byte from the source
            try:
                d = src_fd.read(1)
                if len(d) == 0:
                    print "FAIL -- End of file reached while reading the source file"
                    sys.exit(1)
            except:
                print sys.exc_info()
                sys.exit(1)
            srcData = srcData[1:]+d
            
    print "All done!"
    for d in range(nbDest):
        print "Got ",dstHits[d]," hits for file ",dest[d]
    print "for a total of ",totalHits," hits (=", totalHits*bs, " bytes)"
    
main()