# ReadMe

## How To Get Started

All scripts are in python2.  So make sure you're using that version.

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

Every line in the CFG, ignoring special template lines, looks something like this:

```
1   Clause       NounPhrase_1st_Sng VerbPhrase_1st_Sng
```

This represents the production rule

```
Clause -> NounPhrase_1st_Sng VerbPhrase_1st_Sng
```

and that specific rule has weighting 1.  If we had:

```
10  Clause       NounPhrase_1st_Sng VerbPhrase_1st_Sng
2   Clause       NounPhrase_2nd_Plr VerbPhrase_2nd_Plr
```

then the first rule would be 5 times as likely to be used in the random sentence generator.

One final consideration is that the grammar must be written in Chomsky Normal Form

## How Templates Work

Every template is enclosed in curly braces.  It may optionally start with a header or multiple headers. *There is no real point to having a template without a header, but it's important to know that if you enclose something in curly braces the compiler will treat it as a template*

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

*Final note: if a template contains ε (epsilon), instead of literally placing ε, it will place the empty string.*

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

*IGNORE statements must come before the production rules, and after the headers.*

Finally, the most powerful feature of the templates is that of the conditional.

```
{
	<person _1st _2nd _3rd>
	<plurality _Sng _Plr>
	5   Clause   NounPhrase{person}{plurality}$person,plurality=_1st,_Sng?_DirObj:_Subj$
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
	5   Clause   NounPhrase{person}{plurality}$person,plurality=_1st,_Sng?_DirObj:_Subj$
Production Rule:
	Clause  ->  NounPhrase{person}{plurality}$person,plurality=_1st,_Sng?_DirObj:_Subj$
Conditional:
	$person,plurality=_1st,_Sng?_DirObj:_Subj$
In Human Words:
	The conditional evaluates to _DirObj if the template for person evaluates to _1st 
		and simultaneously the template for plurality evaluates to _Sng
	Otherwise the conditional evaluates to _Subj
```

*If it helps, the format is like a ternary statement: A?B:C = B if A else C*

There aren't too many situations where you should need this.  The example I gave here is actually in use in the code, though (albeit in a slightly more complicated fashion).  This is because "I and You" sounds wrong but "Me and You" is right.  However "He and I" still sounds correct and "Him and I" does not for the most part (depends on circumstance).  I and He are subject pronouns, Me and Him are direct object pronouns.  There is a specific rule for what sounds right or wrong, but the rule is the exact opposite for I and Me, hence why the conditional is specifically changing the 1st person singular noun phrase.  If that all sounds like gobbledygook, I wrote out the full reasoning in the neither/either section of the code.  Just cmnd-f/ctrl-f to `### Clauses continued: Either/Neither ###` to see it.

## Final Considerations

I have tried to make our template model an object oriented system.  None of what I am about to say is enforced by the compiler, but I think we should adhere to the following standards so that we can work together seemlessly:

We should think of each template as an object, and each production rule as a function:

```
{ ### Random Verb Phrases
	<person _1st _2nd _3rd>
	<plurality _Sng _Plr>
	1      RandomVerbPhrase        VerbPhrase{person}{plurality}
	1      VerbPhrase{person}{plurality} SomeProductionRule
}
```

Here, "Random Verb Phrases" is an object, and it contains 2 functions - RandomVerbPhrase() and VerbPhrase(person,plurality).

Every object of sufficient complexity should have a header at the top, saying which functions are intended to be accessible by other objects (think private/public).  Here is an example of the header to the NounPhrase section taken straight from the current code:

```
### Noun Phrases ###=====================================================================================
{
	<person _1st _2nd _3rd>
	<plurality _Sng _Plr>
	<role _Subj _DirObj _IndObj>
	<transitivity _Transitive _Intransitive>
	#######################################################################
	#								      #
	#   Global Nonterminals: NounPhrase, SimpleNounPhrase, GerundPhrase   #
	#								      #
	###########################################################################
	#NounPhrase takes either no arguments, (role), or (person,plurality,role) #
	#	if no arguments, it picks a random (person,plurality,role)        #
	#	if (role), it picks a random (person,plurality).		  #
	#SimpleNounPhrase behaves like NounPhrase				  #
	#GerundPhrase takes no arguments			 	          #
	###########################################################################
	
	/*Code Here*/
	
}
```

By adopting this object oriented approach, we can each work on different objects without worrying about merge conflicts!  So even though the compiler doesn't enforce this, I will enforce it.

## Reserved Symbols

Nonterminals can be composed of any symbol you want - they don't have to be alphanumeric!  However, certain symbols have special meanings for templates, so if you are not specifically using them as part of template code, you should avoid using the following symbols:

```
{
}
<
>
|
∂ #Very Bad
ε #Badish
$ #Extremely Bad
?
:
,
```

Not all of them will probably cause problems, I labeled the ones that I think are extremely likely to cause a problem so if you have to use them for whatever reason, don't use the labeled ones.

*You can use them all outside of template blocks though.*
