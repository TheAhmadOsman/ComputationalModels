###########################################
#   Author: Ahmad M. Osman
#   Date: 10/27/2017
#
#   Class: CS 260
#   Instructor: Dr. Kent Lee
#
#   File name: ahmad-main.py
#   Purpose: Prefix to Postfix
###########################################


import io
import streamreader


class SubNode:

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self):
        return " ".join([str(self.left.eval()), str(self.right.eval()), "-"])


class AddNode:

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self):
        return " ".join([str(self.left.eval()), str(self.right.eval()), "+"])


class MulNode:

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self):
        return " ".join([str(self.left.eval()), str(self.right.eval()), "*"])


class DivNode:

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self):
        return " ".join([str(self.left.eval()), str(self.right.eval()), "/"])


class NumNode:

    def __init__(self, num):
        self.val = num

    def eval(self):
        return self.val


def E(reader):
    token = reader.getToken()

    if token == "-":
        return SubNode(E(reader), E(reader))

    if token == "+":
        return AddNode(E(reader), E(reader))

    if token == "*":
        return MulNode(E(reader), E(reader))

    if token == "/":
        return DivNode(E(reader), E(reader))

    try:
        # Can be float in case we are dealing with decimal points
        # The expression on Katie showed all ints and that is why I used int
        v = int(token)
        return NumNode(v)

    except ValueError:
        raise Exception("Invalid Prefix expression " + token)


def Prog(reader):
    ast = E(reader)
    token = reader.getToken()

    if reader.eof():
        return ast

    raise Exception("Invalid Prefix expression")


def main():

    expression = input(
        "Please enter a prefix expression (or press enter to stop): ")

    while expression != "":

        reader = streamreader.StreamReader(io.StringIO(expression))

        try:
            ast = Prog(reader)
            print("The postfix form is: ", ast.eval())
        except Exception as e:
            print(e)

        expression = input(
            "Please enter a prefix expression (or press enter to stop): ")


if __name__ == "__main__":
    main()
