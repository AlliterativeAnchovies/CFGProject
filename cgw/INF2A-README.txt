Competitive Grammar Writing

September 2017, Shay Cohen


This archive contains the necessary code and files to participate in the competitive grammar writing task in INF2A. Please read README.md thoroughly before you experiment with the code.

Your goal is to change S1.gr so that it covers as much of English as possible, while not generating ungrammatical sentences.

The main driver behind this code is the file pcfg_parse_gen.py.

$ python pcfg_parse_gen.py -h

pcfg_parse_gen.py
        [-h|--help]              # [ ] are optional arguments
        [-v|--verbose level]
        [-s|--start] startsymbol
        [-i|--parse]
        [-r|--prior]             # used with --parse
        [-p|--pruning]           # used with --parse
        [-u|--unseen unseenfile] # used with --parse
        [-b|--beam] beamsize     # used with --parse
        [-o|--generate number]   # use either --parse or --generate
        -g|--grammar file1[,file2,file3,...] or -g|--grammar "*.gr" do *not* use simply *.gr

See README.md to understand how to run it in different modes. The most important modes are: "parse" (to see whether you are able to parse grammatical sentences and not parse ungrammatical ones) and "sample" 
(to see whether your grammar generates grammatical sentences).

Submit your files using the "submit" command on a DICE machine:

$ submit inf2a gr team.txt S1.gr

    team.txt is a list of the UUNs of students who were in that team with their names, one per line. The first line in the file should be a name for the team. For example, here are possible contents of the file:

    The Does
    s144221 Jane Doe
    s123111 John Doe

    S1.gr - the grammar file that you developed. 

The deadline for submission is 12 Nov 2017 at 4:00pm.

Good luck!
