###########################################
#   Author: Ahmad M. Osman
#   Date: 10/23/2017
#
#   Class: CS 260
#   Instructor: Dr. Kent Lee
#
#   File name: ahmad-main.py
#   Purpose: Infix Evaluator
###########################################


import sys
import stack
import nfastate
import streamreader
import orderedcollections

epsilon = "EPSILON"

##########################################################################
# You should use the Operator class in your code for each of the regular
# expression operators. The precedence function will give you the
# precedence of each regular expression operator.
##########################################################################


class Operator:

    def __init__(self, op):
        self.op = op

    def precedence(self):
        if self.op == "|":
            return 1
        if self.op == ".":
            return 2
        if self.op == "*":
            return 3
        if self.op == "(" or self.op == ")":
            return 0

    def getOpChar(self):
        return self.op


class NFA:

    def __init__(self, classes={epsilon: orderedcollections.OrderedSet()}, states=orderedcollections.OrderedMap(), keywords=orderedcollections.OrderedMap(), tokens=orderedcollections.OrderedMap(), firstTokenId=-1):
        self.classes = orderedcollections.OrderedMap(classes)
        self.states = orderedcollections.OrderedMap(states)
        self.numStates = len(states)
        self.keywords = orderedcollections.OrderedMap(keywords)
        self.tokens = orderedcollections.OrderedMap(tokens)
        self.firstTokenId = firstTokenId

    def __repr__(self):
        return ("NFA(" + repr(self.classes) + "," + repr(self.states) + "," + repr(self.keywords) + "," + repr(self.tokens) + "," + repr(self.firstTokenId) + ")")

    def getFirstTokenId(self):
        return self.firstTokenId

    def buildMachine(self, instream):

        #######################################################################
        # The newState function should be called to create any new state. It enters
        # the state information into the self.states dictionary for use later. Then
        # it returns the state Id (its state number) of the newly created state.
        #######################################################################

        def newState():
            self.numStates += 1
            aState = nfastate.NFAState(self.numStates)
            self.states[self.numStates] = aState
            return self.numStates

        #######################################################################
        # The operate function is given an:
        #   op : the operator
        #
        #   opStack: the stack of operators
        #
        #   stateStack: the stack of first,last states (which is the operand stack)
        #   the function does not return anything. Instead it operates on the two
        #   stacks as described in the two stack calculator algorithm.
        #
        # For each new state be sure to call the newState() function to enter
        # the new state in the self.states dictionary correctly.
        #######################################################################

        def operate(op, opStack, stateStack):
            precedence = {'(': 0, '|': 1, '.': 2, '*': 3, ')': 0}

            if op == '(':
                opStack.push(op)
                return None
            elif opStack.isEmpty():
                return None
            else:
                topOp = opStack.pop()
                opStack.push(topOp)
                while precedence[op] <= precedence[topOp]:
                    topOp = opStack.pop()
                    if topOp == '*':
                        q0ID, q1ID = stateStack.pop()

                        startStateID = newState()
                        endStateID = newState()
                        startState = self.states[startStateID]
                        endState = self.states[endStateID]

                        q0 = self.states[q0ID]
                        q1 = self.states[q1ID]

                        startState.addTransition(epsilon, q0ID)
                        startState.addTransition(epsilon, q1ID)
                        q1.addTransition(epsilon, endStateID)
                        endState.addTransition(epsilon, startStateID)

                        stateStack.push((startStateID, endStateID))

                    elif topOp == '.':
                        q0ID, q1ID = stateStack.pop()

                        startStateID = newState()
                        endStateID = newState()
                        startState = self.states[startStateID]
                        endState = self.states[endStateID]

                        q0 = self.states[q0ID]
                        q1 = self.states[q1ID]

                        startState.addTransition(epsilon, q0ID)
                        q1.addTransition(epsilon, endStateID)

                        stateStack.push((startStateID, endStateID))

                    elif topOp == '|':
                        q0ID, q1ID = stateStack.pop()
                        q2ID, q3ID = stateStack.pop()

                        startStateID = newState()
                        endStateID = newState()
                        startState = self.states[startStateID]
                        endState = self.states[endStateID]

                        q0 = self.states[q0ID]
                        q1 = self.states[q1ID]
                        q2 = self.states[q2ID]
                        q3 = self.states[q3ID]

                        q1.addTransition(epsilon, endStateID)
                        q3.addTransition(epsilon, endStateID)
                        startState.addTransition(epsilon, q0ID)
                        startState.addTransition(epsilon, q2ID)

                        stateStack.push((startStateID, endStateID))

                    elif topOp == '(':
                        return None

                opStack.push(op)

        #######################################################################
        # The evaluateRegExpression function is given the StreamReader called
        # reader and reads the regular expression and returns a tuple of start,stop state
        # for the expression. The stop state will be set to an accepting state by the code
        # that calls this function. When this function is called the regular expression must be
        # read. For instance in the line
        #
        # identifier = letter.(letter|digit)*;
        #
        # everything up to the = has already been read. You need to write code to read the
        # regular expression up to the semicolon (i.e. ;) and then run your regular expression
        # calculator code on it to build an NFA from this. To create each new state be sure to call
        # the newState() function to create it so the state gets entered into the self.states dictionary
        # correctly.
        #######################################################################

        def evaluateRegExpression(reader):
            operatorStack = stack.Stack()
            operandStack = stack.Stack()
            operatorStack.push('(')

            token = reader.getToken()
            while token != ';':
                if token in "(|.*":
                    operate(token, operatorStack, operandStack)
                else:
                    startStateID = newState()
                    endStateID = newState()
                    startState = self.states[startStateID]
                    endState = self.states[endStateID]

                    startState.addTransition(token, endStateID)
                    operandStack.push((startStateID, endStateID))

                token = reader.getToken()

            operate(')', operatorStack, operandStack)
            startStateID, endStateID = operandStack.pop()
            reader.unreadChar(';')
            return startStateID, endStateID

        ####################################################
        # This is the start of the buildMachine code here
        ####################################################

        reader = streamreader.StreamReader(instream)
        startStates = []

        reader.skipComments()

        if reader.peek("#CLASSES"):
            # print("Found #CLASSES")
            reader.readUpTo("\n")
            while (not reader.peek("#")):
                # The "#" marks the beginning of the next section. Either
                # KEYWORDS or TOKENS. KEYWORDS are optional.
                reader.skipComments()

                # We could have keywords right after a comment. So if keyword section is found, don't read
                # any more character classes.
                if not reader.peek("#KEYWORDS"):
                    className = reader.readIdentifier()
                    reader.readUpTo("=")
                    if reader.peek("^"):
                        anticlass = True
                        reader.readUpTo("^")
                        classSet = orderedcollections.OrderedSet(range(256))
                    else:
                        anticlass = False
                        classSet = orderedcollections.OrderedSet()

                    done = False

                    while not done:

                        if reader.peek("'"):
                            # Found a character constant
                            reader.readUpTo("'")
                            character = reader.readUpTo("'")[0]
                            # print(character)
                            ordVal = ord(character)

                        else:
                            ordVal = reader.readInt()

                        # Add the end of the range if there is a range of
                        # characters
                        if reader.peek(".."):
                            reader.readUpTo("..")

                            if reader.peek("'"):
                                reader.readUpTo("'")
                                character = reader.readUpTo("'")[0]
                                # print(character)
                                lastOrdVal = ord(character)
                            else:
                                lastOrdVal = reader.readInt()
                        else:
                            lastOrdVal = ordVal

                        # Now build the set
                        for i in range(ordVal, lastOrdVal + 1):
                            if anticlass:
                                classSet.remove(i)
                            else:
                                classSet.add(i)

                        if reader.peek(","):
                            reader.readUpTo(",")
                        else:
                            done = True

                    # print(className)

                    # Add the class to the class dictionary
                    self.classes[className] = classSet

                    reader.readUpTo(";")

        #print("These are the classes")
        # print(self.classes)
        # keyword and token id numbers
        idnum = 0
        keywordsPresent = False

        if reader.peek("#KEYWORDS"):
            reader.readUpTo("#KEYWORDS")
            keywordsPresent = True
            reader.skipComments()

            while (not reader.peek("#TOKENS")):
                #idnum = reader.readInt()
                # reader.readUpTo(":")
                reader.readUpTo("'")
                keyword = reader.readUpTo("'")[:-1].strip()
                # print(idnum,keyword)
                self.keywords[keyword] = idnum
                idnum += 1
                reader.readUpTo(";")
                reader.skipComments()

        # print(self.keywords)
        reader.readUpTo("#TOKENS")
        reader.skipComments()
        readingFirstToken = True

        while not (reader.peek("#PRODUCTIONS") or reader.peek("#END") or reader.peek("#DEFINITIONS")):
            #idnum = reader.readInt()
            # reader.readUpTo(":")
            if reader.peek("'"):
                # Then the token was specified as a string like this:
                # '>=';
                reader.readUpTo("'")
                token = reader.readUpTo("'")[:-1].strip()
                previousId = newState()
                startStateId = previousId

                for c in token:
                    nextId = newState()
                    classSet = orderedcollections.OrderedSet([ord(c)])
                    if not (c in self.classes and self.classes[c] == classSet):
                        self.classes[c] = classSet
                    self.states[previousId].addTransition(c, nextId)
                    previousId = nextId

                self.states[nextId].setAccepting(idnum)
                startStates.append(startStateId)
                reader.readUpTo(";")
                self.tokens[idnum] = token
                idnum += 1
                if readingFirstToken and keywordsPresent:
                    raise Exception(
                        "First Token must be identifier token for matching keywords!")

            else:
                # The token was specified as a regular expression like this:
                # identifier = letter.(letter|digit)*;

                name = reader.readUpTo("=")[:-1].strip()
                self.tokens[idnum] = name
                if readingFirstToken:
                    self.firstTokenId = idnum
                    readingFirstToken = False

                # You must write the evaluateRegExpression(reader) function
                # that reads a regular expression using the reader StreamReader
                # object and returns its start and stop state ids.
                startStateId, stopStateId = evaluateRegExpression(reader)

                self.states[stopStateId].setAccepting(idnum)
                idnum += 1
                startStates.append(startStateId)

                reader.readUpTo(";")
                reader.skipComments()

        # Create a 0th State as the start state
        startState = nfastate.NFAState(0)
        self.numStates += 1
        self.states[0] = startState

        for startId in startStates:
            self.states[0].addTransition(epsilon, startId)

        self.startStateId = 0

        reader.readUpTo("#END")

    def writeListing(self, outStream):

        outStream.write("The NFA CREATED FOR THE REGULAR EXPRESSIONS IS:\n\n")

        outStream.write("The start state is: " +
                        str(self.startStateId) + "\n\n")

        outStream.write("STATE           ON CLASS         GO TO     ACCEPTS\n")
        outStream.write("-----           --------         -----     -------\n")

        for stateId in range(self.numStates):
            if self.states[stateId].isAccepting():
                acceptsId = self.states[stateId].getAcceptsTokenId()
                tokenName = self.tokens[acceptsId]
            else:
                tokenName = ""

            outStream.write("%5d %44s\n" % (stateId, tokenName))

            trans = self.states[stateId].getTransitions()

            for onClass in trans:
                toStateIds = trans[onClass]
                for toStateId in toStateIds:
                    outStream.write("%28s     %5d\n" % (onClass, toStateId))

            outStream.write("\n")


def main():

    filename = "jpython.txt"

    instream = open(filename, 'r')

    nfa = NFA()
    nfa.buildMachine(instream)
    nfa.writeListing(sys.stdout)


if __name__ == "__main__":
    main()
