#!/usr/bin/python
import mock
from popcorn.parse import parse_text,mail_to_admin,DataError
from popcorn import trace_mail
import traceback
import unittest

parse_data=("POPCORN 0.1 openSUSE-fedora-ubuntu-mint 12.1 x86_64 test_hwuuid22\n"
		"o libgmp3 4.3.2 1.13 None i586 openSUSE\n"
		"o libfolks0 0.2.0 1.2 None i586 obs://build.opensuse.org/GNOME\n"
		"v enchant 1.6.0 2.3 1 i586 openSUSE\n"
		"o libx264-112 0.112svn20110115 1.pm.2.6 None i586 http://packman.links2linux.de\n"
		"n myspell-british 20100316 16.1 None noarch Uknown\n")

class testing_calls(unittest.TestCase):
	def test_mail_call(self):
		with mock.patch('popcorn.parse.mail_to_admin') as patched:
			parse_text(parse_data)
			patched.assert_called_with(DataError)

