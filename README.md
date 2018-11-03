# ReadMe

## How To Get Started

All scripts are in python2, unfortunately.  So make sure you're using that version.

There are 3 possible tasks you may want to do: compiling your template to a CFG, generating sentences, and checking if the example sentences are in the grammar.  All of this is handled by the 'run.py' wrapper script:

```
	python run.py compile
	python run.py generate
	python run.py check
```

When you first clone this project to your desktop, run all 3 of them to make sure everything works for you!

You should make sure your working directory is ../CFGProject/cgw.  Everything is run from the cgw folder, and if you try to run the script from a different directory then run.py will not be able to find the necessary scripts to compile/generate/check the grammar.

## How To Change The CFG

Instead of working with an ordinary CFG, I've written a script that will convert a "template CFG" into a normal CFG for us.  Exactly what a template is will be explained in the next section.

The only file you should ever need to edit is "CFGTemplate.txt", which is where the template CFG is written.  

*You may potentially also want to edit Vocab.gr, which is inside the innerWorkings folder - if you want to edit Vocab.gr, one of the rules of this project is that we're not allowed to add new words to the vocabulary.  We are only allowed to change the nonterminals and weights in Vocab.gr - any terminal labeled 'Misc' is up for grabs for being labeled, but if it has a different label then don't change it because it's already in use by our CFG.  You can give a vocab word 2 labels if you please.*

I recommend you dive straight into CFGTemplate.txt and poke around, see if you understand what's going on before you read the next section.

After you change CFGTemplate.txt, you need to save it and then compile it, or else generate and check will use the old compiled version.

If you want to see the compiled version, either look at contextExpanderOutput.txt or innerWorkings/S1.gr.  They should have the same contents.

## How Templates Work

Every template is enclosed in curly braces.  It may optionally start with a header or multiple headers. *There is no real point to having a template without a header, but it's important to know that if you enclose something in curly braces the compiler will treat it as a header*

```
{
	<person _1st _2nd _3rd>
	<plurality _Sng _Plr>
	1   Clause       NounPhrase_1st_Sng
	1   Clause       NounPhrase{person}{plurality} VerbPhrase{person}{plurality}
	1   Clause       NounPhrase{person}{plurality}
	1   Clause       NounPhrase{plurality}
}
```

This is an example of a really simple template.  It gets compiled to:

```
	1   Clause       NounPhrase_1st_Sng
	1   Clause       NounPhrase_1st_Sng VerbPhrase_1st_Sng
	1   Clause       NounPhrase_1st_Plr VerbPhrase_1st_Plr
	1   Clause       NounPhrase_2nd_Sng VerbPhrase_2nd_Sng
	1   Clause       NounPhrase_2nd_Plr VerbPhrase_2nd_Plr
	1   Clause       NounPhrase_3rd_Sng VerbPhrase_3rd_Sng
	1   Clause       NounPhrase_3rd_Plr VerbPhrase_3rd_Plr
	1   Clause       NounPhrase_1st_Sng
	1   Clause       NounPhrase_1st_Plr
	1   Clause       NounPhrase_2nd_Sng
	1   Clause       NounPhrase_2nd_Plr
	1   Clause       NounPhrase_3rd_Sng
	1   Clause       NounPhrase_3rd_Plr
	1   Clause       NounPhrase_Sng
	1   Clause       NounPhrase_Plr
```

*Note that the 4th line in the original only corresponds to 2 lines in the output, not 6 like the others, because it does not contain {person} as part of its template.  The compiler will not expand things inside a template unless they need to be.*

*Also note that the 1st line in the original is basically a pre-filled template, which is useful when certain cases have specific features.*

Simple templates like this are just a pattern matching game.  They have a bit more power than that though.

```
{
	<person _1st _2nd _3rd>
	<plurality _Sng _Plr>
	|IGNORE person:_1st|
	|IGNORE person:_2nd plurality:_Plr|
	1   Clause       NounPhrase{person}{plurality} VerbPhrase{person}{plurality}
}
```

becomes

```
	1   Clause       NounPhrase_2nd_Sng VerbPhrase_2nd_Sng
	1   Clause       NounPhrase_3rd_Sng VerbPhrase_3rd_Sng
	1   Clause       NounPhrase_3rd_Plr VerbPhrase_3rd_Plr
```

The ignore header caused all 1st person and all plural 2nd person expansions to not be considered.  This can occasionally be useful - in English, 3rd person singular verbs work differently from all the rest so it may make sense to occasionally exclude them.

*IGNORE statements must come before every production rule, and after all the headers.*

Finally, the most powerful feature of the templates is that of the conditional.

```
{
	<person _1st _2nd _3rd>
	<plurality _Sng _Plr>
	5   Clause   NounPhrase{person}{plurality}$_DirObj?person,plurality=_1st,_Sng:_Subj$
}
```

which compiles to

```
	5   Clause   NounPhrase_1st_Sng_DirObj
	5   Clause   NounPhrase_1st_Plr_Subj
	5   Clause   NounPhrase_2nd_Sng_Subj
	5   Clause   NounPhrase_2nd_Plr_Subj
	5   Clause   NounPhrase_3rd_Sng_Subj
	5   Clause   NounPhrase_3rd_Plr_Subj
```

Conditionals look kind of complicated so here is that conditional broken up:

```
Full Phrase:
	5   Clause   NounPhrase{person}{plurality}$_DirObj?person,plurality=_1st,_Sng:_Subj$
Production Rule:
	Clause  ->  NounPhrase{person}{plurality}$_DirObj?person,plurality=_1st,_Sng:_Subj$
Conditional:
	$_DirObj?person,plurality=_1st,_Sng:_Subj$
In Human Words:
	The conditional evaluates to _DirObj if the template for person evaluates to _1st 
		and simultaneously the template for plurality evaluates to _Sng
	Otherwise the conditional evaluates to _Subj
```

*If it helps, the format is exactly like a ternary statement: A?B:C = A if B else C*
