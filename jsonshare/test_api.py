import unittest
import frappe
import api

class TestApi(unittest.TestCase):
	def test_sumoftwo_integers(self):
		# Compruebe que la funcion hace lo que dice que hace
		# por ejemplo:
		a = 56
		b = 44
		self.assertAlmostEqual(sumtwo(a,b), a+b)