import typing
import sys

from typing import Optional

class NoteTree:
    'Here we will include the code for parsing a particular heading'
    heading_name = ''
    bare_text = ''

    subheadings: list[Optional['NoteTree']] = []

    def __init__(self, heading_name):
        self.heading_name = heading_name

    def __str__(self):
        current_node_str = f'''{self.heading_name}:\n{self.bare_text}\n\n'''

        return current_node_str

    def append_text(self, new_text: str):
        self.bare_text += new_text

    def add_leaf(self, leaf: Optional['NoteTree']):
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

        self.tree = self.default_parser('root',0,0)


    def default_parser(self, heading, start_line, depth):

        tree = NoteTree(heading) 

        current_node = tree

        line_no = start_line

        while line_no < len(self.full_note):
            line = self.full_note[line_no]
            line = line.strip('\n').split(' ', 1)                       # Convert line to a 2 item list

            if line[0].startswith('#'):
                current_node = NoteTree(line[1])
                tree.add_leaf(current_node)
            
            line_no += 1


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
    sample = open('sample.md','r')

    daily_note = DailyFileObject(sample)
