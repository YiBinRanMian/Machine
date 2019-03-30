//
// Created by Harod Finvh on 2019/3/16.
//
#include <set>
#include <string>
#include <ptree.h>

set<string> oneTerminal;
set<string>::iterator it;
char *pyin;
Tree *root;
map<int,string> id2name;
int previousL = 0;
map<string,int> name2id;
void remendFile(const char * fn,int mode);
std::string formString(vector<string> &wordlist);
void gPtree(Tree *t,ifstream& in);
void getCurrentNodes(const char *f,set<string> &set1);
char * sToC(std::string s);
int getLevelandWords(char *buffer,vector<string> &wordlist);

int pyparser(){
    id_init();
    const char * onet = const_cast<char *>("oneTerminal.txt");
    getCurrentNodes(onet,oneTerminal);
    if(pyin ==NULL){
        cout<<"error"<<endl;
        return 0;
    }
    remendFile(pyin,0);
    remendFile(pyin,1);
    remendFile(pyin,2);

    ifstream infile(pyin);
    char buffer[256];
    std::vector<std::string> words;
    infile.getline(buffer, 255);
    int level = getLevelandWords(buffer,words);
    root = new NonTerminal(name2id[words[0]],level);
    gPtree(root,infile);
    return 1;
}

void remendFile(const char * fn,int mode){
    typedef multimap <int,std::vector<std::string> > IntVectorMap;
    FILE *f = nullptr;
    f = fopen(fn,"r");
    if(!f){
        cout<<"Can not open file for f: "<<fn<<endl;
        return;
    }
    ifstream infile(fn);
    std::vector<int> levelList;
    IntVectorMap lw;
    while(!infile.eof()) {
        char buffer[256];
        infile.getline(buffer, 255);
        std::vector<std::string> words;
        levelList.push_back(getLevelandWords(buffer,words));
        lw.insert(make_pair(levelList.size()-1,words));
    }
    if(mode==0){
        int offset=0;
        for (int i=0;i<levelList.size();i++) {
            IntVectorMap::iterator it = lw.find(i);
            if(it->second.size()==2 and it->second[0]!="keyword"){
                string extraNode = it->second[1];
                it->second.pop_back();
                vector<std::string> extraString;
                extraString.push_back(extraNode);
                lw.insert(make_pair(i,extraString));
                levelList.insert(levelList.begin()+i+1+offset,levelList[i+offset]+1);

                for (int j = i+offset+2; levelList[j] >levelList[i+offset] ; ++j) {
                    levelList[j]+=1;
                }
                offset++;
            }
        }
    }else if(mode==1){
        int offset=0;
        for (int i=0;i<levelList.size();i++) {
            IntVectorMap::iterator it = lw.find(i);
            if(it->second.size()>=4 and it->second[1]=="T"){
                int len = it->second.size();
                vector<std::string> extraString;
                for (int j = 1; j < len; ++j) {
                    extraString.push_back(it->second[j]);
                }
                for (int k = 1; k < len; ++k) {
                    it->second.pop_back();
                }
                lw.insert(make_pair(i,extraString));
                levelList.insert(levelList.begin()+i+1+offset,levelList[i+offset]+1);
                offset++;
            }
        }
    }else if(mode==2){
        int offset=0;
        int slevelList = levelList.size();
        for (int i=0;i<slevelList;i++) {
            IntVectorMap::iterator it = lw.find(i);
            if(it->second.size()>=5 and it->second[1]=="Name"){
                int len = it->second.size();
                vector<std::string> extraString;
                for (int j = 4; j < len; ++j) {
                    extraString.push_back(it->second[0]);
                    extraString.push_back(it->second[1]);
                    extraString.push_back(it->second[2]);
                    extraString.push_back(it->second[j]);
                    lw.insert(make_pair(i,extraString));
                    extraString.clear();
                    levelList.insert(levelList.begin()+i+1+offset,levelList[i+offset]);
                    offset++;
                }
                for (int k = 4; k < len; ++k) {
                    it->second.pop_back();
                }
                i+=offset;
            }
        }
    }

    int k =0;
    ofstream fout(fn);
    IntVectorMap::iterator pos;
    pos = lw.begin();
    while(pos!=lw.end()){
        fout<<levelList[k];
        for (int i = 0; i < pos->second.size(); ++i) {
            fout<<" "<<pos->second[i];
        }
        ++pos;
        k++;
        if(pos!=lw.end())
            fout<<endl;

    }

    fout.close();
}

std::string formString(vector<string> &wordlist){
    int len = wordlist.size();
    std::string s="";
    int i=3;
    while(i!=len-1){
        s.append(wordlist[i]+" ");
        i++;
    }
    s.append(wordlist[len-1]);
    s.erase(s.length()-1,1);
    s.erase(0,1);
    return s;
}

void gPtree(Tree *t,ifstream& in){
    if(!in.eof()){
        char buffer[256];
        in.getline(buffer, 255);
        std::vector<std::string> words;
        int tLevel = getLevelandWords(buffer,words);
        if(tLevel>t->level){
            if(words.size()==1){
                if(t->type== name2id["Alias"]) {
                    char *temp = sToC(words[0]);
#ifdef DEBUG
                    cout<<words[0]<<endl;
                    cout<<temp<<endl;
#endif
                    Terminal *node = new Terminal(name2id["Alias"],temp,previousL,tLevel);
                    t->addChild(node);
                    node->parent = t;
                    gPtree(node,in);
                }
                else{
                    it = oneTerminal.find(words[0]);
                    if(it == oneTerminal.end()){
                        NonTerminal *node = new NonTerminal(name2id[words[0]], tLevel);
                        t->addChild(node);
                        node->parent = t;
                        gPtree(node, in);
                    }else{
                        char *temp = sToC(words[0]);
#ifdef DEBUG
                        cout<<words[0]<<endl;
                        cout<<temp<<endl;
#endif
                        Terminal *node = new Terminal(name2id[words[0]],temp,previousL,tLevel);
                        t->addChild(node);
                        node->parent = t;
                        gPtree(node,in);
                    }
                }
            }else if(words.size()==2){
                if(words[0]=="keyword"){
                    char* temp = sToC(words[1]);
#ifdef DEBUG
                    cout<<words[1]<<endl;
                    cout<<temp<<endl;
#endif
                    NonTerminal *node = new NonTerminal(name2id[words[0]],tLevel);
                    Terminal *node1 = new Terminal(name2id["Keyword"],temp,previousL,tLevel+1);
                    node->addChild(node1);
                    node1->parent = node;
                    t->addChild(node);
                    node->parent= t;
                    gPtree(node,in);
                }
            }
            else if(words.size()==3){
                if(words[1]=="Str"){
                    char *temp = sToC("");
#ifdef DEBUG
                    cout<<""<<endl;
                    cout<<temp<<endl;
#endif
                    Terminal *node = new Terminal(name2id[words[1]],temp,atoi(words[2].c_str()),tLevel);
                    previousL = atoi(words[2].c_str());
                    t->addChild(node);
                    node->parent = t;
                    gPtree(node,in);
                }else{
/*                    it = threeTerminal.find(words[1]);
                    if(it == threeTerminal.end())
                        threeTerminal.insert(words[1]);*/
                    char *temp=sToC(words[1]);
#ifdef DEBUG
                    cout<<words[1]<<endl;
                    cout<<temp<<endl;
#endif
                    Terminal *node = new Terminal(name2id[words[1]],temp,atoi(words[2].c_str()),tLevel);
                    previousL = atoi(words[2].c_str());
                    t->addChild(node);
                    node->parent = t;
                    gPtree(node,in);
                }
            }else if(words.size()==4){
/*                it = fourTerminal.find(words[1]);
                if(it == fourTerminal.end())
                    fourTerminal.insert(words[1]);*/
                if(words[3].at(0)=='\''){
                    words[3].erase(words[3].length()-1,1);
                    words[3].erase(0,1);
                }
                char *temp = sToC(words[3]);
#ifdef DEBUG
                cout<<words[3]<<endl;
                cout<<temp<<endl;
#endif
                if(words[1]=="ClassDef" || words[1]=="FunctionDef" || words[1]=="ImportFrom" || words[1]=="Name" ||words[1]=="arg"){
                    Terminal *node = new Terminal(name2id["IDENTIFIER"],temp,atoi(words[2].c_str()),tLevel);
                    previousL = atoi(words[2].c_str());
                    t->addChild(node);
                    node->parent = t;
                    gPtree(node,in);
                }else{
                    Terminal *node = new Terminal(name2id[words[1]],temp,atoi(words[2].c_str()),tLevel);
                    previousL = atoi(words[2].c_str());
                    t->addChild(node);
                    node->parent = t;
                    gPtree(node,in);
                }
            }
            else if(words.size()>=5){
                if(words[1]=="Str"){
                    char *temp = sToC(formString(words));
#ifdef DEBUG
                    cout<<formString(words)<<endl;
                    cout<<temp<<endl;
#endif
                    Terminal *node = new Terminal(name2id[words[1]],temp,atoi(words[2].c_str()),tLevel);
                    previousL = atoi(words[2].c_str());
                    t->addChild(node);
                    node->parent = t;
                    gPtree(node,in);
                }
            }
        }else if(tLevel==t->level){
            if(words.size()==1){
                if(t->type== name2id["alias"]) {
                    char *temp = sToC(words[0]);
#ifdef DEBUG
                    cout<<words[0]<<endl;
                    cout<<temp<<endl;
#endif
                    Terminal *node = new Terminal(name2id["alias"],temp,previousL,tLevel);
                    t->nextSibbling = node;
                    node->parent = t->parent;
                    (t->parent)->addChild(node);
                    gPtree(node,in);
                }
                else{
                    it = oneTerminal.find(words[0]);
                    if(it == oneTerminal.end()){
                        NonTerminal *node = new NonTerminal(name2id[words[0]], tLevel);
                        t->nextSibbling = node;
                        node->parent = t->parent;
                        (t->parent)->addChild(node);
                        gPtree(node, in);
                    }else{
                        char *temp = sToC(words[0]);
#ifdef DEBUG
                        cout<<words[0]<<endl;
                        cout<<temp<<endl;
#endif
                        Terminal *node = new Terminal(name2id[words[0]],temp,previousL,tLevel);
                        t->nextSibbling = node;
                        node->parent = t->parent;
                        (t->parent)->addChild(node);
                        gPtree(node,in);
                    }
                }
            }
            else if(words.size()==2){
                if(words[0]=="keyword"){
                    char* temp = sToC(words[1]);
#ifdef DEBUG
                    cout<<words[1]<<endl;
                    cout<<temp<<endl;
#endif
                    NonTerminal *node = new NonTerminal(name2id[words[0]],tLevel);
                    Terminal *node1 = new Terminal(name2id["Keyword"],temp,previousL,tLevel+1);
                    node->addChild(node1);
                    node1->parent = node;
                    t->nextSibbling = node;
                    node->parent= t->parent;
                    (t->parent)->addChild(node);
                    gPtree(node,in);
                }
            }
            else if(words.size()==3){
                if(words[1]=="Str"){
                    char *temp = sToC("");
#ifdef DEBUG
                    cout<<""<<endl;
                    cout<<temp<<endl;
#endif
                    Terminal *node = new Terminal(name2id[words[1]],temp,atoi(words[2].c_str()),tLevel);
                    previousL = atoi(words[2].c_str());
                    t->nextSibbling = node;
                    node->parent = t->parent;
                    (t->parent)->addChild(node);
                    gPtree(node,in);
                }else {
/*                        it = threeTerminal.find(words[1]);
                        if(it == threeTerminal.end())
                            threeTerminal.insert(words[1]);*/
                    char *temp = sToC(words[1]);
#ifdef DEBUG
                    cout<<words[1]<<endl;
                    cout<<temp<<endl;
#endif
                    Terminal *node = new Terminal(name2id[words[1]], temp, atoi(words[2].c_str()), tLevel);
                    previousL = atoi(words[2].c_str());
                    t->nextSibbling = node;
                    node->parent = t->parent;
                    (t->parent)->addChild(node);
                    gPtree(node, in);
                }
            }else if(words.size()==4){
/*                it = fourTerminal.find(words[1]);
                if(it == fourTerminal.end())
                    fourTerminal.insert(words[1]);*/
                if(words[3].at(0)=='\'') {
                    words[3].erase(words[3].length() - 1, 1);
                    words[3].erase(0, 1);
                }
                char *temp = sToC(words[3]);
#ifdef DEBUG
                cout<<words[3]<<endl;
                cout<<temp<<endl;
#endif
                if(words[1]=="ClassDef" || words[1]=="FunctionDef" || words[1]=="ImportFrom" || words[1]=="Name" ||words[1]=="arg"){
                    Terminal *node = new Terminal(name2id["IDENTIFIER"],temp,atoi(words[2].c_str()),tLevel);
                    previousL = atoi(words[2].c_str());
                    t->nextSibbling = node;
                    node->parent = t->parent;
                    (t->parent)->addChild(node);
                    gPtree(node,in);
                }else{
                    Terminal *node = new Terminal(name2id[words[1]],temp,atoi(words[2].c_str()),tLevel);
                    previousL = atoi(words[2].c_str());
                    t->nextSibbling = node;
                    node->parent = t->parent;
                    (t->parent)->addChild(node);
                    gPtree(node,in);
                }
            }
            else if(words.size()>=5){
                if(words[1]=="Str"){
                    char *temp = sToC(formString(words));
#ifdef DEBUG
                    cout<<formString(words)<<endl;
                    cout<<temp<<endl;
#endif
                    Terminal *node = new Terminal(name2id[words[1]],temp,atoi(words[2].c_str()),tLevel);
                    previousL = atoi(words[2].c_str());
                    t->nextSibbling = node;
                    node->parent = t->parent;
                    (t->parent)->addChild(node);
                    gPtree(node,in);
                }
            }
        }else{
            while(tLevel<t->level){
                t = t->parent;
            }

            if(words.size()==1){
                it = oneTerminal.find(words[0]);
                if(it == oneTerminal.end()){
                    NonTerminal *node = new NonTerminal(name2id[words[0]], tLevel);
                    t->nextSibbling = node;
                    node->parent = t->parent;
                    (t->parent)->addChild(node);
                    gPtree(node, in);
                }else{
                    char *temp = sToC(words[0]);
#ifdef DEBUG
                    cout<<words[0]<<endl;
                    cout<<temp<<endl;
#endif
                    Terminal *node = new Terminal(name2id[words[0]],temp,previousL,tLevel);
                    t->nextSibbling = node;
                    node->parent = t->parent;
                    (t->parent)->addChild(node);
                    gPtree(node,in);
                }
            }
            else if(words.size()==2){
                if(words[0]=="keyword"){
                    char* temp = sToC(words[1]);
#ifdef DEBUG
                    cout<<words[1]<<endl;
                    cout<<temp<<endl;
#endif
                    NonTerminal *node = new NonTerminal(name2id[words[0]],tLevel);
                    Terminal *node1 = new Terminal(name2id["Keyword"],temp,previousL,tLevel+1);
                    node->addChild(node1);
                    node1->parent = node;
                    t->nextSibbling = node;
                    node->parent= t->parent;
                    (t->parent)->addChild(node);
                    gPtree(node,in);
                }
            }
            else if(words.size()==3){
                if(words[1]=="Str"){
                    char *temp = sToC("");
#ifdef DEBUG
                    cout<<""<<endl;
                    cout<<temp<<endl;
#endif
                    Terminal *node = new Terminal(name2id[words[1]],temp,atoi(words[2].c_str()),tLevel);
                    previousL = atoi(words[2].c_str());
                    t->nextSibbling = node;
                    node->parent = t->parent;
                    (t->parent)->addChild(node);
                    gPtree(node,in);
                }else {
//                    it = threeTerminal.find(words[1]);
//                    if(it == threeTerminal.end())
//                        threeTerminal.insert(words[1]);
                    char *temp = sToC(words[1]);
#ifdef DEBUG
                    cout<<words[1]<<endl;
                    cout<<temp<<endl;
#endif
                    Terminal *node = new Terminal(name2id[words[1]], temp, atoi(words[2].c_str()), tLevel);
                    previousL = atoi(words[2].c_str());
                    t->nextSibbling = node;
                    node->parent = t->parent;
                    (t->parent)->addChild(node);
                    gPtree(node, in);
                }
            }else if(words.size()==4){
//                it = fourTerminal.find(words[1]);
//                if(it == fourTerminal.end())
//                    fourTerminal.insert(words[1]);
                if(words[3].at(0)=='\'') {
                    words[3].erase(words[3].length() - 1, 1);
                    words[3].erase(0, 1);
                }
                char *temp = sToC(words[3]);
#ifdef DEBUG
                cout<<words[3]<<endl;
                cout<<temp<<endl;
#endif
                if(words[1]=="ClassDef" || words[1]=="FunctionDef" || words[1]=="ImportFrom" || words[1]=="Name" ||words[1]=="arg"){
                    Terminal *node = new Terminal(name2id["IDENTIFIER"],temp,atoi(words[2].c_str()),tLevel);
                    previousL = atoi(words[2].c_str());
                    t->nextSibbling = node;
                    node->parent = t->parent;
                    (t->parent)->addChild(node);
                    gPtree(node,in);
                }else{
                    Terminal *node = new Terminal(name2id[words[1]],temp,atoi(words[2].c_str()),tLevel);
                    previousL = atoi(words[2].c_str());
                    t->nextSibbling = node;
                    node->parent = t->parent;
                    (t->parent)->addChild(node);
                    gPtree(node,in);
                }
            }
            else if(words.size()>=5){
                if(words[1]=="Str"){
                    char *temp = sToC(formString(words));
#ifdef DEBUG
                    cout<<formString(words)<<endl;
                    cout<<temp<<endl;
#endif
                    Terminal *node = new Terminal(name2id[words[1]],temp,atoi(words[2].c_str()),tLevel);
                    previousL = atoi(words[2].c_str());
                    t->nextSibbling = node;
                    node->parent = t->parent;
                    (t->parent)->addChild(node);
                    gPtree(node,in);
                }
            }
        }
    }
}

void getCurrentNodes(const char *f,set<string> &set1){
    char buffer[256];
    ifstream in(f);
    while(in.getline(buffer, 255)) {
        string string1(buffer);
        set1.insert(string1);
    }
}

char * sToC(std::string s){
    char * temp;
    int len = s.length();
    temp = new char[len+1];
//    temp = (char*)malloc((len+1)* sizeof(char));
    strcpy(temp,s.c_str());
//    s.copy(temp,len,0);
    return temp;
}

int getLevelandWords(char *buffer,vector<string> &wordlist){
    int index = 0;
    int level = 0;
    char *tokenPtr = strtok(buffer," ");
    while(tokenPtr!= nullptr){
        if(index == 0){
            level = atoi(tokenPtr);
        }else{
            wordlist.push_back(tokenPtr);
        }
        index++;
        tokenPtr = strtok(NULL," ");
    }
    return level;
}