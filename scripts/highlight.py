#!/bin/python

# Scirpt for highlighting code snippets.
# The only argument is the path to the .html file.
# The output is directed to stdout.

import re
import sys


keywords = {
    'VHDL': [
        'alias', 'all', 'architecture', 'array', 'assert',
        'begin', 'boolean', 'buffer',
        'case', 'constant',
        'downto',
        'elsif', 'else', 'end', 'entity',
        'failure', 'false', 'for', 'function',
        'generate', 'generic',
        'if', 'impure', 'in', 'inout', 'integer', 'is',
        'library', 'loop',
        'natural',
        'of', 'or', 'others', 'out',
        'package', 'port', 'positive', 'process', 'procedure', 'protected', 'pure',
        'range', 'real', 'real_vector', 'record', 'report', 'return',
        'select', 'severity', 'shared', 'signal', 'signed', 'std_logic', 'std_logic_vector', 'std_ulogic', 'std_ulogic_vector', 'string', 'subtype',
        'then', 'time', 'time_vector', 'to', 'true', 'type',
        'unsigned', 'use',
        'variable',
        'wait', 'when', 'with',
    ],
    'C': [
        'auto',
        'break',
        'case', 'char', 'const', 'continue',
        'default', 'do', 'double',
        'else', 'enum', 'extern',
        'float', 'for',
        'goto',
        'if', 'int',
        'long',
        'register', 'return',
        'short', 'signed', 'sizeof', 'static', 'struct', 'switch',
        'typedef',
        'union', 'unsigned',
        'void', 'volatile',
        'while',
        # Not keywords but also highlight
        '#define', '#include', '#ifdef', '#ifndef', '#endif',
        'bool',
        'int8_t', 'int16_t', 'int32_t', 'int64_t',
        'PRIu64',
        'size_t', 'ssize_t',
        'uint8_t', 'uint16_t', 'uint32_t', 'uint64_t',
     ],
}

comment_tokens = {
    'VHDL': '--',
    'C': '//',
}

assert len(sys.argv) == 2, "too many file paths"

in_code = False
lang = None
with open(sys.argv[1]) as file_:
    for line in file_:
        if in_code:
            if line.startswith('</pre>'):
                in_code = False
                print(line, end='')
                continue

            print('<code class="code-line">', end ='')

            code = line
            comment = None
            aux = line.split(comment_tokens[lang], 1)
            if len(aux) == 2:
                code = aux[0]
                comment = aux[1]

            words = re.split(r'(\s+|;|:|\(|\)|=|\+|-|\*|%|\{|\}|\[|\]|\.|,|<|>)', code)
            for word in words:
                if word in keywords[lang]:
                    print("<b>" + word + "</b>", end='')
                elif word == "<":
                    print("&lt", end='')
                elif word == "\n":
                    print("</code>")
                else:
                    print(word, end='')

            if comment is not None:
                print(comment_tokens[lang] + "<i>", end='')
                if comment[-1] == "\n":
                    print(comment[0:-1], end ='')
                else:
                    print(comment, end ='')
                print("</i></code>")

            continue

        if line.startswith('<pre class="code-block'):
            in_code = True
            lang = line.split()[-1].split('"')[0]

        print(line, end='')
