#include "wordle_solv.h"

int main(void)
{
    char lens[256];
    int len;
    char *filename = "wsolf.txt";
    FILE *fp = fopen(filename, "r");
    fgets(lens, 256, fp);
    len = atoi(lens);

    struct wordle_tent * list = create_wordle_list();
    struct wordle_mot * word[7];
    int nombre_tent = 1;



    int i;
    for(i = 0; i < 7; i++)
    {
        word[i] = create_wordle_mot();
        int j;
        double arret;

        char* res = solveur(list,len);

        printf("Voulez vous arrêtez le solveur ? \nSi oui renvoyez -1 : ");
        scanf("%lf", &arret);
        printf("\n");


        if(arret == -1)
        {
            break;
        }



        printf("Quelle est le placement des lettres du mot donné ? : ");

        int place[len];

        if(len == 5)
        {
            scanf("%1d%1d%1d%1d%1d", &place[0], &place[1], &place[2], &place[3], &place[4]);
            for(j = 0; j < len; j++)
            {
                wordle_mot_append(word[i], res[j], place[j]);
            }
        }

        if(len == 6)
        {
            scanf("%1d%1d%1d%1d%1d%1d", &place[0], &place[1], &place[2], &place[3], &place[4], &place[5]);
            for(j = 0; j < len; j++)
            {
                wordle_mot_append(word[i], res[j], place[j]);
            }
        }

        if(len == 7)
        {
            scanf("%1d%1d%1d%1d%1d%1d%1d", &place[0], &place[1], &place[2], &place[3], &place[4], &place[5], &place[6]);
            for(j = 0; j < len; j++)
            {
                wordle_mot_append(word[i], res[j], place[j]);
            }
        }

        if(len == 8)
        {
            scanf("%1d%1d%1d%1d%1d%1d%1d%1d", &place[0], &place[1], &place[2], &place[3], &place[4], &place[5], &place[6], &place[7]);
            for(j = 0; j < len; j++)
            {
                wordle_mot_append(word[i], res[j], place[j]);
            }
        }

        if(len == 9)
        {
            scanf("%1d%1d%1d%1d%1d%1d%1d%1d%1d", &place[0], &place[1], &place[2], &place[3], &place[4], &place[5], &place[6], &place[7], &place[8]);
            for(j = 0; j < len; j++)
            {
                wordle_mot_append(word[i], res[j], place[j]);
            }
        }


        if(len == 10)
        {
            scanf("%1d%1d%1d%1d%1d%1d%1d%1d%1d%1d", &place[0], &place[1], &place[2], &place[3], &place[4], &place[5], &place[6], &place[7], &place[8], &place[9]);
            for(j = 0; j < len; j++)
            {
                wordle_mot_append(word[i], res[j], place[j]);
            }
        }

        if(len == 11)
        {
            scanf("%1d%1d%1d%1d%1d%1d%1d%1d%1d%1d%1d", &place[0], &place[1], &place[2], &place[3], &place[4], &place[5], &place[6], &place[7], &place[8], &place[9], &place[10]);
            for(j = 0; j < len; j++)
            {
                wordle_mot_append(word[i], res[j], place[j]);
            }
        }

        wordle_list_append(list, word[i]);
        nombre_tent++;
    }




    for(i = 0; i < nombre_tent ; i++)
    {
        wordle_mot_destroy(word[i]);
    }
    wordle_list_destroy(list);

    return 0;


}
