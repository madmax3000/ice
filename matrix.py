#! /usr/bin/env python

import sys

class Matrix:
    """ For defining arrays of any given size.
    Contains overloaded operators for print, add, subtract and multiply. Does not contain = assignment operator! Use a(b) instead of a=b.
    Last updated - Dec 30, 2012 """

    def resize(self, rows, columns = 1):
        """ Changes the dimension of an existing matrix by add/deleting difference of rows and columns."""

        if (rows<self.rows):
            for c1 in range(self.rows-1,rows-1,-1):
                del self.data[c1]
                self.rows = rows
        if (columns<self.columns):
            for c1 in range(self.rows):
                for c2 in range(self.columns-1, columns-1, -1):
                    del self.data[c1][c2]
            for c1 in range(self.rows, rows):
                row_vector = []
                for c2 in range(columns):
                    row_vector.append(0.0)
                self.data.append(row_vector)
        else:
            for c1 in range(self.rows):
                for c2 in range(self.columns, columns):
                    self.data[c1].append(0.0)
            for c1 in range(self.rows, rows):
                row_vector = []
                for c2 in range(columns):
                    row_vector.append(0.0)
                self.data.append(row_vector)
        self.rows = rows
        self.columns = columns

        return


    def zeros(self, rows, columns = 1):
        """ Creates a zero matrix
        Dimensions have to be passed as <Matrix>.zeros(rows, columns).
        This function also creates the actual array. So every method of the class/object should call this first before using the array."""

        try:
            if self.data: pass
        except:
            self.data = []
            for count1 in range(self.rows):
                row_vector = []
                for count2 in range(self.columns):
                    row_vector.append(0.0)
                self.data.append(row_vector)

        if not (self.rows==rows and self.columns==columns):
            self.resize(rows, columns)

        # self.data=[]                                  Removed on Dec. 30 due to resize() function addition to class.
        for count1 in range(self.rows):
            #row_vector=[]                              Removed on Dec. 30 due to resize() function addition to class.
            for count2 in range(self.columns):
                #row_vector.append(0.0)                 Removed on Dec. 30 due to resize() function addition to class.
                self.data[count1][count2]=0.0
            #self.data.append(row_vector)               Removed on Dec. 30 due to resize() function addition to class.

        return


    def __init__(self, rows = 1, columns = 1):
        """Creates an object with a zero array of size rowsXcolumns.
        If only one dimension is specified specified, a column vector is assumed. If no dimensions are specified, an null matrix is created."""

        self.rows = 1
        self.columns = 1
        self.zeros(rows, columns)


    def __call__(self, matrix1):
        """ Replaces the assignment operator =. Use as c(b) instead of c=b.
            The = will only result in a reference to the object and not an actual copy. This method ensures it. """

        #self.rows = matrix1.rows                         Removed on Dec. 30 due to resize() function addition to class.
        #self.columns = matrix1.columns                   Removed on Dec. 30 due to resize() function addition to class.
        if not (self.rows==matrix1.rows and self.columns==matrix1.columns):
            self.resize(matrix1.rows, matrix1.columns)
        for count1 in range(self.rows):
            for count2 in range(self.columns):
                self.data[count1][count2] = matrix1.data[count1][count2]


    def identity(self, rows):
        """ Generates an identity matrix of rowsXrows. """
        self.rows = rows
        self.columns = rows
        self.zeros(self.rows, self.columns)
        for count in range(self.rows):
            self.data[count][count] = 1.0


    def display(self):
        """ Explicit method for displaying an array. """
        for count1 in range(self.rows):
            for count2 in range(self.columns):
                print(str(self.data[count1][count2]), end="\t")
            print()


    def __repr__(self):
        """ Displays an array when print <Matrix> is used. """
        for count1 in range(self.rows):
            for count2 in range(self.columns):
                print(str(self.data[count1][count2]), end="\t")
            print()
        return " "


    def __add__(self, matrix1):
        """ Left addition of two matrices. """
        add_result = Matrix(self.rows, self.columns)
        try:
            if matrix1.rows: pass
        except AttributeError:
            print("*"*40)
            print("Can't add a float or integer to a matrix directly.")
            print("*"*40)
            sys.exit("Logic Error")
        else:
            if not (self.rows==matrix1.rows and self.columns==matrix1.columns):
                print("Matrices not compatible for summation.")
                sys.exit("Logic Error")
            else:
                for count1 in range(self.rows):
                    for count2 in range(self.columns):
                        add_result.data[count1][count2] = self.data[count1][count2]+matrix1.data[count1][count2]
        return add_result


    def __radd__(self, matrix1):
        """ Right addition of two matrices. """
        add_result = Matrix(self.rows, self.columns)
        try:
            if matrix1.rows: pass
        except AttributeError:
            print("*"*40)
            print("Can't add a float or integer to a matrix directly.")
            print("*"*40)
            sys.exit("Logic Error")
        else:
            if not (self.rows==matrix1.rows and self.columns==matrix1.columns):
                print("Matrices not compatible for summation.")
            else:
                for count1 in range(self.rows):
                    for count2 in range(self.columns):
                        add_result.data[count1][count2] = self.data[count1][count2]+matrix1.data[count1][count2]
        return add_result


    def __sub__(self, matrix1):
        """ Left subtraction of two matrices. """
        sub_result = Matrix(self.rows, self.columns)
        try:
            if matrix1.rows: pass
        except AttributeError:
            print("*"*40)
            print("Can't subtract a float or integer to a matrix directly.")
            print("*"*40)
            sys.exit("Logic Error")
        else:
            if not (self.rows==matrix1.rows and self.columns==matrix1.columns):
                print("Matrices not compatible for subtraction.")
                sys.exit("Logic Error")
            else:
                for count1 in range(self.rows):
                    for count2 in range(self.columns):
                        sub_result.data[count1][count2] = self.data[count1][count2]-matrix1.data[count1][count2]
        return sub_result


    def __rsub__(self, matrix1):
        """ Right subtraction of two mnatrices. """
        sub_result = Matrix(self.rows, self.columns)
        try:
            if matrix1.rows: pass
        except AttributeError:
            print("*"*40)
            print("Can't subtract a float or integer to a matrix directly.")
            print("*"*40)
            sys.exit("Logic Error")
        else:
            if not (self.rows==matrix1.rows and self.columns==matrix1.columns):
                print("Matrices not compatible for subtraction.")
                sys.exit("Logic Error")
            else:
                for count1 in range(self.rows):
                    for count2 in range(self.columns):
                        sub_result.data[count1][count2] = matrix1.data[count1][count2]-self.data[count1][count2]
        return sub_result


    def __mul__(self, matrix1):
        """ Left multiplication of two matrices.
        The multiplication is NOT done elementwise but in the conventional mathematical sense. """
        try:
            if matrix1.rows: pass
        except AttributeError:
            mul_result = Matrix(self.rows, self.columns)
            for count1 in range(self.rows):
                for count2 in range(self.columns):
                    mul_result.data[count1][count2] = self.data[count1][count2]*matrix1
        else:
            mul_result = Matrix()
            if not (self.columns==matrix1.rows):
                print("Matrices not compatible for multiplication.")
            else:
                mul_result.zeros(self.rows, matrix1.columns)
                for count1 in range(self.rows):
                    for count2 in range(matrix1.columns):
                        for count3 in range(self.columns):
                            mul_result.data[count1][count2] += self.data[count1][count3]*matrix1.data[count3][count2]
        return mul_result


    def __rmul__(self, matrix1):
        """ Right multiplication of two matrices.
        The multiplication is NOT done elementwise but in the conventional mathematical sense. """
        try:
            if matrix1.rows: pass
        except AttributeError:
            mul_result = Matrix(self.rows, self.columns)
            for count1 in range(self.rows):
                for count2 in range(self.columns):
                    mul_result.data[count1][count2] = self.data[count1][count2]*matrix1
        else:
            mul_result = Matrix()
            if not (self.rows==matrix1.columns):
                print("Matrices not compatible for multiplication.")
            else:
                mul_result.zeros(matrix1.rows, self.columns)
                for count1 in range(matrix1.rows):
                    for count2 in range(self.columns):
                        for count3 in range(self.rows):
                            mul_result.data[count1][count2] += self.data[count1][count3]*matrix1.data[count3][count2]
        return mul_result


    def transpose(self):
        """ Returns a matrix that is transpose of the calling object array. A new object is returned. Original object is untouched. """
        trans_result = Matrix(self.columns, self.rows)
        for count1 in range(self.rows):
            for count2 in range(self.columns):
                trans_result.data[count2][count1] = self.data[count1][count2]
        return trans_result
