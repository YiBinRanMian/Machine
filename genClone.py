import os,sys
import subprocess

def getString(l):
    s = ''
    for i in range(len(l)):
        s += str(l[i])+' '
    return s.rstrip()

def genclone(qpath,minT,strI,simI,disT):
    print("""
    ##################################################
    generating clone report:
    
    """)
    path = sys.path[0]+"/Paprika/scripts/clonedetect"
    config = open(path+'/config',"w")
    minTokens = getString(minT)
    stride = getString(strI)
    similarity = getString(simI)
    distance = getString(disT)
    s= """
    #
    # 
    # Copyright (c) 2007-2013, University of California / Singapore Management University
    #   Lingxiao Jiang         <lxjiang@ucdavis.edu> <lxjiang@smu.edu.sg>
    #   Ghassan Misherghi      <ghassanm@ucdavis.edu>
    #   Zhendong Su            <su@ucdavis.edu>
    #   Stephane Glondu        <steph@glondu.net>
    # All rights reserved.
    # 
    # Redistribution and use in source and binary forms, with or without
    # modification, are permitted provided that the following conditions are met:
    #     * Redistributions of source code must retain the above copyright
    #       notice, this list of conditions and the following disclaimer.
    #     * Redistributions in binary form must reproduce the above copyright
    #       notice, this list of conditions and the following disclaimer in the
    #       documentation and/or other materials provided with the distribution.
    #     * Neither the name of the University of California nor the
    #       names of its contributors may be used to endorse or promote products
    #       derived from this software without specific prior written permission.
    # 
    # THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    # ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    # WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    # DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
    # FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    # DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    # SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    # CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
    # OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    # OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
    # 
    #
    #############################################################
    # Configuration file for clone detection.
    #
    
    ############################################################ 
    # Often, need to change these common parameters:
    # - FILE_PATTERN : for source files in different languages
    # - SRC_DIR : the root directory containing the source files
    # - DECKARD_DIR : Where is the home directory of DECKARD
    # - clone detection parameters: c.f. DECKARD's paper
    #   -- MIN_TOKENS
    #   -- STRIDE
    #   -- SIMILARITY
    #
    # java, c, or php?
    FILE_PATTERN='*.txt' # used for the 'find' command
    # where are the source files?
    SRC_DIR='"""+qpath+"""'
    # where is Deckard?
    DECKARD_DIR='"""+os.path.join(sys.path[0]+"/Paprika")+"""'
    # clone parameters; refer to paper.
    MIN_TOKENS='"""+minTokens+"""'  # can be a sequence of integers
    STRIDE='"""+stride+"""'  # can be a sequence of integers
    SIMILARITY='"""+similarity+"""'  # can be a sequence of values <= 1
    #DISTANCE='"""+distance+"""'
    
    ###########################################################
    # Where to store result files?
    #
    # where to output generated vectors?
    VECTOR_DIR='"""+qpath+"""/vectors'
    # where to output detected clone clusters?
    CLUSTER_DIR='"""+qpath+"""/clusters'
    # where to output timing/debugging info?
    TIME_DIR='"""+qpath+"""/times'
    
    ##########################################################
    # where are several programs we need?
    #
    # where is the vector generator?
    VGEN_EXEC="$DECKARD_DIR/src/main"
    case $FILE_PATTERN in 
      *.txt )
        VGEN_EXEC="$VGEN_EXEC/pyvecgen" ;;
      * )
        echo "Error: invalid FILE_PATTERN: $FILE_PATTERN"
        VGEN_EXEC="$VGEN_EXEC/invalidvecgen" ;;
    esac
    # how to divide the vectors into groups?
    GROUPING_EXEC="$DECKARD_DIR/src/vgen/vgrouping/runvectorsort"
    # where is the lsh for vector clustering?
    CLUSTER_EXEC="$DECKARD_DIR/src/lsh/bin/enumBuckets"
    # how to post process clone groups?
    POSTPRO_EXEC="$DECKARD_DIR/scripts/clonedetect/post_process_groupfile"
    # how to transform source code html?
    SRC2HTM_EXEC=source-highlight 
    SRC2HTM_OPTS=--line-number-ref
    
    ############################################################
    # For parallel processing
    #
    # the maximal number of processes to be used (by xargs)
    # - 0 means as many as possible (upto xargs)
    MAX_PROCS=8
    
    ##################################################################
    # Some additional, internal parameters; can be ignored
    #
    # the maximal vector size for the first group; not really useful
    GROUPING_S='50'  # should be a single value
    #GROUPING_D
    #GROUPING_C
    
    """
    config.write(s)
    os.system("chmod u+x "+path+'/config')
    config.close()
    devNull = open(os.devnull, 'w')
    os.chdir(path)
    subprocess.call('./deckard.sh', stdout=devNull)
    # os.system('./deckard.sh')
    print("""
    Clone report generating succeed.
    see detains in ./clusters/post_clusters*
    
    """)