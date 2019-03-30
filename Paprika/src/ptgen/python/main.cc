#include <ptree.h>
using namespace std;

#define DEBUG

int main() {


    const char * fn = const_cast<char *>("sample23.txt");
    pyin = const_cast<char*>(fn);
    const char * fo = const_cast<char *>("sample23");
    pyparser();
    if ( root==NULL ) {
        cerr << "Error: no parse tree created for file: " << fn << endl;
        return 1;
    }
    root->printTok();
    return 0;
}