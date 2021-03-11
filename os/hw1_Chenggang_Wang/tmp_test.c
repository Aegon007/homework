#include <iostream>
#include <string.h>

using namespace std;

int main(void)
{
    int a[100];
    cout<<sizeof(a)<<endl;
    memset(a, 0, sizeof(a));
    /**
    for(int i=0;i<100;i++)
    {
        a[i]=0;
    }
    */
    for(int i=0;i<100;i++)
    {
        cout<<a[i]<<endl;
    }
    return 0;
}
