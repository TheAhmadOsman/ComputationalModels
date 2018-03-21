'''
Name: Rafael Broseghini
Prof: Kent Lee

Date: 9/27/2017
Course: CS260
'''



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
            new_State = state.State(self.numStates)
            self.states[self.numStates] = new_State
            self.numStates += 1
            return new_State.getId()

        def getAcceptingTokenId(stateSet):
            for stateid in stateSet:
                final_state = nfa.states[stateid].isAccepting()
                if final_state:
                    self.tokens[final_state] = "Yes"
                    return nfa.states[stateid].getAcceptsTokenId()
            return None

        def EPSclosure(stateSet):
            closureSet = orderedcollections.OrderedSet(stateSet)
            unexploredStatesSet = orderedcollections.OrderedSet(stateSet)
            while len(unexploredStatesSet) != 0:
                stateidx = unexploredStatesSet.pop()
                toStates = nfa.states[stateidx].onClassGoTo(epsilon)
                for toState in toStates:
                    if toState not in closureSet:
                        closureSet.add(toState)
                        unexploredStatesSet.add(toState)
            return orderedcollections.OrderedFrozenSet(closureSet)

        def nfaTransTo(fromStates, onClass):
            toStates = orderedcollections.OrderedSet()
            for stateidx in fromStates:
                toStates.update(nfa.states[stateidx].onClassGoTo(onClass))
            return orderedcollections.OrderedSet(EPSclosure(toStates))

        def gatherClasses(states):
            gathered = orderedcollections.OrderedSet()
            for stateidx in states:
                transitions = nfa.states[stateidx].getTransitions()
                for onClass in transitions:
                    if onClass != epsilon:
                        gathered.add(onClass)
            return gathered

        # This is the beginning of the buildFromNFA method.
        # Copy over the classes
        self.classes = nfa.classes

        # Create the start state and the DFA to NFA stateMap.
        self.startStateId = newState()
        stateMap = orderedcollections.OrderedMap()
        
        EPSstartState = EPSclosure(orderedcollections.OrderedSet([self.startStateId]))
        stateMap[self.startStateId] = EPSstartState        
        # Form the epsilon closure of the NFA start state (i.e. state 0) and then
        # map the start state of the DFA to the start state set of the NFA
        
        alphabet = gatherClasses(stateMap[self.startStateId])
        for letter in alphabet:
            toStates = orderedcollections.OrderedSet()
            for stateidx in stateMap[self.startStateId]:
                toStates.update(nfa.states[stateidx].onClassGoTo(letter))
            for trans in toStates:
                self.states[self.startStateId].addTransition(letter, trans)


        # Keep track of the new DFA states. The first new DFA state is the start
        # state. You can keep track of this as an ordered set or a stack if you
        # wish.
        unexploredStatesSet = orderedcollections.OrderedSet([self.startStateId])
        self.tokens = orderedcollections.OrderedMap()
        nfa2dfaMap = orderedcollections.OrderedMap()
        nfa2dfaMap[EPSstartState] = self.states[self.startStateId]        
        # Map the set of nfa state ids (as a frozen set) to the new DFA state id in the
        # nfa2dfa map.
        # set the new DFA state to accepting if the NFA states contained an accepting state.
        # You can use the getAcceptingTokenId function for this.

        while len(unexploredStatesSet) > 0:
            currentStateId = unexploredStatesSet.pop()
            alphabet = gatherClasses(stateMap[currentStateId])
            for letter in alphabet:
                transitioning = orderedcollections.OrderedFrozenSet(
                    nfaTransTo(stateMap[currentStateId], letter))
                if transitioning not in stateMap.values():
                    newDFAState = newState()
                    stateMap[newDFAState] = transitioning
                    nfa2dfaMap[transitioning] = self.states[newDFAState]
                    alphabetTwo = gatherClasses(stateMap[newDFAState])
                    for letter in alphabetTwo:
                        toStates = orderedcollections.OrderedSet()
                        for stateidx in stateMap[newDFAState]:
                            toStates.update(nfa.states[stateidx].onClassGoTo(letter))
                        for trans in toStates:
                            self.states[newDFAState].addTransition(letter, trans)
                    if getAcceptingTokenId(transitioning):
                        self.states[newDFAState].setAccepting(True)
                    unexploredStatesSet.add(newDFAState)

                    for stateidx in stateMap[newDFAState]:
                        EPSColusreState = EPSclosure(
                            orderedcollections.OrderedSet([stateidx]))
                        if EPSColusreState not in stateMap.values() and len(EPSColusreState) > 1:
                            newDFAstateFromClosure = newState()
                            stateMap[newDFAstateFromClosure] = EPSColusreState
                            nfa2dfaMap[EPSColusreState] = self.states[newDFAstateFromClosure]
                            isAcceptingDFA[newDFAstateFromClosure] = getAcceptingTokenId(EPSColusreState)
                            toStates = orderedcollections.OrderedSet()
                            for stateidx in stateMap[newDFAstateFromClosure]:
                                toStates.update(nfa.states[stateidx].onClassGoTo(letter))
                            for trans in toStates:
                                self.states[newDFAstateFromClosure].addTransition(letter, trans)
                            self.states[newDFAstateFromClosure].addTransition(epsilon, trans)
                            if getAcceptingTokenId(EPSColusreState):
                                self.states[
                                    newDFAstateFromClosure].setAccepting(True)
                            unexploredStatesSet.add(newDFAstateFromClosure)

        # While there are no more unexplored states in the new DFA state set, follow the algorithm
        # given on the website by using the nfaTransTo function and creating new DFA states for each
        # new set of NFA states that are found by using gatherClasses. Remember to set accepting states
        # in the DFA as you proceed.

    def writeListing(self, outStream):

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

            for onClass in trans:
                outStream.write("%18s     %5d\n" % (onClass[0], onClass[1]))

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

    states = {0: q0, 1: q1, 2: q2, 3: q3, 4: q4,
              5: q5, 6: q6, 7: q7, 8: q8, 9: q9, 10: q10}

    nfa = NFA(classes, states)

    dfa = DFA()
    dfa.buildFromNFA(nfa)
    dfa.writeListing(sys.stdout)

if __name__ == "__main__":
    main()
