import unittest

import test_recompose
import test_find_basis
import test_utils
import test_matrix_ln
import test_diagonalize

loader = unittest.TestLoader()

suite = unittest.TestSuite()
suite.addTest(test_recompose.get_suite())
suite.addTest(test_find_basis.get_suite())
suite.addTest(test_utils.get_suite())
suite.addTest(test_matrix_ln.get_suite())
suite.addTest(test_diagonalize.get_suite())
unittest.TextTestRunner(verbosity=2).run(suite)