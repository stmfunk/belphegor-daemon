import typing
import sys
import re

from typing import Optional

debug = False

indentation_level = '   >'
bulleted_task_pattern = r'\s*- \[.\].*'
numbered_task_pattern = r'\s*[0-9]+\. \[.\].*'
bulleted_task_incomplete_pattern = r'\s*- \[ \].*'
numbered_task_incomplete_pattern = r'\s*[0-9]+\. \[ \].*'
empty_line_pattern = r'\s*$'
link_pattern = r'https?://'

class NoteTask:
    def __init__(self, text, status=False):
        self.status = status
        self.text   = text

class NoteTree:
    'Here we will include the code for parsing a particular heading'

    def __init__(self, heading_name, depth=0):
        self.heading_name = heading_name
        self.bare_text = []
        self.tasks = []
        self.links = []

        self.depth = depth

        self.subheadings = []

    def __str__(self):
        current_node_str = f'''{self.heading_name}'''

        return current_node_str

    def print_me(self):
        print((indentation_level * self.depth) + self.__str__())
        for line in self.bare_text:
            print((indentation_level * (self.depth+1)) + line)

        for heading in self.subheadings:
            heading.print_me()

    def export_md_file(self):
        markdown_text = ''

        if self.depth > 0:
            markdown_text += f'{"#"*self.depth} {self.heading_name}\n'

        for line in self.bare_text:
            markdown_text += line + '\n'

        for heading in self.subheadings:
            markdown_text += heading.export_md_file()

        return markdown_text

    def append_text(self, new_text: str):
        self.bare_text.append(new_text)

    def add_task(self, text):
        if re.match(bulleted_task_incomplete_pattern, text) or re.match(numbered_task_incomplete_pattern, text):
            status = False
        else:
            status = True

        self.tasks.append(NoteTask(text, status))

    def add_leaf(self, leaf):
        if debug: print("Adding leaf: %s to node:%s" % (leaf, self.heading_name))
        self.subheadings.append(leaf)


class FileObject:
    '''
    This is the generic object all obsidian 
    files are based on
    '''
    headings = {}
    full_note = []

    def __init__(self, note: typing.TextIO):
        self.note = note

    def parse(self):
        self.full_note = self.note.readlines()

        (_, self.tree) = self.default_parser('root',0,0)


    def default_parser(self, heading, start_line, depth):
        if debug: print("Spawned new instance heading:%s, startline:%d, depth:%d," % (heading,start_line,depth))

        tree = NoteTree(heading, depth) 
        line_no = start_line

        while line_no < len(self.full_note): 
            if debug: print(line_no)
            line = self.full_note[line_no]

            if line.startswith('#'):

                line_dissected = line.strip('\n').split(' ', 1)                       # Convert line to a 2 item list

                if len(line_dissected[0]) == depth+1:
                    if debug: print('Heading matched length')
                    (line_no, new_node) = self.default_parser(line_dissected[1], line_no+1, depth+1) ## Spawn new instance one layer deeper
                    tree.add_leaf(new_node)
                    
                    line_no -= 1

                elif len(line[0]) <= depth:
                    if debug: print('Dropped out of function')
                    break
            else:
                if debug: print('Found plain text: "%s"' % line.strip('\n'))
                tree.append_text(line.strip('\n'))
            
            if re.match(numbered_task_pattern, line) or re.match(bulleted_task_pattern, line):
                tree.add_task(line)

            line_no += 1

        if debug and depth == 0:
            print("Start print")
            tree.print_me()
        return (line_no, tree)


    def transform(self):
        'Perform Operations on the note itself'
        pass

    def export(self):
        'Export data to other part of the tree'
        pass


class LedgerFileObject(FileObject):
    'Base object for all periodic files'
    pass

class DailyFileObject(LedgerFileObject):
    'Object handles data collection from daily notes'

    def __init__(self, note: typing.TextIO):
        super(DailyFileObject, self).__init__(note)
        self.headings = {
                'Apropos'   :   self.default_parser, 
                'Tasks'     :   ['Daily', 'Today\'s Top 9', 'Probablies', 'Non-Priority', 'Unfinished Yesterday'],
                'Musings'   :   self.default_parser,
                'Ideas'     :   self.default_parser,
                'Money'     :   ['Shopping List', 'Spent Today'],
                'Link Dump' :   []
            }


        self.parse()


if __name__ == "__main__":
    sample = open('2024-09-20.md','r')

    daily_note = DailyFileObject(sample)

    print(daily_note.tree.export_md_file())
    
