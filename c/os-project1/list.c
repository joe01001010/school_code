#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "list.h"

/* Allocate space for a new list and set its head to NULL.
 * Returns the created list if successful, NULL otherwise. */
list *create_list()
{
    list *ll = malloc(sizeof *ll);

    if (ll == NULL) {
        return NULL;
    }

    ll->head = NULL;
    return ll;
}


/* Allocates a new node and copies the string from item to this node
* (use malloc, strlen, and strncpy; or try strdup) . Adds this new node
* to end of the list ll. Returns 0 if successful, non-zero otherwise. */
int add_to_list(list *ll, char *item) {
    /* Base case check for if the list is NULL or if the item is NULL return 1 */
    if (ll == NULL || item == NULL) {
        return 1;
    }

    node *new_node = malloc(sizeof *new_node);
    if (new_node == NULL) {
        return 1;
    }

    size_t bytes = strlen(item) + 1;
    new_node->item = malloc(bytes);
    if (new_node->item == NULL) {
        free(new_node);
        return 1;
    }

    strncpy(new_node->item, item, bytes);
    new_node->next = NULL;

    if (ll->head == NULL) {
        ll->head = new_node;
    } else {
        node *current = ll->head;
        while (current->next != NULL) {
            current = current->next;
        }
        current->next = new_node;
    }

    return 0;
}


/* Removes the head of the list ll (and move the head of ll to the next node
* in the list), extracts the string stored in the head, and returns a
* pointer to this string. Also frees the removed head node. */
char *remove_from_list(list *ll) {
    /* Base case check for if the list is NULL or if the head pointer is NULL return NULL */
    if (ll == NULL || ll->head == NULL) {
        return NULL;
    }

    node *old_head = ll->head;
    char *item = old_head->item;

    ll->head = old_head->next;
    free(old_head);

    return item;
}


/* Prints every string in each node of the list ll, with a new line
* character at the end of each string */
void print_list(list *ll)
{
    /* Check if ll is NULL and return because there is nothing to print */
    if (ll == NULL) {
        return;
    }

    /* Iterate until the current node is null and print every item if the current node is not NULL */
    node *current = ll->head;
    while (current != NULL) {
        printf("%s\n", current->item);
        current = current->next;
    }
}


/* Flushes (clears) the entirelist and re-initializes the list. The passed
* pointer ll should still point to a valid, empty list when this function
* returns. Any memory allocated to store nodes in the list should be freed. */
void flush_list(list *ll)
{
    /* Check if the list is null and return because there is nothing to flush */
    if (ll == NULL) {
        return;
    }

    /* Iterate through the list until ll->head is NULL and move current head into a temp variable
     * move temp variables next pointer into head and then free the old head pointer*/
    while (ll->head != NULL) {
         node *old_head = ll->head;
         ll->head = old_head->next;
         free(old_head->item);
         free(old_head);
    }
}


/* De-allocates all data for the list. Ensure all memory allocated for list
* ll is freed, including any allocated strings and list ll itself. */
void free_list(list **ll)
{
    /* Have to check for the list being null and the address for the list being null to return */
    if (ll == NULL || *ll == NULL) {
        return;
    }

    flush_list(*ll);
    free(*ll);
    *ll = NULL;
}
