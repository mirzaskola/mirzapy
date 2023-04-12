class Matrix:
    @staticmethod
    def ones(rows, cols):
        """
        Returns a matrix of ones with the given dimensions.
        """
        result = Matrix(rows, cols)
        for i in range(rows):
            for j in range(cols):
                result[i][j] = 1
        return result

    def __init__(self, *args, **kwargs):
        self.rows = 0
        self.cols = 0
        self.data = []

        if len(args) == 1 and isinstance(args[0], list) and args[0] != []:
            self.data = args[0]
            if isinstance(self.data[0], list):
                self.rows = len(self.data)
                self.cols = len(self.data[0])
                for i in range(self.rows):
                    if len(self.data[i]) != self.cols:
                        raise ValueError("Inconsistent matrix dimensions")
            else:
                self.rows = 1
                self.cols = len(self.data)
        elif len(args) == 1 and isinstance(args[0], list) and args[0] == []:
            self.rows = 0
            self.cols = 0
            self.data = []
        elif len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int):
            self.rows = args[0]
            self.cols = args[1]
            self.data = [[0 for j in range(self.cols)] for i in range(self.rows)]
        elif 'data' in kwargs:
            self.data = kwargs['data']
            if isinstance(self.data[0], list):
                self.rows = len(self.data)
                self.cols = len(self.data[0])
                for i in range(self.rows):
                    if len(self.data[i]) != self.cols:
                        raise ValueError("Inconsistent matrix dimensions")
            else:
                self.rows = 1
                self.cols = len(self.data)
        elif 'rows' in kwargs and 'cols' in kwargs:
            self.rows = kwargs['rows']
            self.cols = kwargs['cols']
            self.data = [[0 for j in range(self.cols)] for i in range(self.rows)]
        else:
            if len(args) == 0 and len(kwargs) == 0:
                self.rows = 0
                self.cols = 0
                self.data = []
            else:
                raise ValueError("Must specify either data or rows and cols")

    def __getitem__(self, key):
        """
        Definition of the __getitem__ method, supports the following syntax:
        print(A[:, 1])  # output: [2, 5, 8]
        print(A[1, :])  # output: [4, 5, 6]
        print(A[0:2, 1:])  # output: [[2, 3], [5, 6]]
        print(A[::2, ::2])  # output: [[1, 3], [7, 9]]
        """
        if isinstance(key, tuple):
            row_key, col_key = key
            if isinstance(row_key, int) and isinstance(col_key, int):
                return self.data[row_key][col_key]
            elif isinstance(row_key, int) and isinstance(col_key, slice):
                return [self.data[row_key][j] for j in range(*col_key.indices(self.cols))]
            elif isinstance(row_key, slice) and isinstance(col_key, int):
                return [self.data[i][col_key] for i in range(*row_key.indices(self.rows))]
            elif isinstance(row_key, slice) and isinstance(col_key, slice):
                return [[self.data[i][j] for j in range(*col_key.indices(self.cols))] for i in
                        range(*row_key.indices(self.rows))]
            else:
                raise IndexError("Invalid index")
        elif isinstance(key, int):
            return self.data[key]
        elif isinstance(key, slice):
            return [row[0] for row in self.data[key]]
        else:
            raise IndexError("Invalid index")

    def __str__(self):
        """
        Returns a string representation of the matrix.
        """
        output = ""
        if self.rows == 1:
            output += "[" + " ".join(str(x) for x in self.data) + "]"
        else:
            for i in range(self.rows):
                for j in range(self.cols):
                    output += str(self.data[i][j]) + " "
                output += "\n"
        return output

    def size(self):
        """
        Returns the size of the matrix as a tuple (rows, cols)
        """
        return self.rows, self.cols

    def get_row(self, index):
        return self[index, :]

    def get_col(self, index):
        return self[:, index]

    def transform(self, data_type):
        """
        Convert the data in the matrix to a specific datatype
        """
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                self.data[i][j] = data_type(self.data[i][j])

    def transpose(self):
        """
        Transposes the matrix
        """
        if self.rows == 1:
            self.data = [[x] for x in self.data]
            self.rows, self.cols = self.cols, self.rows
        elif self.cols == 1:
            self.data = [x for x in self.data[0]]
            self.rows, self.cols = self.cols, self.rows
        else:
            self.data = [[self.data[j][i] for j in range(self.rows)] for i in range(self.cols)]
            self.rows, self.cols = self.cols, self.rows

    def verify_type(self, other):
        """
        Verifies if the input matrix is of the correct type before performing operations.
        """
        if not isinstance(other, Matrix):
            raise TypeError("Cannot perform operation. Input must be a Matrix object.")


def is_nested_list(lista):
    if not isinstance(lista, list):
        return False
    return any(isinstance(i, list) for i in lista)
