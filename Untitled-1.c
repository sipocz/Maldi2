#include <stdio.h>
#include <stdlib.h>
int main()
{
printf("Kerek egy szamot: ");
int hossz;
scanf("%d",&hossz);
int space=-2;
for(int i=1;i<=hossz*2;i++){
        if(i<=hossz){
            printf("%*s",hossz-i,"");
            printf("/");
            space+=2;
            printf("%*s",space,"");
            printf("\\");
            printf("\n");
        }
}
//space=space+2;
for(int i=1;i<=hossz;i++){
    printf("%*s",i-1,"");
    printf("\\");
    printf("%*s",space,"");
    printf("/");
    printf("\n");
    space=space-2;
}
return 0;
}