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
        self.command_to_handler = {
            "left": self._handle_command_left,
            "right": self._handle_command_right,
            "insert": self._handle_insert,
        }

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

    def parse_input(self, user_input) -> list[str, list]:
        command_parts = user_input.split(" ")
        command = command_parts[0]
        command_args = command_parts[1:]
        return command, command_args

    def execute_command(self, user_input: str):
        command, args = self.parse_input(user_input)
        mapped_handler = self.command_to_handler.get(command, None)
        if mapped_handler:
            mapped_handler(args)
        else:
            print(f"Invalid command: {user_input=}")
        print(self.get_text())

    def _handle_command_left(self, args: list[str] | None):
        if not args:
            self._move_cursor_left()

        elif len(args) > 1:
            print(f"Please insert one argument: {args=}")

        else:
            if args[0].isnumeric():
                self._move_cursor_left(int(args[0]))

            else:
                print(f"Not numeric argument {args=}")

    def _move_cursor_left(self, times: int = 1):
        for _ in range(times):
            left = self.cursor.prev
            if left is self.head:
                break

            # connect cursor node with left.prev node
            self.cursor.prev = left.prev
            left.prev.next = self.cursor

            # connect left node with cursor.next node
            left.next = self.cursor.next
            self.cursor.next.prev = left

            # switch position with cursor node and left node
            self.cursor.next = left
            left.prev = self.cursor

    def _handle_command_right(self, args: list[str] | None):
        if not args:
            self._move_cursor_right()

        elif len(args) > 1:
            print(f"Please insert one argument: {args=}")

        else:
            if args[0].isnumeric():
                self._move_cursor_right(int(args[0]))

            else:
                print(f"Not numeric argument {args=}")

    def _move_cursor_right(self, times: int = 1):
        for _ in range(times):
            right = self.cursor.next
            if right is self.tail:
                break

            # connect cursor node with right.next node
            self.cursor.next = right.next
            right.next.prev = self.cursor

            # connect right node with cursor.prev node
            right.prev = self.cursor.prev
            self.cursor.prev.next = right

            # switch position with cursor node and right node
            self.cursor.prev = right
            right.next = self.cursor

    def _handle_insert(self, args: list[str] | None):
        if not args:
            self._insert_character()
            self._move_cursor_right()

        elif len(args) > 2:
            print(f"Please Please insert one argument: {args=}")

        else:
            ch = args[0]
            if ch:
                self._insert_character(ch)
            else:
                self._insert_character()
            self._move_cursor_right()

    def _insert_character(self, ch: str = " "):
        new_node = Node(value=ch)

        new_node.next = self.cursor.next
        self.cursor.next = new_node

        new_node.prev = self.cursor
        new_node.next.prev = new_node


def main():
    text = "Hello, world!"
    text_editor = Text_Editor(text)

    print(text_editor.get_text())

    while True:
        user_input = input(
            "Command (insert character, delete, right times, left times, undo, quit): "
        )
        if user_input == "quit":
            break

        text_editor.execute_command(user_input)


if __name__ == "__main__":
    main()
