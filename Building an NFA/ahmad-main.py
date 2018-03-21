###########################################
#   Author: Ahmad M. Osman
#   Date: 9/17/2017
#   File name: ahmad-main.py
#   Class: CS 260
#   Instructor: Dr. Kent Lee
#   Purpse: Building an NFA
###########################################


import state
import io
import streamreader

# This NFAStateMachine demonstrates backtracking search while trying
# to find a means of accepting a string of characters. The NFA allows
# the use of "epsilon" transitions and cycles of "epsilon" transitions.
# It avoids getting stuck in a cycle by keeping track of visited
# "states". The state of the NFA is determined not only by the nfa
# state it is in, but also by the state of the stream it is reading.
# A cycle occurs when a state is visited twice with the same number
# of characters read from the stream.


class NFAStateMachine:

    def __init__(self, states, startStateId, classes):
        self.states = states
        self.startStateId = startStateId
        self.classes = classes

        for stateId in self.states:
            self.states[stateId].setClasses(classes)

    def accepts(self, strm):
        # The accepts method uses a recursive acceptsSuffix
        # which starts in the given state (not necessarily the
        # start state) and recursively uses search with backtracking
        # to try to find a final state with all of the input consumed.
        # If it is successful on this path then it returns True and if
        # not it returns False to continue to backtrack and look for
        # another path to a final state.

        def acceptsSuffix(stateId):
            #print("trying", stateId, "with", strm.numCharsRead(), "characters read")

            # If we are not making any progress, we must backtrack.
            if (stateId, strm.numCharsRead()) in visited:
                #print("backtracking from", stateId, "already visited")
                return False

            # Otherwise, add the (stateId, number of characters read) to the
            # set of visited states.
            visited.add((stateId, strm.numCharsRead()))
            theState = self.states[stateId]

            # Check that we are not at end of file and in an accepting state.
            c = strm.readChar()
            if strm.eof() and theState.isAccepting():
                # print(stateId)
                return True

            strm.unreadChar(c)

            for onClass, toStateId in theState.getTransitions():

                if onClass == "epsilon":
                    if acceptsSuffix(toStateId):
                        # print(stateId)
                        return True

                else:  # onClass is not an epsilon transition
                    c = strm.readChar()

                    if c in self.classes[onClass] and acceptsSuffix(toStateId):
                        # print(stateId)
                        return True

                    strm.unreadChar(c)

            #print("backtracking from", stateId)
            return False

        # This set will take care of keeping track of all traversed
        # states and characters read from the stream. If progress is
        # not made, then we must backtrack.
        visited = set()

        # Beginning of accepts function body - We call acceptsSuffix
        # initially starting from the start state.
        return acceptsSuffix(self.startStateId)


def main():

    q0 = state.State(0)
    q1 = state.State(1)
    q2 = state.State(2)
    q3 = state.State(3, True)
    q4 = state.State(4)
    q5 = state.State(5)
    q6 = state.State(6)
    q7 = state.State(7)
    q8 = state.State(8, True)

    classes = {"a": frozenset(["a"])}

    q0.addTransition("a", 1)
    q0.addTransition("a", 4)

    q1.addTransition("a", 2)
    q2.addTransition("a", 3)

    q3.addTransition("a", 1)

    q4.addTransition("a", 5)
    q5.addTransition("a", 6)
    q6.addTransition("a", 7)
    q7.addTransition("a", 8)

    q8.addTransition("a", 4)

    nfa = NFAStateMachine(
        {0: q0, 1: q1, 2: q2, 3: q3, 4: q4, 5: q5, 6: q6, 7: q7, 8: q8}, 0, classes)

    done = False

    s = input(
        "Please enter a string of zeros and ones (type done to quit): ").strip()

    while s != "done":

        strm = streamreader.StreamReader(io.StringIO(s))

        if nfa.accepts(strm):
            print("The string is accepted by the finite state machine.")
        else:
            print("The string is not accepted.")

        s = input(
            "Please enter a string of zeros and ones (type done to quit): ").strip()

    print("Program Completed.")

if __name__ == "__main__":
    main()
