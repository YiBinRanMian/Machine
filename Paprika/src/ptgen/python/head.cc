#include <map>
#include <string>

using namespace std;

extern map<string,int> name2id;
extern map<int,string> id2name;

void id_init()
{
name2id["AnnAssign_stmt"]= 0;
id2name[0]= "AnnAssign_stmt";
name2id["Assign_stmt"]= 1;
id2name[1]= "Assign_stmt";
name2id["Attribute"]= 2;
id2name[2]= "Attribute";
name2id["AugAssign_stmt"]= 3;
id2name[3]= "AugAssign_stmt";
name2id["BinOp"]= 4;
id2name[4]= "BinOp";
name2id["BoolOp"]= 5;
id2name[5]= "BoolOp";
name2id["Call_stmt"]= 6;
id2name[6]= "Call_stmt";
name2id["Compare"]= 7;
id2name[7]= "Compare";
name2id["ExceptHandler_stmt"]= 8;
id2name[8]= "ExceptHandler_stmt";
name2id["Expr"]= 9;
id2name[9]= "Expr";
name2id["For_stmt"]= 10;
id2name[10]= "For_stmt";
name2id["FunctionDef_stmt"]= 11;
id2name[11]= "FunctionDef_stmt";
name2id["GeneratorExp"]= 12;
id2name[12]= "GeneratorExp";
name2id["IfExp_stmt"]= 13;
id2name[13]= "IfExp_stmt";
name2id["If_stmt"]= 14;
id2name[14]= "If_stmt";
name2id["ImportFrom_stmt"]= 15;
id2name[15]= "ImportFrom_stmt";
name2id["Import_stmt"]= 16;
id2name[16]= "Import_stmt";
name2id["Index"]= 17;
id2name[17]= "Index";
name2id["Module"]= 18;
id2name[18]= "Module";
name2id["Return_stmt"]= 19;
id2name[19]= "Return_stmt";
name2id["Slice"]= 20;
id2name[20]= "Slice";
name2id["Subscript"]= 21;
id2name[21]= "Subscript";
name2id["UnaryOp"]= 22;
id2name[22]= "UnaryOp";
name2id["While_stmt"]= 23;
id2name[23]= "While_stmt";
name2id["alias"]= 24;
id2name[24]= "alias";
name2id["annotation"]= 25;
id2name[25]= "annotation";
name2id["args"]= 26;
id2name[26]= "args";
name2id["arguments"]= 27;
id2name[27]= "arguments";
name2id["bases"]= 28;
id2name[28]= "bases";
name2id["body"]= 29;
id2name[29]= "body";
name2id["comparators"]= 30;
id2name[30]= "comparators";
name2id["comprehension"]= 31;
id2name[31]= "comprehension";
name2id["decorator_list"]= 32;
id2name[32]= "decorator_list";
name2id["defaults"]= 33;
id2name[33]= "defaults";
name2id["elt"]= 34;
id2name[34]= "elt";
name2id["elts"]= 35;
id2name[35]= "elts";
name2id["exc"]= 36;
id2name[36]= "exc";
name2id["func"]= 37;
id2name[37]= "func";
name2id["generators"]= 38;
id2name[38]= "generators";
name2id["handlers"]= 39;
id2name[39]= "handlers";
name2id["iter"]= 40;
id2name[40]= "iter";
name2id["keys"]= 41;
id2name[41]= "keys";
name2id["keyword"]= 42;
id2name[42]= "keyword";
name2id["keywords"]= 43;
id2name[43]= "keywords";
name2id["left"]= 44;
id2name[44]= "left";
name2id["lower"]= 45;
id2name[45]= "lower";
name2id["names"]= 46;
id2name[46]= "names";
name2id["op"]= 47;
id2name[47]= "op";
name2id["operand"]= 48;
id2name[48]= "operand";
name2id["ops"]= 49;
id2name[49]= "ops";
name2id["orelse"]= 50;
id2name[50]= "orelse";
name2id["right"]= 51;
id2name[51]= "right";
name2id["slice"]= 52;
id2name[52]= "slice";
name2id["step"]= 53;
id2name[53]= "step";
name2id["target"]= 54;
id2name[54]= "target";
name2id["targets"]= 55;
id2name[55]= "targets";
name2id["test"]= 56;
id2name[56]= "test";
name2id["type"]= 57;
id2name[57]= "type";
name2id["upper"]= 58;
id2name[58]= "upper";
name2id["value"]= 59;
id2name[59]= "value";
name2id["values"]= 60;
id2name[60]= "values";
name2id["Add"]= 61;
id2name[61]= "Add";
name2id["And"]= 62;
id2name[62]= "And";
name2id["BitAnd"]= 63;
id2name[63]= "BitAnd";
name2id["Div"]= 64;
id2name[64]= "Div";
name2id["Eq"]= 65;
id2name[65]= "Eq";
name2id["FloorDiv"]= 66;
id2name[66]= "FloorDiv";
name2id["Gt"]= 67;
id2name[67]= "Gt";
name2id["GtE"]= 68;
id2name[68]= "GtE";
name2id["In"]= 69;
id2name[69]= "In";
name2id["Lt"]= 70;
id2name[70]= "Lt";
name2id["LtE"]= 71;
id2name[71]= "LtE";
name2id["Mod"]= 72;
id2name[72]= "Mod";
name2id["Mult"]= 73;
id2name[73]= "Mult";
name2id["Not"]= 74;
id2name[74]= "Not";
name2id["NotEq"]= 75;
id2name[75]= "NotEq";
name2id["NotIn"]= 76;
id2name[76]= "NotIn";
name2id["Or"]= 77;
id2name[77]= "Or";
name2id["Sub"]= 78;
id2name[78]= "Sub";
name2id["USub"]= 79;
id2name[79]= "USub";
name2id["AnnAssign"]= 80;
id2name[80]= "AnnAssign";
name2id["Assign"]= 81;
id2name[81]= "Assign";
name2id["AugAssign"]= 82;
id2name[82]= "AugAssign";
name2id["Call"]= 83;
id2name[83]= "Call";
name2id["Continue"]= 84;
id2name[84]= "Continue";
name2id["Dict"]= 85;
id2name[85]= "Dict";
name2id["ExceptHandler"]= 86;
id2name[86]= "ExceptHandler";
name2id["For"]= 87;
id2name[87]= "For";
name2id["If"]= 88;
id2name[88]= "If";
name2id["IfExp"]= 89;
id2name[89]= "IfExp";
name2id["Import"]= 90;
id2name[90]= "Import";
name2id["Lambda"]= 91;
id2name[91]= "Lambda";
name2id["List"]= 92;
id2name[92]= "List";
name2id["ListComp"]= 93;
id2name[93]= "ListComp";
name2id["Pass"]= 94;
id2name[94]= "Pass";
name2id["Raise"]= 95;
id2name[95]= "Raise";
name2id["Return"]= 96;
id2name[96]= "Return";
name2id["Try"]= 97;
id2name[97]= "Try";
name2id["Tuple"]= 98;
id2name[98]= "Tuple";
name2id["While"]= 99;
id2name[99]= "While";
name2id["ClassDef"]= 100;
id2name[100]= "ClassDef";
name2id["FunctionDef"]= 101;
id2name[101]= "FunctionDef";
name2id["ImportFrom"]= 102;
id2name[102]= "ImportFrom";
name2id["Name"]= 103;
id2name[103]= "Name";
name2id["NameConstant"]= 104;
id2name[104]= "NameConstant";
name2id["Num"]= 105;
id2name[105]= "Num";
name2id["Str"]= 106;
id2name[106]= "Str";
name2id["arg"]= 107;
id2name[107]= "arg";
name2id["Keyword"]=108;
id2name[108]="Keyword";
name2id["IDENTIFIER"]=108;
id2name[108]="IDENTIFIER";
}
