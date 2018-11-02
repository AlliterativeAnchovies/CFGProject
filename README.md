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

Nonterminals can have names that use nonalphanumeric characters, by the way!  Just don't use |,<,{,},∂,or #.
```
# is comments
∂ is a special token used by contextExpander.py mid-generation
< and | are special tokens that will be explained next section
{ and } can be used but only in circumstances explained next section
```

## Next Section (AKA How to use templates to your advantage)

The problem with CFGs is that they're context free.  Consider the sentence "It is Sir Lancelot who knows the truth ."  This may seem like a benign sentence, but it's hard for a CFG to parse - "knows" is conjugated according to "Sir Lancelot" - that is, "knows" needs context provided by "Sir Lancelot" *Even though they are in different clauses!!!*

How do we pass this context along?  Well, we can add tags to our nonterminals.  Instead of 1 nonterminal `Clause -> NounPhrase VerbPhrase`, which is in danger of having the VerbPhrase use an incorrectly conjugated verb with respect to the NounPhrase, we can have multiple:

```
Clause -> NounPhrase_1st_Sng VerbPhrase_1st_Sng
Clause -> NounPhrase_2nd_Sng VerbPhrase_2nd_Sng
Clause -> NounPhrase_1st_Plr VerbPhrase_1st_Plr
...etc
```

If we want to have all possible combinations of (1st,2nd,3rd) person and plural/singular, we need to write out the same thing 6 times!  That's inefficient, but there's no way around it - the CFG *must* expand exponentially with every tag introduced.  A human can't keep up - but a computer can.  We can express the aforementioned production rule succinctly as `Clause -> NounPhrase{person}{plurality} VerbPhrase{person}{plurality}` where person ranges over (1st,2nd,3rd) and plurality over (plural,singular).  I wrote a script, contextExpander.py, to take these rules and produce all the required production rules based on a template.  Here is how you would express it in actual code:

```
{
	<person _1st _2nd _3rd>
	<plurality _Sng _Plr>
	Clause -> NounPhrase{person}{plurality} VerbPhrase{person}{plurality}
}
```

If for some reason you wanted your phrase to loop through everything but specifically 1st person plural:

```
{
	<person _1st _2nd _3rd>
	<plurality _Sng _Plr>
	|IGNORE _1st _2nd|
	Clause -> NounPhrase{person}{plurality} VerbPhrase{person}{plurality}
}
```

And finally, if you also had nonterminals of the form `NounPhrase{person}` and `VerbPhrase{person}`, so you wanted to sometimes ignore plurality altogether (aka replace {plurality} with the empty string):

```
{
	<person _1st _2nd _3rd>
	<plurality _Sng _Plr ε>
	|IGNORE _1st _2nd|
	Clause -> NounPhrase{person}{plurality} VerbPhrase{person}{plurality}
}
```

Note that the underscores on 1st,2nd,3rd are not required but I think it makes the resultant code more readable.  If you're still not sure how to use this, look at "precompiledS1V2.txt" to see real world examples of their use, and "contextExpanderOutput.txt" to see what the compiled, un-templated code looks like.

Warning: make sparing use of IGNORE commands.  I'm pretty sure I could write production rules that will not change like expected using IGNOREs, because of the way I programmed it.  I don't think you would write one by accident, but it is definitely possible. (the fix would make the contextExpander.py a lot more complicated so I'm not going to bother unless it becomes a problem - don't worry too much, I don't think it'll be a problem.  Just don't try to push them to the limit.)

### Actually Running The Template Code!

|   python contextExpander.py precompiledS1V2.txt

This will take template code in precompiledS1V2.txt, compile it into an actual CFG, and then save the result in S1.gr and contextExpanderOutput.txt.  (there is a weird error where, at least on my mac, S1.gr will not open in TextEdit because TextEdit thinks it is corrupted, even though it can be used fine to generate sentences and whatnot.  So if you want to see what your code compiled to, contextExpanderOutput.txt is your best bet.)

One problem: contextExpander.py is in python3...  And the other scripts are in python2.  I'd like them to all be the same, but python2 file input reading is apparently harder than python3 so I didn't want to deal with it XD (and it's the teacher's scripts that are in py2 so I don't want to make those py3.)  I use anaconda (I mentioned earlier) to deal with this discrepancy.  Your computer should be able to use both at once though - maybe write python2 and python3 instead of just python to specify? (not sure, haven't tested).  Feel free to convert contextExpander.py in your own time.

## How We Can Colaborate On This

I've already split up the CFG into 3 sections - Clauses, Noun Phrases, Verb Phrases.  As we go on these may get split further.  But they're all very self contained so we can work on them seperately.  It's not set in stone which one you have to work on, but you should only change 1 inbetween commits.  That way merge conflicts are easy to deal with.

Please comment your CFG.  I'm also enforcing a bit of Object-Oriented-Programming standards - every section should be thought of as an object, and it has private and public production rules.  At the start of each section, these should be put in plain view.

```
	##########################################################################
	#									 #	
	#   Global Nonterminals: QuestionClause, StatementClause, SimpleClause   #
	#								         #
	#############################################################################
	#StatementClause takes no arguments					    #
	#QuestionClause takes no arguments					    #
	#SimpleClause takes either no arguments or (person,plurality)	            #
	#	if no arguments, it will pick an arbitrary (person,plurality) pair. #
	#############################################################################
```

This is an example of the header for the Clause section that states which Nonterminals are allowed to be used by other sections if they so please.  Here, arguments refer to templates.  So basically SimpleClause looks like either `SimpleClause` or `SimpleClause{person}{plurality}` - templates can be thought of as functions.

### This was a mouthful!
#### I'm tired
##### Bye now!
