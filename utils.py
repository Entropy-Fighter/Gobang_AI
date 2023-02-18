import numpy as np
# (1, 1)black, (1, 0)white, (0, 0)None
threechess = np.array([[0, 0], [1, 1], [1, 1], [1, 1], [0, 0]], dtype=bool)
threeChess = np.array([[[0, 0], [1, 1], [1, 1], [1, 1], [0, 0], [0, 0]],
                       [[0, 0], [1, 1], [1, 1], [1, 1], [0, 0], [1, 0]],
                       [[0, 0], [0, 0], [1, 1], [1, 1], [1, 1], [0, 0]],
                       [[1, 0], [0, 0], [1, 1], [1, 1], [1, 1], [0, 0]],
                       [[0, 0], [1, 1], [1, 1], [0, 0], [1, 1], [0, 0]],
                       [[0, 0], [1, 1], [0, 0], [1, 1], [1, 1], [0, 0]]], dtype=bool)
fourChess = np.array([[[1, 1], [1, 1], [1, 1], [1, 1], [0, 0], [0, 0]],
                      [[1, 1], [1, 1], [1, 1], [1, 1], [0, 0], [1, 0]],
                      [[0, 0], [1, 1], [1, 1], [1, 1], [1, 1], [0, 0]],
                      [[1, 0], [1, 1], [1, 1], [1, 1], [1, 1], [0, 0]],
                      [[0, 0], [1, 1], [1, 1], [1, 1], [1, 1], [1, 0]],
                      [[0, 0], [0, 0], [1, 1], [1, 1], [1, 1], [1, 1]],
                      [[1, 0], [0, 0], [1, 1], [1, 1], [1, 1], [1, 1]],
                      [[1, 1], [1, 1], [1, 1], [0, 0], [1, 1], [0, 0]],
                      [[1, 1], [1, 1], [1, 1], [0, 0], [1, 1], [1, 0]],
                      [[0, 0], [1, 1], [1, 1], [1, 1], [0, 0], [1, 1]],
                      [[1, 0], [1, 1], [1, 1], [1, 1], [0, 0], [1, 1]],
                      [[1, 1], [1, 1], [0, 0], [1, 1], [1, 1], [0, 0]],
                      [[1, 1], [1, 1], [0, 0], [1, 1], [1, 1], [1, 0]],
                      [[0, 0], [1, 1], [1, 1], [0, 0], [1, 1], [1, 1]],
                      [[1, 0], [1, 1], [1, 1], [0, 0], [1, 1], [1, 1]]], dtype=bool)
fivechess = np.array([[1, 1], [1, 1], [1, 1], [1, 1], [1, 1]], dtype=bool)
fiveChess = np.array([[[0, 0], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1]],
                      [[1, 0], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1]],
                      [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 0]],
                      [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [0, 0]],
                      # white
                      [[0, 0], [1, 0], [1, 0], [1, 0], [1, 0], [1, 0]],
                      [[1, 1], [1, 0], [1, 0], [1, 0], [1, 0], [1, 0]],
                      [[1, 0], [1, 0], [1, 0], [1, 0], [1, 0], [1, 1]],
                      [[1, 0], [1, 0], [1, 0], [1, 0], [1, 0], [0, 0]]], dtype=bool)
sixChess = np.array([[1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1]], dtype=bool)
blank = np.array([0, 0], dtype=bool)
