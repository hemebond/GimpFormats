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
from imgcompare import imgcompare

from gimpformats.GimpVbrBrush import GimpVbrBrush

__HERE__ = os.path.abspath(__file__).rsplit(os.sep, 1)[0] + os.sep


class Test(unittest.TestCase):
	"""Run unit test."""

	def setUp(self):
		self.dut = GimpVbrBrush()

	def tearDown(self):
		pass

	def testDiagonalStar(self):
		"""Test diagonal star."""
		self.dut.load(__HERE__ + "Diagonal-Star-17.vbr")
		# test image saving (explicit)
		# self.dut.image.save(__HERE__+'actualOutput_Diagonal-Star-17.png')
		# test for image match
		assert imgcompare.is_equal(
			self.dut.image, __HERE__ + "desiredOutput_Diagonal-Star-17.png", tolerance=1
		)
		# os.remove(__HERE__+'actualOutput_Diagonal-Star-17.png')
		# test round-trip compatibility
		self.dut.save(__HERE__ + "actualOutput_Diagonal-Star-17.vbr")
		original = GimpVbrBrush(
			__HERE__ + "Diagonal-Star-17.vbr"
		)  # open(__HERE__+'Diagonal-Star-17.vbr','rb').read()
		actual = self.dut  # open(__HERE__+'actualOutput_Diagonal-Star-17.vbr','rb').read()
		assert actual == original
		os.remove(__HERE__ + "actualOutput_Diagonal-Star-17.vbr")


def testSuite():
	"""Combine unit tests into an entire suite."""
	varTestSuite = unittest.TestSuite()
	varTestSuite.addTest(Test("testDiagonalStar"))
	return varTestSuite


if __name__ == "__main__":
	"""
	Run all the test suites in the standard way.
	"""
	unittest.main()
