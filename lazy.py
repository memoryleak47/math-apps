#!/usr/bin/env python

import sys
import math

MIN_COMPLEXITY = 0
MAX_COMPLEXITY = 6
ARGS_AMOUNT = 1
TOLERANCE = 0.03

FUNCS = ["($+$)", "($-$)"]
VARS=["1"]

for arg in range(ARGS_AMOUNT):
	VARS.append("args[" + str(arg) + "]")

RULES = list()
RULES.append(([3], 2))
RULES.append(([5], 4))

OVERFLOW=True

def die(string):
	print(string)
	sys.exit()

class FunctionCreator():
	def __init__(self, complexity, counter=0):
		self.complexity = complexity
		self.counter = 0
		self.args = list()
		self.__updateCounter(counter)

	def __updateCounter(self, counter):
		if counter > len(FUNCS)-1:
			die("FunctionCreator::__updateCounter("+str(self.counter)+") outta range for FUNCS")
		self.counter = counter
		self.args = list()
		if self.complexity > 0:
			gotOne = False
			for i in range(len(FUNCS[self.counter])):
				if FUNCS[self.counter][i] == '$':
					if gotOne == False:
						gotOne = True
						self.args.append(FunctionCreator(self.complexity-1))
					else:
						self.args.append(FunctionCreator(0))
		if len(self.args) > 2:
			die("too many args")

	def __increase(self):
		if self.complexity == 0:
			return OVERFLOW
		for arg in self.args:
			if arg.__increase() != OVERFLOW:
				return not OVERFLOW
		if len(self.args) == 2 and self.args[1].complexity != self.complexity-1:
			self.args[0] = FunctionCreator(self.args[0].complexity-1)
			self.args[1] = FunctionCreator(self.args[1].complexity+1)
			return not OVERFLOW
		if self.counter+1 > len(FUNCS)-1: # unsure
			self.__updateCounter(0)
			return OVERFLOW
		self.__updateCounter(self.counter+1)
		return not OVERFLOW

	def __get(self):
		if self.complexity == 0:
			return "$"
		if self.counter > len(FUNCS)-1:
			die("__get(): self.counter("+str(self.counter)+") outta range for FUNCS")
		tmp = FUNCS[self.counter]
		for i in range(len(self.args)):
			spot = tmp.find("$")
			argstr = self.args[i].__get()
			tmp = tmp[:spot] + argstr + tmp[spot+1:]
		return tmp

	def getNext(self):
		return self.__get(), (self.__increase() == OVERFLOW)

def validate(func):
	for rule in RULES:
		args, res = rule
		try:
			if abs(res-eval(func)) > TOLERANCE:
				return False
		except:
			return False
	return True

for complexity in range(MIN_COMPLEXITY, MAX_COMPLEXITY+1):
	print("complexity=" + str(complexity))
	fc = FunctionCreator(complexity)
	while True:
		func, overflow = fc.getNext()

		# insertVars
		varIndexes=list()
		for x in range(func.count("$")):
			varIndexes.append(0)
		while True:
			varfunc = func
			for i in varIndexes:
				varfunc = varfunc[:varfunc.find("$")] + VARS[i] + varfunc[varfunc.find("$")+1:]
			if validate(varfunc):
				print(varfunc)
				sys.exit()
			else:
				checkedAllVars=True
				for i in range(len(varIndexes)):
					if varIndexes[i] == len(VARS)-1:
						varIndexes[i] = 0
					else:
						varIndexes[i] += 1
						checkedAllVars=False
						break
				if checkedAllVars:
					break
		if overflow == OVERFLOW:
			break
print("Game over")
