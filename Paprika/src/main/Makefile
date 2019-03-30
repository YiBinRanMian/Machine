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

# '?=' gives environment variables (if any) higher priority than definitions in the file
# So, it would be easier to re-define DEBUGFLAGS to be '-g -pg' to enable debugging
DEBUGFLAGS?=-O3

TREEHEADER=../include/ptree.h
TREESRC=ptree.cc

#CTREEOBJS=ptreeC.o
#JTREEOBJS=ptreeJ.o
#PHPTREEOBJS=ptreePHP.o
PYTREEOBJS=ptreePY.o

#CVGENOBJS=${CTREEOBJS} ../vgen/treeTra/libvgen.a  # TODO: libvgen may also be language dependent, especially the parts that involve "contextual nodes" (e.g., bugfinding, context locating code)
# A better architecture would make 'vgen' language independent, put all language-dependent code into ptgen/ptree but provide a language-independent interface for accessing tree structures;
# 'bugfinding' (the buggy code scoring algorithm in particular) should also be language-independent, accessing language-dependent tree structures only through a language-independent interface.
#JVGENOBJS=${JTREEOBJS} ../vgen/treeTra/libvgen.a
#PHPVGENOBJS=${PHPTREEOBJS} ../vgen/treeTra/libvgen.a
PYVGENOBJS=${PYTREEOBJS} ../vgen/treeTra/libvgen.a

#COBJS=${CVGENOBJS} ../ptgen/gcc/gccptgen.a
#JOBJS=${JVGENOBJS} ../ptgen/java/javaptgen.a
#PHPOBJS=${PHPVGENOBJS} ../ptgen/php5/phpptgen.a
PYOBJS=${PYVGENOBJS} ../ptgen/python/pyptgen.a


#CHEADERS=../ptgen/gcc/crelevantNodes.h ../ptgen/gcc/catomicNodes.h ../ptgen/gcc/cparentNodes.h ../ptgen/gcc/ccontextualNodes.h
#JHEADERS=../ptgen/java/jrelevantNodes.h ../ptgen/java/jatomicNodes.h ../ptgen/java/jparentNodes.h ../ptgen/java/jcontextualNodes.h
#PHPHEADERS=../ptgen/php5/phprelevantNodes.h ../ptgen/php5/phpatomicNodes.h ../ptgen/php5/phpparentNodes.h ../ptgen/php5/phpcontextualNodes.h
PYHEADERS=../ptgen/python/pyrelevantNodes.h ../ptgen/python/pyatomicNodes.h ../ptgen/python/pyparentNodes.h ../ptgen/python/pycontextualNodes.h

CC=g++
CXX=g++ 
CPPFLAGS+=-I../include -I../vgen/treeTra
CFLAGS+=$(DEBUGFLAGS)
CXXFLAGS+=$(DEBUGFLAGS)
LDFLAGS+=$(DEBUGFLAGS)

#EXES=cvecgen jvecgen cbugfilters jbugfilters out2html \
#     phpvecgen phpbugfilters out2xml \
#     cParseTreeMain jParseTreeMain phpParseTreeMain
EXES=pyvecgen  pybugfilters out2html \
     out2xml \
       pyParseTreeMain

TARGET:${EXES}

#NOTE: this Makefile may not be good for parallel compilation,
#      because intermediate files may be overwritten.

#${CTREEOBJS}:${TREESRC} ${TREEHEADER}
#	$(CXX) -o $@ $(CXXFLAGS) $(CPPFLAGS) -c -DCLANG ${TREESRC}

${PYTREEOBJS}:${TREESRC} ${TREEHEADER}
	$(CXX) -o $@ $(CXXFLAGS) $(CPPFLAGS) -c -DPYTHON ${TREESRC}

#phpvecgen:${PHPOBJS} ${PHPHEADERS} main.cc
#	$(CXX) $(CXXFLAGS) $(CPPFLAGS) -c -DPHP main.cc
#	$(CXX) -o $@ $(LDFLAGS) main.o ${PHPOBJS}

pyvecgen:${PYOBJS} ${PYHEADERS} main.cc
	$(CXX) $(CXXFLAGS) $(CPPFLAGS) -c -DPYTHON main.cc
	$(CXX) -o $@ $(LDFLAGS) main.o ${PYOBJS}

#phpbugfilters:${PHPOBJS} ${PHPHEADERS} bugmain.cc
#	${CXX} ${CXXFLAGS} $(CPPFLAGS) -c -DPHP bugmain.cc
#	${CXX} ${LDFLAGS} -o $@ bugmain.o ${PHPOBJS}

pybugfilters:${PYOBJS} ${PYHEADERS} bugmain.cc
	${CXX} ${CXXFLAGS} $(CPPFLAGS) -c -DPYTHON bugmain.cc
	${CXX} ${LDFLAGS} -o $@ bugmain.o ${PYOBJS}

out2html:${PYOBJS} out2html.C  # don't matter to use COBJS or others
	${CXX} ${CXXFLAGS} $(CPPFLAGS) -o $@ out2html.C ${PYOBJS}

out2xml:${PYOBJS} out2xml.C  # don't matter to use COBJS or others
	${CXX} ${CXXFLAGS} $(CPPFLAGS) -o $@ out2xml.C ${PYOBJS}
	
#cParseTreeMain:${COBJS} ${CHEADERS} parseTreeMain.cc
#	${CXX} ${CXXFLAGS} $(CPPFLAGS) -DCLANG -o $@ parseTreeMain.cc ${COBJS}

#jParseTreeMain:${JOBJS} ${JHEADERS} parseTreeMain.cc
#	${CXX} ${CXXFLAGS} $(CPPFLAGS) -DJAVA -o $@ parseTreeMain.cc ${JOBJS}

#phpParseTreeMain:${PHPOBJS} ${PHPHEADERS} parseTreeMain.cc
#	${CXX} ${CXXFLAGS} $(CPPFLAGS) -DPHP -o $@ parseTreeMain.cc ${PHPOBJS}

pyParseTreeMain:${PYOBJS} ${PYHEADERS} parseTreeMain.cc
	${CXX} ${CXXFLAGS} $(CPPFLAGS) -DPYTHON -o $@ parseTreeMain.cc ${PYOBJS}

.PHONY: clean
clean:
	rm -f *.o ${EXES}

