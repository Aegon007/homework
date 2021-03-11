/**
 *
 * Advanced algorithm homework1
 * Copyright@Chenggang Wang
 * M12645906
 * Year 2019
 */

#include "rsa.h"
#include <iostream>
#include <string>


using namespace std;


char* breakDownStr(string input_str)
{
    int n = input_str.length();

    char rtn[n+1];
    strcpy(rtn, input_str.c_str());

    return rtn;
}

int main(int argc, char* argv[])
{
    string input_str;
    while(true){
        getline(cin, input_str, '\n');
        if(input_str == "quit"){
            break;
        }
        cout<<input_str<<endl;
    }
    return 0;
}
