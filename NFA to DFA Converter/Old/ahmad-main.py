###########################################
#   Author: Ahmad M. Osman
#   Date: 9/27/2017
#   File name: ahmad-main.py
#   Class: CS 260
#   Instructor: Dr. Kent Lee
#   Purpse: NFA to DFA Converter
###########################################


import sys
import stack
import state
import nfastate
import streamreader
import orderedcollections


epsilon = "epsilon"


class NFA:

    def __init__(self, classes, states):
        self.states = states
        self.classes = classes


class DFA:

    def __init__(self, classes=orderedcollections.OrderedMap(), states=orderedcollections.OrderedMap()):
        self.classes = orderedcollections.OrderedMap(classes)
        self.states = orderedcollections.OrderedMap(states)
        self.numStates = len(states)

    def __repr__(self):
        return ("DFA(" + repr(self.classes) + "," + repr(self.states) + ")")

    def buildFromNFA(self, nfa):
        def newState():
            ''' Add a new state to the map of stateIds to states in the state map.
                                Return the new state id.'''

            new_State = state.State(self.numStates)
            self.states[self.numStates] = new_State
            self.numStates += 1
            return new_State.getId()

        def getAcceptingTokenId(stateSet):
            ''' Return the first accepting tokenId found in the NFA state set.
                        Otherwise, return None '''

            for stateid in stateSet:
                condition = nfa.states[stateid].isAccepting()
                if condition:
                    self.tokens[condition] = "Yes"
                    return nfa.states[stateid].getAcceptsTokenId()

            return None

        def EPSclosure(stateSet):
            ''' Add to the closure set all NFA state Ids that are
                        in the epsilon closure of this stateSet. Then
                        return the OrderedFrozenSet of this closure set.'''

            closureSet = orderedcollections.OrderedSet(stateSet)
            unexploredStates = orderedcollections.OrderedSet(stateSet)

            while len(unexploredStates) != 0:
                stateID = unexploredStates.pop()
                toStates = nfa.states[stateID].onClassGoTo(epsilon)

                # Depth-First Search
                for toStateID in toStates:
                    if toStateID not in closureSet:
                        closureSet.add(toStateID)
                        unexploredStates.add(toStateID)

            return orderedcollections.OrderedFrozenSet(closureSet)

        def nfaTransTo(fromStates, onClass):
            ''' Return the epsilon closure of the set of NFA states that
                        you can get to on the class of characters (i.e. onClass) from
                        this set of fromStates.'''

            toStates = orderedcollections.OrderedSet()

            for fromStateID in fromStates:
                toStates.update(nfa.states[fromStateID].onClassGoTo(onClass))

            return orderedcollections.OrderedSet(EPSclosure(toStates))

        def gatherClasses(states):
            ''' Return the set of classes of transitions (i.e. classes of characters)
                        that are possible transitions from this set of NFA states.'''

            gatheredClasses = orderedcollections.OrderedSet()

            for stateID in states:
                transitions = nfa.states[stateID].getTransitions()
                for onClass in transitions:
                    if onClass != epsilon:
                        gatheredClasses.add(onClass)

            return gatheredClasses

        # This is the beginning of the buildFromNFA method.
        # Copy over the classes
        self.classes = nfa.classes

        # Create the start state and the DFA to NFA stateMap.
        self.startStateId = newState()
        stateMap = orderedcollections.OrderedMap()

        # Form the epsilon closure of the NFA start state (i.e. state 0) and then
        # map the start state of the DFA to the start state set of the NFA
        EPSstartState = EPSclosure(
            orderedcollections.OrderedSet([self.startStateId]))
        stateMap[self.startStateId] = EPSstartState

        ##########

        ##letters = gatherClasses(stateMap[self.startStateId])
        ##for letter in letters:

            #toStates = orderedcollections.OrderedSet()

            #for stateIDX in stateMap[self.startStateId]:
                #toStates.update(nfa.states[stateIDX].onClassGoTo(letter))

            #for trans in toStates:
                #self.states[self.startStateId].addTransition(letter, trans)

        ###########

        # Keep track of the new DFA states. The first new DFA state is the start
        # state. You can keep track of this as an ordered set or a stack if you
        # wish.
        unexploredStates = orderedcollections.OrderedSet([self.startStateId])

        # Map the set of nfa state ids (as a frozen set) to the new DFA state id in the
        # nfa2dfa map.
        nfa2dfa = orderedcollections.OrderedMap()
        nfa2dfa[EPSstartState] = self.startStateId

        # set the new DFA state to accepting if the NFA states contained an accepting state.
        # You can use the getAcceptingTokenId function for this.
        self.tokens = orderedcollections.OrderedMap()

        while len(unexploredStates) > 0:
            currentStateID = unexploredStates.pop()
            letters = gatherClasses(stateMap[currentStateID])
            for letter in letters:
                transitionsTo = orderedcollections.OrderedFrozenSet(
                    nfaTransTo(stateMap[currentStateID], letter))
                if transitionsTo not in nfa2dfa:
                    toDFAStateID = newState()
                    stateMap[toDFAStateID] = transitionsTo
                    nfa2dfa[transitionsTo] = toDFAStateID
                    if getAcceptingTokenId(transitionsTo):
                        self.states[toDFAStateID].setAccepting(True)
                    unexploredStates.add(toDFAStateID)
                else:
                    toDFAStateID = nfa2dfa[transitionsTo]

                self.states[currentStateID].addTransition(letter, toDFAStateID)

        # While there are no more unexplored states in the new DFA state set, follow the algorithm
        # given on the website by using the nfaTransTo function and creating new DFA states for each
        # new set of NFA states that are found by using gatherClasses. Remember to set accepting states
        # in the DFA as you proceed.

    def writeListing(self, outStream):
        ''' The writeListing method is provided assuming you used the correct data structures
                in your code.'''

        outStream.write("The start state is: " +
                        str(self.startStateId) + "\n\n")

        outStream.write("STATE     ON CLASS     GO TO     ACCEPTS\n")
        outStream.write("-----     --------     -----     -------\n")

        for stateId in range(self.numStates):
            if self.states[stateId].isAccepting():
                acceptsId = self.states[stateId].getAcceptsTokenId()
                tokenName = self.tokens[acceptsId]
            else:
                tokenName = ""

            outStream.write("%5d %34s\n" % (stateId, tokenName))

            trans = self.states[stateId].getTransitions()

            for onClass, toStateID in trans:
                outStream.write("%18s     %5d\n" % (onClass, toStateID))

            outStream.write("\n")


def main():

    q0 = nfastate.NFAState(0)
    q1 = nfastate.NFAState(1)
    q2 = nfastate.NFAState(2)
    q3 = nfastate.NFAState(3)
    q4 = nfastate.NFAState(4, True)
    q5 = nfastate.NFAState(5)
    q6 = nfastate.NFAState(6)
    q7 = nfastate.NFAState(7)
    q8 = nfastate.NFAState(8)
    q9 = nfastate.NFAState(9)
    q10 = nfastate.NFAState(10, True)

    classes = {epsilon: frozenset([]), 'a': frozenset(['a'])}

    q0.addTransition(epsilon, 1)
    q0.addTransition(epsilon, 5)
    q1.addTransition("a", 2)
    q2.addTransition("a", 3)
    q3.addTransition("a", 4)
    q4.addTransition("a", 2)
    q5.addTransition("a", 6)
    q6.addTransition("a", 7)
    q7.addTransition("a", 8)
    q8.addTransition("a", 9)
    q9.addTransition("a", 10)
    q10.addTransition("a", 6)

    states = {0: q0, 1: q1, 2: q2, 3: q3, 4: q4, 5: q5, 6: q6, 7: q7, 8: q8, 9: q9, 10: q10}

    nfa = NFA(classes, states)

    dfa = DFA()
    dfa.buildFromNFA(nfa)
    dfa.writeListing(sys.stdout)

    #classes = {epsilon: frozenset([]), "zero": frozenset([0]), "one": frozenset([1])}

    #q0 = nfastate.NFAState(0)
    #q1 = nfastate.NFAState(1, 1)
    #q2 = nfastate.NFAState(2)

    #q0.addTransition("zero", 1)
    #q0.addTransition("one", 1)
    #q1.addTransition("one", 1)
    #q1.addTransition("zero", 0)
    #q1.addTransition("zero", 2)
    #q1.addTransition(epsilon, 2)
    #q2.addTransition("one", 1)

    #states = {0: q0, 1: q1, 2: q2}

    #nfa = NFA(classes, states)

    #dfa = DFA()
    #dfa.buildFromNFA(nfa)
    #dfa.writeListing(sys.stdout)


if __name__ == "__main__":
    main()
