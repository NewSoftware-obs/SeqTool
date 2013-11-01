#!/usr/bin/env python
# output a randomly selected sequences from a fasta file
import sys,re,os;
import random;
import myfunc;

BLOCK_SIZE=100000;

usage="""
Usage:  randfasta.py [-i] fastafile  [-n INT ] 
output a randomly selected sequences from a fasta file 
Options:
  -i    FILE  Input file
  -n     INT  Output n sequences instead of all
  -seed  INT  Set random seed, default is set by time
  -o    FILE  Outputfile
  -bs|--block-size INT  
              Size for blocks when reading file, (default: 100000)
  -h|--help             Print this help message and exit
Created 2011-04-08, updated 2011-10-31, Nanjiang
"""

def PrintHelp():
    print usage;

def RandFasta(inFile,N,rand_seed, fpout):#{{{
    (idList,annotationList, seqList)=myfunc.ReadFasta(inFile, BLOCK_SIZE);
    if idList == None:
        print >> sys.stderr, "Failed to read fastafile %s. Exit."%inFile;
        return -1;
    random.seed(rand_seed);
    Nseq=len(idList);
    if N > Nseq:
        N=Nseq;
    idxArray=range(Nseq);
    idxSample=random.sample(idxArray,N);
    for i in xrange(N):
        idx = idxSample[i];
        fpout.write(">%s\n"% annotationList[idx]);
        fpout.write("%s\n"% seqList[idx]);
    return 0;
#}}}

def main():#{{{
    numArgv=len(sys.argv)
    if numArgv < 2:
        PrintHelp();
        sys.exit(1);

    outFile="";
    inFile="";
    N=999999999;
    rand_seed=None;

    i = 1;
    isNonOptionArg=False
    while i < numArgv:
        if isNonOptionArg == True:
            isNonOptionArg=False;
            i = i + 1;
        elif sys.argv[i] == "--":
            isNonOptionArg=True;
            i = i + 1;
        elif sys.argv[i][0] == "-":
            if sys.argv[i] ==  "-h" or  sys.argv[i] == "--help":
                PrintHelp();
                sys.exit(0);
            elif sys.argv[i] == "-i" or sys.argv[i] == "--infile":
                inFile=sys.argv[i+1];
                i = i + 2;
            elif sys.argv[i] == "-n" or sys.argv[i] == "--n":
                N=int(sys.argv[i+1]);
                i = i + 2;
            elif sys.argv[i] == "-seed" or sys.argv[i] == "--seed":
                rand_seed=int(sys.argv[i+1]);
                i = i + 2;
            elif sys.argv[i] == "-o" or sys.argv[i] == "--outfile":
                outFile=sys.argv[i+1];
                i = i + 2;
            elif sys.argv[i] == "-bs" or sys.argv[i] == "--block-size" or sys.argv[i] == "-block-size":
                BLOCK_SIZE=int(sys.argv[i+1]);
                if BLOCK_SIZE < 0:
                    print >> sys.stderr,"Error! BLOCK_SIZE should >0";
                    sys.exit(1);
                i = i + 2;
            else:
                print >> sys.stderr,("Error! Wrong argument:%s" % sys.argv[i]);
                sys.exit(1);
        else:
            inFile=sys.argv[i];
            i+=1;

    if inFile == "" :
        print >> sys.stderr,"Error! Input file not set.";
        return -1;
    elif not os.path.exists(inFile):
        print >> sys.stderr,"Error! Input file %s does not exist. Exit."%inFile;
        return -1;


    fpout = sys.stdout;
    if outFile != "":
        fpout = open(outFile,"w");
        if fpout == None:
            print >> sys.stderr, "Failed to write to file %s. Force to stdout."%outFile;
            fpout = sys.stdout;

    RandFasta(inFile, N, rand_seed,  fpout);

    if fpout != None and fpout != sys.stdout:
        fpout.close();
#}}}
if __name__ == '__main__' :
    # Check argv
    main();
