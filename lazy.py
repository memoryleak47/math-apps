#!/usr/bin/env python

import random
import sys

MAX_COMPLEXITY = 4
MAX_COMPLEXITY_TRIES = 200
MAX_INSERTION_TRIES = 5
ARGS_AMOUNT = 2

RULES = list()
RULES.append(((2, 2), 8))
RULES.append(((3, 2), 18))

ALLOWEDFUNCS = ["max($,$)", "min($,$)", "$*$", "float($)/float($)", "$+$", "$-$", "($+$)", "($-$)"]

def getRandomFunc():
	return ALLOWEDFUNCS[random.randint(0, len(ALLOWEDFUNCS)-1)]

def insertAt(insertion, index, string):
	return string[:index] + insertion + string[index+1:]

def insertAtRandomPoint(insertion, string):
	l = list()
	for x in range(len(string)):
		if string[x] == '$':
			l.append(x)
	if len(l) == 0:
		print("insertAtRandomPoint: NOPE")
		return
	return insertAt(insertion, l[random.randint(0, len(l)-1)], string)

def insertRandom(string):
	return insertAtRandomPoint(getRandomFunc(), string)

def validate(func):
	for rule in RULES:
		args, res = rule
		if eval(func) != res:
			return False
	return True

def insertVars(func):
	while "$" in func:
		func = insertAtRandomPoint("args[" + str(random.randint(0, ARGS_AMOUNT-1)) + "]", func)
	return func

# increase complexity
for complexity in range(1, MAX_COMPLEXITY):
	print("complexity=" + str(complexity))
	# try
	for tries in range(MAX_COMPLEXITY_TRIES):
		func="$"
		# insertRandom
		for i in range(complexity):
			func = insertRandom(func)
			# insertVars
			for x in range(MAX_INSERTION_TRIES):
				varfunc = insertVars(func)
				if validate(varfunc):
					print(varfunc)
					sys.exit()
