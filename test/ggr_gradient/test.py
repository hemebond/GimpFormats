#!/usr/bin/env python3
"""Run unit tests.

You might be looking to run test.py from the 'test' directory. In windows::
/GimpFormats/test> py ./test.py

Alternatively, you can do py test.py or if you have pytest, pytest test.py
"""
from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

PROJECTDIR = str(Path(__file__).resolve().parent.parent)
sys.path.insert(0, os.path.dirname(PROJECTDIR))
from gimpformats.GimpGgrGradient import GimpGgrGradient

__HERE__ = os.path.abspath(__file__).rsplit(os.sep, 1)[0] + os.sep


class Test(unittest.TestCase):
	"""
	Run unit test
	"""

	def setUp(self):
		self.dut = GimpGgrGradient()

	def tearDown(self):
		pass

	def colorArray(self, numPoints):
		"""colour array."""
		colors = []
		i = 0.0
		inc = 1.0 / numPoints
		while i < 1.0:
			colors.append(self.dut.getColor(i))
			i += inc
		return colors

	def saveColors(self, f, colorArray):
		"""save colours."""
		f.write(b"r, g, b, a\n")
		for c in colorArray:
			line = []
			for _chan in c:
				line.append(str(c))
			line = ", ".join(line) + "\n"
			f.write(line.encode("utf-8"))

	def testColdSteel(self):
		"""test cold steel."""
		self.dut.load(__HERE__ + "Cold_Steel_2.ggr")
		# test round-trip compatibility
		self.dut.save(__HERE__ + "actualOutput_Cold_Steel_2.ggr")
		original = open(__HERE__ + "Cold_Steel_2.ggr", "rb")
		actual = open(__HERE__ + "actualOutput_Cold_Steel_2.ggr", "rb")
		assert actual.read() == original.read().replace(b"\r\n", b"\n")
		original.close()
		actual.close()
		os.remove(__HERE__ + "actualOutput_Cold_Steel_2.ggr")
		# TODO: test calculated colors
		# colors=self.colorArray(512)
		# actual=open(__HERE__+'actualOutput_Cold_Steel_2.csv','wb')
		# saveColors(actual,colors)


def testSuite():
	"""
	Combine unit tests into an entire suite
	"""
	varTestSuite = unittest.TestSuite()
	varTestSuite.addTest(Test("testColdSteel"))
	return varTestSuite


if __name__ == "__main__":
	"""
	Run all the test suites in the standard way.
	"""
	unittest.main()
