class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None


    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node


    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        
        last_node.next = new_node


    def length(self):
        count = 0
        curr = self.head

        while curr:
            curr = curr.next
            count += 1
        return count
    

    def print_list(self):
        curr = self.head
        while curr:
            print(curr.data, end=' -> ')
            curr = curr.next
        print("None")


    def search(self, key):
        curr = self.head
        while curr:
            if curr.data == key:
                return True
            curr = curr.next
        return False
    

    def delete_node(self, key):
        curr = self.head

        if curr and curr.data == key:
            self.head = curr.next
            curr = None
            return
        
        prev = None

        while curr and curr.data != key:
            prev = curr
            curr = curr.next

        if curr is None:
            return
        
        prev.next = curr.next
        curr = None


    def insert_after(self, prev, data):
        if not prev:
            print("Previous node doesn't exist.")
            return
        
        new = Node(data)
        new.next = prev.next
        prev.next = new
        


def main():
    linked_list = LinkedList()

    for num in range(1,11):
        linked_list.append(num)
    print("Created list with nodes 1-10:")
    print("Linked list length: ", linked_list.length())
    linked_list.print_list()
    print()

    linked_list.prepend(0)
    print("Prepended with 0:")
    print("Linked list length: ", linked_list.length())
    linked_list.print_list()
    print()

    linked_list.insert_after(linked_list.head.next, 1.5)
    print("Inserted 1.5 into linked list:")
    print("Linked list length: ", linked_list.length())
    linked_list.print_list()
    print()

    linked_list.delete_node(1.5)
    print("Deleted the 1.5 node")
    print("Linked list length: ", linked_list.length())
    linked_list.print_list()
    print()

    print("Searching for number 5 in the linked list:")
    print(linked_list.search(5))
    print()

    print("Searching for the number 11 in the linked list:")
    print(linked_list.search(11))
    print()


if __name__ == '__main__':
    main()