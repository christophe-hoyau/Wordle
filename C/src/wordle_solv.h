#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>

#ifndef C_WORDLE_SOLV_H
#define C_WORDLE_SOLV_H

struct wordle_element
{
    char letter;
    int place;
    struct wordle_element * next;
};

struct wordle_mot
{
    struct wordle_element* head;
    struct wordle_mot * next;
};


struct wordle_tent
{
    struct wordle_mot * head;
};




struct wordle_tent * create_wordle_list(); // Créer une liste vide de tentative les

struct wordle_mot * create_wordle_mot();// Créer un mot tenter avec lettre et placement


bool wordle_list_empty(struct wordle_tent * trys); // Vérifier si la liste de tentative est vide

bool wordle_mot_empty(struct wordle_mot * word); // Vérifie si le mot est vide

int get_number_tent(struct wordle_tent * trys);

void wordle_list_destroy(struct wordle_tent * trys); // Détruire la liste de tentative

void wordle_mot_destroy(struct wordle_mot * word); // Détruire le mot

void wordle_list_append(struct wordle_tent * trys, struct wordle_mot * one_try); // Ajouter une tentative en queue de liste

void wordle_mot_append(struct wordle_mot * word, char lettre, int placement); // Créer un mot tentative

struct linked_list_dico_t* get_word_length(struct linked_list_dico_t* dictionnaire, int len);

struct linked_list_dico_t* get_word_without(char lettre, struct linked_list_dico_t* list_word);

struct linked_list_dico_t* get_word_with_between(char lettre, struct linked_list_dico_t* list_word,int inf, int max);

struct linked_list_dico_t* get_word_with_not_here(char lettre, struct linked_list_dico_t* list_word, int index);

struct linked_list_dico_t* get_word_with_here(char lettre, struct linked_list_dico_t* list_word, int index);

char* solveur(struct wordle_tent* tentatives, int len_mot);

int is_several(char letter, struct wordle_element* word);

/*

------------------------------------------------------------------------------------------------------------------------

                            Structure dico

------------------------------------------------------------------------------------------------------------------------
 */

struct list_element
{
    char* word;
    struct list_element * next;
};

struct linked_list_dico_t
{
    struct list_element * head;
};


struct linked_list_dico_t* list_create();

bool list_is_empty(struct linked_list_dico_t* one_list);

void list_prepend(struct linked_list_dico_t* one_list, char* mot);

void list_append(struct linked_list_dico_t* one_list, char* mot);

void list_destroy(struct linked_list_dico_t* one_list);

struct linked_list_dico_t* get_word_length(struct linked_list_dico_t* dictionnaire, int len);

void list_print(struct linked_list_dico_t* one_list);

#endif //C_WORDLE_SOLV_H
