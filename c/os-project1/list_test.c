#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "list.h"


int test_create_list(void);
int test_add_to_list(void);
int test_remove_from_list(void);
int test_print_list(void);
int test_flush_list(void);
int test_free_list(void);


/* This function will have tests for the entire project.
 * Main will call a different function to test different pieces of the function.
 * This function takes no arguments and will return a 1 for failure and a 0 for success*/
int main(void)
{
    int test_create_list_result = test_create_list();
    if (test_create_list_result != 0) {
        return EXIT_FAILURE;
    }

    int test_free_list_result = test_free_list();
    if (test_free_list_result != 0) {
        return EXIT_FAILURE;
    }

    int test_flush_list_result = test_flush_list();
    if (test_flush_list_result != 0) {
        return EXIT_FAILURE;
    }

    int test_add_to_list_result = test_add_to_list();
    if (test_add_to_list_result != 0) {
        return EXIT_FAILURE;
    }

    int test_remove_from_list_result = test_remove_from_list();
    if (test_remove_from_list_result != 0) {
        return EXIT_FAILURE;
    }

    int test_print_list_result = test_print_list();
    if (test_print_list_result != 0) {
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}


/* This function will validate that the list in created and has a NULL head pointer.
 * This function will return a 0 for success or 1 for failure
 * This function takes no arguments */
int test_create_list(void)
{
    list *ll = create_list();
    
    if (ll == NULL) {
        fprintf(stderr, "FAILURE: create_list returned a NULL pointer\n");
        return EXIT_FAILURE;
    }
    if (ll->head != NULL) {
        fprintf(stderr, "FAILURE: The list was not created with a NULL head pointer\n");
        free(ll);
        return EXIT_FAILURE;
    }
    printf("SUCCESS: create_list created an empty list\n");

    free(ll);
    return EXIT_SUCCESS;
}


/* This function will validate the ability to add a new node to the list with a copy of item
 * This function will return 0 for success and 1 for failue
 * This function takes no arguments */
int test_add_to_list(void)
{
    list *ll = create_list();

    /* Checks for valid functionality should return 0 */
    if (add_to_list(ll, "Test string 1") != 0) {
        fprintf(stderr, "FAILURE: add_to_list failed to add the first item\n");
        free_list(&ll);
        return EXIT_FAILURE;
    }
    if (add_to_list(ll, "Test string 2") != 0) {
        fprintf(stderr, "FAILURE: add_to_list failed to add the second item\n");
        free_list(&ll);
        return EXIT_FAILURE;
    }
    if (add_to_list(ll, "Test string 3") != 0) {
        fprintf(stderr, "FAILURE: add_to_list failed to add the third item\n");
        free_list(&ll);
        return EXIT_FAILURE;
    }
    printf("SUCCESS: add_to_list successfully added strings to the linked list\n");

    /* Checks for invalid functionality, should return 1 if either argument is NULL */
    if (add_to_list(NULL, "Test string for NULL ll pointer") != 1) {
        fprintf(stderr, "FAILURE: add_to_list didnt return a 1 when the pointer to ll was NULL\n");
        free_list(&ll);
        return EXIT_FAILURE;
    }
    if (add_to_list(ll, NULL) != 1) {
        fprintf(stderr, "FAILURE: add_to_list didnt return a 1 when the string was NULL\n");
        free_list(&ll);
        return EXIT_FAILURE;
    }
    if (add_to_list(NULL, NULL) != 1) {
        fprintf(stderr, "FAILURE: add_to_list didnt return a 1 when both arguments were NULL\n");
        free_list(&ll);
        return EXIT_FAILURE;
    }
    printf("SUCCESS: add_to_list successfully returned 1 when invalid input was sent as args\n");

    free_list(&ll);
    return EXIT_SUCCESS;
}


/* This function will validate the ability to remove a node from the linked list
 * This function will return 0 for success and 1 for failue
 * This function takes no arguments */
int test_remove_from_list(void)
{
    /* Populate list with 3 items values */
    list *ll = create_list();
    add_to_list(ll, "Test String 1");
    add_to_list(ll, "Test String 2");
    add_to_list(ll, "Test String 3");

    /* Checks for error handling, should return NULL if either argument is NULL even if the list has items */
    if (remove_from_list(NULL) != NULL) {
        fprintf(stderr, "FAILURE: remove_from_list didnt return NULL when no list was sent\n");
        free_list(&ll);
        return EXIT_FAILURE;
    }

    /* Checks for valid functionality should return test string 1, 2, 3 in order then should return NULL */
    char *removed_item1 = remove_from_list(ll);
    if (strcmp("Test String 1", removed_item1) != 0) {
        fprintf(stderr, "FAILURE: remove_from_list didnt return the first string\n");
        free(removed_item1);
        free_list(&ll);
        return EXIT_FAILURE;
    }

    char *removed_item2 = remove_from_list(ll);
    if (strcmp("Test String 2", removed_item2) != 0) {
        fprintf(stderr, "FAILURE: remove_from_list didnt return the second string\n");
        free(removed_item2);
        free_list(&ll);
        return EXIT_FAILURE;
    }

    char *removed_item3 = remove_from_list(ll);
    if (strcmp("Test String 3", removed_item3) != 0) {
        fprintf(stderr, "FAILURE: remove_from_list didnt return the third string\n");
        free(removed_item3);
        free_list(&ll);
        return EXIT_FAILURE;
    }

    if (remove_from_list(ll) != NULL) {
        fprintf(stderr, "FAILURE: remove_from_list didnt return NULL when the list was empty\n");
        free_list(&ll);
        return EXIT_FAILURE;
    }

    printf("SUCCESS: remove_from_list removed the correct items in the correct order then returned NULL\n");
    free(removed_item1);
    free(removed_item2);
    free(removed_item3);
    free_list(&ll);
    return EXIT_SUCCESS;
}


/* This function will validate the print_list function
 * This function will return 0 for success and 1 for failure
 * This function takes no arguments */
int test_print_list(void)
{
    list *ll = create_list();
    add_to_list(ll, "Test String 1");
    add_to_list(ll, "Test String 2");
    add_to_list(ll, "Test String 3");

    print_list(ll);
    printf("SUCCESS: print_list successfully printed everything from the list\n");

    free_list(&ll);
    return EXIT_SUCCESS;
}


/* This function will validate the flush_list function
 * This function will return 0 for success and 1 for failure
 * This function takes no arguments */
int test_flush_list(void)
{
    /* Populate list with 3 items values */
    list *ll = create_list();
    add_to_list(ll, "Test String 1");
    add_to_list(ll, "Test String 2");
    add_to_list(ll, "Test String 3");

    /* First test to ensure the head pointer in the list is set to NULL */
    flush_list(ll);
    if (ll->head != NULL) {
        fprintf(stderr, "FAILURE: flush_list did not set the head pointer to NULL\n");
        free_list(&ll);
        return EXIT_FAILURE;
    }

    /* Should be able ot use the same list pointer after flush_list */
    if (add_to_list(ll, "Test String 1") != 0) {
        fprintf(stderr, "FAILURE: flush_list did not leave the list pointer usable to add new items to\n");
        free_list(&ll);
        return EXIT_FAILURE;
    }

    printf("SUCCESS: flush_list successfully returned a NULL list head pointer\n");
    free_list(&ll);
    return EXIT_SUCCESS;
}


/* This function will validate the free_list function
 * This function will return 0 for success and 1 for failure
 * This function takes no arguments */
int test_free_list(void)
{
    /* Populate list with 3 items values */
    list *ll = create_list();
    add_to_list(ll, "Test String 1");
    add_to_list(ll, "Test String 2");
    add_to_list(ll, "Test String 3");

    free_list(&ll);

    if (ll != NULL) {
        fprintf(stderr, "FAILURE: free_list did not clear the list pointer\n");
        free_list(&ll);
        return EXIT_FAILURE;
    }

    printf("SUCCESS: free_list successfully set the list pointer to NULL\n");
    free_list(&ll);
    return EXIT_SUCCESS;
}
