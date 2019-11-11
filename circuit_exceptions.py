#! /usr/bin/env python

import sys
import math

class AdjacentJumpError(Exception):
    """
    This error is raised when two jump labels
    are found adjacent to each other.
    """

    def __init__(self):
        print("Circuit Error: Jump labels in adjacent cells.")
        print("*"*40)
        print()
        sys.exit(1)


class JumpNotExtremeError(Exception):
    """
    This error is raised when a jump label
    is not the extreme element on the branch.
    """

    def __init__(self):
        print("Circuit Error: Jump has to be the extreme connector on a branch segment.")
        print("*"*40)
        print()
        sys.exit(1)


class SingleJumpError(Exception):
    """
    This error is raised when a jump label
    does not have a corresponding jump.
    """

    def __init__(self):
        print("Circuit Error: Jump does not have a corresponding jump label.")
        print("*"*40)
        print()
        sys.exit(1)


class MultipleJumpError(Exception):
    """
    This error is raised when a more than
    two jumps having the same label exist.
    """

    def __init__(self):
        print("Circuit Error: More than two jumps for the jump label.")
        print("*"*40)
        print()
        sys.exit(1)


class JumpAdjacentNodeError(Exception):
    """
    This error is raised when a jump label
    is adjacent to a node.
    """

    def __init__(self):
        print("Circuit Error: Jump label is adjacent to a node.")
        print("*"*40)
        print()
        sys.exit(1)


class BrokenBranchError(Exception):
    """
    This error is raised when a branch is broken.
    """

    def __init__(self):
        print("Circuit Error: Branch is broken. Must close all branches.")
        print("*"*40)
        print()
        sys.exit(1)



class PolarityError(Exception):
    """
    This error is raised when there is an error in the polarity of an element.
    """

    def __init__(self):
        print("Circuit Error: Error in polarity")
        print("*"*40)
        print()
        sys.exit(1)



class MissingComponentTagError(Exception):
    """
    This error is raised when a component does not
    have a label or name.
    """

    def __init__(self):
        print("Circuit Error: Missing component tags")
        print("*"*40)
        print()
        sys.exit(1)



class UnidentifiedComponentError(Exception):
    """
    This error is raised when a component does not
    exist in the library.
    """

    def __init__(self):
        print("Circuit Error: Component does not exist")
        print("*"*40)
        print()
        sys.exit(1)


class DuplicateComponentLabelError(Exception):
    """
    This error is raised when two or more components
    have the same label or name.
    """

    def __init__(self):
        print("Circuit Error: Duplicate component labels")
        print("*"*40)
        print()
        sys.exit(1)



class BranchZeroResistanceError(Exception):
    """
    This error is raised when the resistance of a branch
    with elements becomes zero.
    """

    def __init__(self):
        print("Circuit Error: Branch has zero resistance.")
        print("*"*40)
        print()
        sys.exit(1)



class MultipleControlVariableError(Exception):
    """
    This error is raised when there are the same control variables
    with the same name defined in multiple files.
    """

    def __init__(self):
        print("Control Error: Control variable repeated. A control variable can occur only once among all the control files.")
        print("*"*40)
        print()
        sys.exit(1)
