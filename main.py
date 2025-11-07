class Node:
    def __init__(self, value: str, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next


class Text_Editor:
    def __init__(self, text):
        self.head = Node(None)
        self.tail = Node(None)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.build(text)
        self.cursor = self.tail.prev

    def build(self, text):
        for character in reversed(text):
            self.insert_at_first(character)

        self.insert_at_last("|")

    def insert_at_first(self, value):
        new_node = Node(value)
        new_node.next = self.head.next
        new_node.prev = self.head
        new_node.next.prev = new_node
        self.head.next = new_node

    def insert_at_last(self, value):
        new_node = Node(value)
        new_node.next = self.tail
        new_node.prev = self.tail.prev
        self.tail.prev.next = new_node
        self.tail.prev = new_node

    def get_text(self) -> str:
        text = ""
        curr_node = self.head.next
        while curr_node is not self.tail:
            text += curr_node.value
            curr_node = curr_node.next
        return text


def main():
    text = "Hello, world!"
    text_editor = Text_Editor(text)

    print(text_editor.get_text())


if __name__ == "__main__":
    main()
