#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include "wordle_solv.h"


/*
 ------------------------------------------------------------------------------------------------------------------------

                                    Création des différents éléments

 ------------------------------------------------------------------------------------------------------------------------
 */
struct wordle_tent * create_wordle_list()
{
    struct wordle_tent* list = NULL;
    list = (struct wordle_tent *) malloc(sizeof(struct wordle_tent));
    list->head = NULL;
    return list;
}

struct wordle_mot* create_wordle_mot()
{
    struct wordle_mot* list = NULL;
    list = (struct wordle_mot *) malloc(sizeof(struct wordle_mot));
    list->head = NULL;
    list->next = NULL;
    return list;
}

/*
 ------------------------------------------------------------------------------------------------------------------------

                                    Vérification si vide / Avoir nombre tentatives

 ------------------------------------------------------------------------------------------------------------------------
 */


bool wordle_list_empty(struct wordle_tent * trys)
{
    if (trys->head == NULL)
    {
        return true;
    }
    return false;
}

bool wordle_mot_empty(struct wordle_mot * word)
{
    if (word->head == NULL)
    {
        return true;
    }
    return false;
}


int get_number_tent(struct wordle_tent * trys)
{
    int len = 0;
    struct wordle_mot* pointer = trys->head;
    while (pointer != NULL)
    {
        len++;
        pointer = pointer->next;
    }
    return len;
}


/*
 ------------------------------------------------------------------------------------------------------------------------

                                    Détruire éléments

 ------------------------------------------------------------------------------------------------------------------------
 */

void wordle_list_destroy(struct wordle_tent * trys)
{
    if(wordle_list_empty(trys))
    {
        free(trys);
    }
    else
    {
        struct wordle_mot * pointer = trys->head;
        while(pointer->next != NULL)
        {
            struct wordle_mot * pointer_next = pointer->next;
            free(pointer);
            pointer = pointer_next;
        }
        free(pointer);
        free(trys);
    }
}

void wordle_mot_destroy(struct wordle_mot * word)
{
    if(wordle_mot_empty(word))
    {
        free(word);
    }
    else
    {
        struct wordle_element * pointer = word->head;
        while(pointer->next != NULL)
        {
            struct wordle_element * pointer_next = pointer->next;
            free(pointer);
            pointer = pointer_next;
        }
        free(pointer);
        free(word);
    }
}

/*
 ------------------------------------------------------------------------------------------------------------------------

                                    Ajout d'éléments

 ------------------------------------------------------------------------------------------------------------------------
 */

void wordle_list_append(struct wordle_tent * trys, struct wordle_mot * one_try)
{
    if(wordle_list_empty(trys))
    {
        struct wordle_mot * ajout = NULL;
        ajout = (struct wordle_mot *) malloc(sizeof(struct wordle_mot));
        ajout->head = one_try->head;
        ajout->next = NULL;
        trys->head = ajout;
    }
    else
    {
        struct wordle_mot * pointer = trys->head;
        while(pointer->next != NULL)
        {
            pointer = pointer->next;
        }
        struct wordle_mot * ajout = NULL;
        ajout = (struct wordle_mot *) malloc(sizeof(struct wordle_mot));
        ajout->head = one_try->head;
        ajout->next = NULL;
        pointer->next = ajout;
    }
}

void wordle_mot_append(struct wordle_mot * word, char lettre, int placement)
{
    if(wordle_mot_empty(word))
    {
        struct wordle_element * ajout = NULL;
        ajout = (struct wordle_element *) malloc(sizeof(struct wordle_element));
        ajout->letter = lettre;
        ajout->place = placement;
        ajout->next = NULL;
        word->head = ajout;
    }
    else
    {
        struct wordle_element * pointer = word->head;
        while(pointer->next != NULL)
        {
            pointer = pointer->next;
        }
        struct wordle_element * ajout = NULL;
        ajout = (struct wordle_element *) malloc(sizeof(struct wordle_element));
        ajout->letter = lettre;
        ajout->place = placement;
        ajout->next = NULL;
        pointer->next = ajout;
    }
}


/*
 ------------------------------------------------------------------------------------------------------------------------

                                    Avoir mot

 ------------------------------------------------------------------------------------------------------------------------
 */


struct linked_list_dico_t* get_word_length(struct linked_list_dico_t* dictionnaire, int len)
{
    char *filename = "dico.txt";
    FILE *fp = fopen(filename, "r");
    // reading line by line, max 256 bytes
    const unsigned MAX_LENGTH = 256;
    char buffer[MAX_LENGTH];
    char mot[330789][12];
    int i = 0;
    while(fgets(buffer, MAX_LENGTH, fp))
    {
        strcpy(mot[i],strtok(buffer,"\n"));
        if((int) strlen(mot[i]) == len)
        {
            list_append(dictionnaire,mot[i]);
        }
        i++;
    }
    // close the file
    fclose(fp);
    return dictionnaire;
}

/*
 ------------------------------------------------------------------------------------------------------------------------

                                    Avoir l'occurrence d'une lettre dans un mot

 ------------------------------------------------------------------------------------------------------------------------
 */

int is_several(char letter, struct wordle_element* word)
{
    int comp = 0;
    int i = 0;
    while(word != NULL)
    {
        if(word->letter == letter && word->place != 0)
        {
            comp++;
        }
        word = word->next;
        i++;
    }
    return comp;
}



/*
 ------------------------------------------------------------------------------------------------------------------------

                                    Avoir mot contenant pas la lettre

 ------------------------------------------------------------------------------------------------------------------------
 */

struct linked_list_dico_t* get_word_without(char lettre, struct linked_list_dico_t* list_word)
{
    struct linked_list_dico_t* dico = list_create();
    struct list_element * pointer = list_word->head;
    int len = strlen(list_word->head->word);
    while(pointer != NULL)
    {
        int i;
        int comp = 0;
        for(i=0; i < len; i++)
        {
            if(pointer->word[i] == lettre)
            {
                comp++;
            }
        }
        if(comp == 0)
        {
            list_append(dico,pointer->word);
        }
        pointer = pointer->next;
    }
    return dico;
}

/*
 ------------------------------------------------------------------------------------------------------------------------

                                    Avoir mot exactement n occurence de la lettre

 ------------------------------------------------------------------------------------------------------------------------
 */


struct linked_list_dico_t* get_word_with_between(char lettre, struct linked_list_dico_t* list_word,int inf, int max)
{
    struct linked_list_dico_t* dico = list_create();
    struct list_element * pointer = list_word->head;
    int len = strlen(list_word->head->word);
    while(pointer != NULL)
    {
        int i;
        int comp = 0;
        for(i=0; i < len; i++)
        {
            if(pointer->word[i] == lettre)
            {
                comp++;
            }
        }
        if(inf <= comp && comp <= max)
        {
            list_append(dico,pointer->word);
        }
        pointer = pointer->next;
    }
    return dico;
}


/*
 ------------------------------------------------------------------------------------------------------------------------

                                    Avoir mot la lettre a cet endroit

 ------------------------------------------------------------------------------------------------------------------------
 */

struct linked_list_dico_t* get_word_with_here(char lettre, struct linked_list_dico_t* list_word, int index)
{
    struct linked_list_dico_t* dico = list_create();
    struct list_element * pointer = list_word->head;
    int len = strlen(list_word->head->word);
    while(pointer != NULL)
    {
        int i;
        for(i=0; i < len; i++)
        {
            if(pointer->word[i] == lettre && i == index)
            {
                list_append(dico,pointer->word);
            }
        }
        pointer = pointer->next;
    }
    return dico;
}

/*
 ------------------------------------------------------------------------------------------------------------------------

                                    Avoir mot contenant la lettre pas ici

 ------------------------------------------------------------------------------------------------------------------------
 */

struct linked_list_dico_t* get_word_with_not_here(char lettre, struct linked_list_dico_t* list_word, int index)
{
    struct linked_list_dico_t* dico = list_create();
    struct list_element *pointer = list_word->head;
    int len = strlen(list_word->head->word);
    while (pointer != NULL)
    {
        int i;
        int cmp = 0;
        int cbp = 0;
        for (i = 0; i < len; i++)
        {
            if (pointer->word[i] == lettre && i != index)
            {
                cmp++;
            }
            if (pointer->word[i] == lettre && i == index)
            {
                cbp++;
            }
        }
        if(cmp != 0 && cbp == 0)
        {
            list_append(dico, pointer->word);

        }
        pointer = pointer->next;
    }
    return dico;
}


/*
 ------------------------------------------------------------------------------------------------------------------------

                                   !!!!!     SOLVEUR      !!!!!!!!

 ------------------------------------------------------------------------------------------------------------------------
 */


char* solveur(struct wordle_tent* tentatives, int len_mot)
{
    if(get_number_tent(tentatives) == 0)
    {
        char* res[7] = {"saine","nieras","taniser","notaires","relations","soufraient","adulterions"};
        printf("\n Le solveur renvoie le mot: %s\n", res[len_mot - 5]);
        printf("\n");
        return res[len_mot - 5];
    }
    else
    {
        int nombre_tentative = 2 * (get_number_tent(tentatives) * len_mot + 1);
        struct linked_list_dico_t*  dico[nombre_tentative];
        int j = 0;
        dico[j] = list_create();
        get_word_length(dico[j], len_mot);
        j++;
        struct wordle_mot * pointer = tentatives->head;
        while(pointer != NULL)
        {
            int i = 0;
            struct wordle_element* mot = pointer->head;
            while(mot != NULL)
            {
                if(mot->place == 0)
                {
                    int cmp = is_several(mot->letter, pointer->head);
                    if(cmp == 0)
                    {
                        dico[j] = get_word_without(mot->letter, dico[j-1]);
                    }
                    else
                    {
                        dico[j] = get_word_with_between(mot->letter,dico[j-1],cmp, cmp);
                    }
                }
                if(mot->place == 1)
                {
                    int cmp = is_several(mot->letter, pointer->head);
                    if(cmp == 1)
                    {
                        dico[j] = get_word_with_not_here(mot->letter, dico[j-1], i);
                    }
                    else
                    {
                        dico[j] = get_word_with_between(mot->letter,dico[j-1],cmp, len_mot);
                        j++;
                        dico[j] = get_word_with_not_here(mot->letter, dico[j-1], i);
                    }
                }
                if(mot->place == 2)
                {
                    int cmp = is_several(mot->letter, pointer->head);
                    if(cmp == 1)
                    {
                        dico[j] = get_word_with_here(mot->letter, dico[j-1], i);
                    }
                    else
                    {
                        dico[j] = get_word_with_between(mot->letter,dico[j-1],cmp, len_mot);
                        j++;
                        dico[j] = get_word_with_here(mot->letter, dico[j-1], i);
                    }
                }
                i++;
                j++;
                mot = mot->next;
                if(i == len_mot)
                {
                    i = 0;
                }
            }
            pointer = pointer->next;
        }
        char* res = dico[j - 1]->head->word;
        printf("\n Le solveur renvoie le mot: %s\n", dico[j - 1]->head->word);
        printf("\n");
        int k;
        for(k=0; k < j; k++)
        {
            list_destroy(dico[k]);
        }
        return res;
    }
}



/*
 ------------------------------------------------------------------------------------------------------------------------

                                    Fonction dico

 ------------------------------------------------------------------------------------------------------------------------
 */


struct linked_list_dico_t* list_create()
{
    struct linked_list_dico_t* list = NULL;
    list = (struct linked_list_dico_t*) malloc(sizeof(struct linked_list_dico_t));
    list->head = NULL;
    return list;
}

bool list_is_empty(struct linked_list_dico_t* one_list)
{
    if (one_list->head == NULL)
    {
        return true;
    }
    else
    {
        return false;
    }
}

void list_prepend(struct linked_list_dico_t* one_list, char* mot)
{
    if(list_is_empty(one_list))
    {
        struct list_element * ajout = NULL;
        ajout = (struct list_element*) malloc(sizeof(struct list_element));
        ajout->word = mot;
        ajout->next = NULL;
        one_list->head = ajout;
    }
    else
    {
        struct list_element * ajout = NULL;
        ajout = (struct list_element*) malloc(sizeof(struct list_element));
        ajout->word = mot;
        ajout->next = one_list->head;
        one_list->head = ajout;
    }
}

void list_destroy(struct linked_list_dico_t* one_list)
{
    if(list_is_empty(one_list))
    {
        free(one_list);
    }
    else
    {
        struct list_element * pointer = one_list->head;
        while(pointer != NULL)
        {
            struct list_element * pointer_next = pointer->next;
            free(pointer);
            pointer = pointer_next;
        }
        free(pointer);
        free(one_list);
    }
}

void list_append(struct linked_list_dico_t* one_list, char* mot)
{
    if(list_is_empty(one_list))
    {
        list_prepend(one_list, mot);
    }
    else
    {
        struct list_element * pointer = one_list->head;
        while(pointer->next != NULL)
        {
            pointer = pointer->next;
        }
        struct list_element * ajout = NULL;
        ajout = (struct list_element*) malloc(sizeof(struct list_element));
        ajout->word = mot;
        ajout->next = NULL;
        pointer->next = ajout;
    }
}

void list_print(struct linked_list_dico_t* one_list) //selon le format suivant [mot1, mot2, mot3, mot4 ]
{
    if(list_is_empty(one_list))
    {
        printf("[]");
    }
    else
    {
        struct list_element * pointer = one_list->head;
        printf("[");
        while(pointer->next != NULL)
        {
            printf(" %s", pointer->word);
            printf("%c", ',');
            pointer = pointer->next;
        }
        printf(" %s]", pointer->word);
    }
}
