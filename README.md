# ReadMe

## Basics
I will summarize how this project works - you should also read the 2 ReadMe files written by our lecturer, in the cgw folder (everything is in the cgw folder).

The goal is to create a CFG (Context Free Grammar) that generates as many grammatical English sentences as possible while generating very few ungrammatical sentences.  There are 2 sides to this project: generating random sentences, and checking if a given sentence is inside the grammar.

### Generating Random Sentences
|   python pcfg_parse_gen.py -o 20 -g S1.gr,Vocab.gr

This line of code runs the sentence generator.  This is self explanatory.  Keep an eye out for ungrammatical sentences!


### Checking Sentences
|   python pcfg_parse_gen.py -i -g "*.gr" < example_sentences.txt

This line of code runs the sentence checker on every sentence in example_sentences.txt

You are allowed to add more to example_sentences, but let's avoid that until our parser
correctly parses every single sentence already given to us (harder than it looks...)

If a sentence is not parsed, it looks like this:
#No parses found for: when the king drinks , Patsy drinks .
(TOP (X when) (X the) (X king) (X drinks) (X ,) (X Patsy) (X drinks) (X .))

If a sentence is parsed, if gives the parse tree in this ungodly mess:

(TOP (S1 (QuestionClause (QuestionClauseInner (QuestionClause1 (wrap_do do) (DoConstruction (NounPhrase_3rd_Plr_Subj (SimpleNounPhrase_3rd_Plr_Subj (ProperStuffs_Plr (Noun_3rd_Plr (Noun_p coconuts) ) ) ) ) (VerbPhrase_inf (Verb_inf (Verb_inf_Transitive speak) ) ))) ) (EOS_Question ?)) ) )

For reference - this is the parse tree for "do coconuts speak ?"

Later on when we try to eliminate ungrammatical sentences, this may be useful as it lets us see exactly why the CFG thinks it should work.  It may be worth writing another python script to take these parse trees in and spit out a more readable version (perhaps by drawing it as a tree rather than printing a string)

You need to use python2.7 to run those two lines of code!  I set up an anaconda environment for it.
If you don't know what anaconda is, you should install it - it allows you to have multiple versions of
python on your computer, which you'll see is important later on because contextExpander.py runs on python3

## Rules

Please read the teacher's readme's for full familiarity with the rules.  There should be no problem if you only edit "precompiledS1V2.txt" though (that is the file that we use contextExpander.py on to generate our grammer, which is saved in S1.gr)

## What The Grammar Looks Like And How To Get Started

For this, I will post a segment of the code:

```
###Wrappers
{
	<wordlist1 is of to the does do what who whose how when where why>
	<wordlist2 that so either neither or nor are at have has than am ,>
	<questionWords where when why how>
	<qwt who what>

	1   wrap_{wordlist1}        {wordlist1}
	1   wrap_{wordlist2}        {wordlist2}
	1   QuestionWord            {questionWords}
	1   QuestionWord_Transitive {qwt}
}
```

This is a 'weighted grammar'.  Each normal line is broken into 3 parts - the weight and the 2 sides of the production rule.

So `1   wrap_{wordlist1}        {wordlist1}` is broken into 1, wrap_{wordlist1},{wordlist1} and it means that there is a production rule wrap_{wordlist1} -> {wordlist1} and that this rule has weight 1.  A more abstract example would be:

```
2   A   B C
10  A   D
```

Which gives us A->BC and A->D.  A->D is 5 times as likely to be used in the generation process compared to A->BC, because it's weight is 10 compared to A->BC's 2.  By default, you should leave weights at 1 unless you are debugging and want to make sure that the sentence generator always generates sentences of the type you want, or if you have a rule like A->AA, in which case you should make it considerably less likely than other production rules because we want to avoid infinite recursion!

The grammar is in Chomsky Normal form, so every production rule can have at most 2 nonterminals on the right hand side.
