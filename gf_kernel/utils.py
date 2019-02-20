def to_display_data(message,omdoc=None):
    """wraps the message into the display_data format"""
    if(omdoc):
        return {
            'data': {
                'text/plain': message,
                'application/omdoc' : omdoc
            },
            'metadata': {},
            'transient': {},
        }
    else:
        return {
            'data': {
                'text/plain': message,
            },
            'metadata': {},
            'transient': {}
        }

def readFile(fn, cursor_pos=0):
    """Reads the file with name `fn` starting at `cursor_pos`"""
    fd = open(fn, 'r')
    fd.seek(cursor_pos)
    line = fd.readline()
    out = ""
    while line:
        if line != '\n':
            out += line
        line = fd.readline()
    fd.close()
    return out



commonKeywords = ["flags", "startcat", "cat", "fun", "of", "lin", "lincat", "with",
                  "open", "in", "param", "linref", "table", "let", "case", "overload"]
commonBuiltins = ["Phrase", "Item", "Kind", "Quality", "Item"]
commonDefiners = ["abstract", "concrete", "resource",
                  "incomplete", "instance", "interface"]
GFshellCommands = ["abstract_info", "ai", "align_words", "al", "clitic_analyse", "ca", "compute_conctete", "cc",
                   "define_command", "dc", "depencency_graph", "dg", "define_tree", "dt", "empty", "e", "example_based", "eb",
                   "execute_history", "eh", "generate_random", "gr", "generate_trees", "gt", "help", "h", "import", "i",
                   "linearize", "l", "linearize_chunks", "lc", "morpho_analyse", "ma", "morpho_quiz", "mq", "parse", "p",
                   "print_grammar", "pg", "print_history", "ph", "put_string", "ps", "put_tree", "pt", "quit", "q", "reload",
                   "r", "read_file", "rf", "rank_trees", "rt", "show_dependencies", "sd", "set_encoding", "se", "show_operations",
                   "so", "system_pipe", "sp", "show_source", "ss", "translation_quiz", "tq", "to_trie", "tt", "unicode_table",
                   "ut", "visualize_dependency", "vd", "visualize_parse", "vp", "visualize_tree", "vt", "write_file", "wf"]
kernelCommands = ["view", "clean"]
commonCommands = GFshellCommands + kernelCommands


def parse(code):
    lines = code.split('\n')
    parseDict = {
        'type': None,
        'grammar_name': None,
        'commands': []
    }
    isContent = False
    for line in lines:
        words = line.split(' ')
        lastWord = ''
        for word in words:
            if word in commonDefiners:
                isContent = True
                lastWord = word
                continue
            if isContent and word not in commonDefiners and lastWord in commonDefiners:
                parseDict['type'] = 'content'
                parseDict['grammar_name'] = word
                parseDict['commands'] = []
                return parseDict
            if not isContent and word in commonCommands and word == words[0]:
                command = {
                    'name': word,
                    'args': ' '.join(words[1:])
                }
                parseDict['type'] = 'commands'
                parseDict['commands'].append(command)

    return parseDict