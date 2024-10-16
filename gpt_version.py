import re
from collections import defaultdict

class MarkdownTreeParser:
    def __init__(self, markdown_file):
        with open(markdown_file, 'r') as file:
            self.lines = file.readlines()

    def parse(self):
        tree = {'content': [], 'children': defaultdict(list)}  # Root node
        current_node = tree
        header_stack = []

        for line in self.lines:
            stripped_line = line.strip()

            if stripped_line.startswith('#'):
                current_node = self.handle_header(stripped_line, tree, header_stack)
            elif stripped_line.startswith('-') or stripped_line.startswith('*'):
                current_node['content'].append(self.parse_list_item(stripped_line))
            else:
                current_node['content'].append(self.parse_paragraph(stripped_line))

        return tree

    def handle_header(self, line, tree, header_stack):
        header_level = len(line) - len(line.lstrip('#'))
        header_text = line.strip('# ').strip()
        
        # Create a new node for this header
        new_node = {'header': header_text, 'content': [], 'children': defaultdict(list)}

        # Pop the header stack to find the correct parent
        while header_stack and header_stack[-1][0] >= header_level:
            header_stack.pop()

        # Find the parent node
        if header_stack:
            parent_node = header_stack[-1][1]
        else:
            parent_node = tree

        # Add new node to parent's children
        parent_node['children'][header_level].append(new_node)

        # Push the new node onto the header stack
        header_stack.append((header_level, new_node))

        return new_node

    def parse_list_item(self, line):
        return f"List item: {line[2:].strip()}"

    def parse_paragraph(self, line):
        if line:
            return f"Paragraph: {line.strip()}"
        return None

    def print_tree(self, node, depth=0):
        indent = '  ' * depth
        if 'header' in node:
            print(f"{indent}Header: {node['header']}")
        for content in node['content']:
            if content:
                print(f"{indent}  {content}")
        for level in node['children']:
            for child in node['children'][level]:
                self.print_tree(child, depth + 1)


# Example usage
if __name__ == "__main__":
    parser = MarkdownTreeParser('sample.md')
    tree = parser.parse()
    parser.print_tree(tree)

