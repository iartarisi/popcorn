#!/usr/bin/python
from popcorn.models import System,Distro,Arch,Submission
from popcorn.test.test_models import ModelsTest
from popcorn.parse import parse_text,FormatError,EarlySubmissionError,_can_submit
from popcorn.database import db_session
from sqlalchemy.exc import DataError
from datetime import date
import unittest
class TestClass(ModelsTest):
	#Test Creation of Submission
	def test_submission_creation(self):
		sys=System('test_hwuuid','x86_64','openSUSE','12.1')
		db_session.add(sys)
		sub=Submission('test_hwuuid','POPCORN 0.1',date.today())
		self.assertEqual(sys.submissions,[])
		db_session.add(sub)
		db_session.commit()
		
		self.assertEqual(sys.submissions,[sub])
		self.assertEqual(Submission.query.all(),[sub])
		
	#Test Bad plain-text submission- FormatError,ValueError
	def test_bad_plain_text(self):
		subm_text1=('POPCORN 0.1 Fedora 12 unknown-arch test_hwuuid\n')
		self.assertRaises(FormatError,parse_text,subm_text1)
		
		subm_text2=('Fedora 12 x86_64 test_hwuuid\n')
		self.assertRaises(ValueError,parse_text,subm_text2)
		
	#Test for Early Submission
	def test_early_submission(self):
		sys=System('test_hwuuid','x86_64','openSUSE','12.1')
		db_session.add(sys)
		sub=Submission('test_hwuuid','POPCORN 0.1',date.today())
		self.assertEqual(sys.submissions,[])
		db_session.add(sub)
		db_session.commit()
		
		subm_text=('POPCORN 0.1 openSUSE 12.1 x86_64 test_hwuuid\n')
		self.assertRaises(EarlySubmissionError,parse_text,subm_text)
		self.assertEqual(sys.last_submission,sub)
		self.assertEqual(_can_submit(sys),False)
		
	#Test for DataError in adding Distro to database
	def test_data_error_distro(self):
		distro1_name='opensuse-fedora-ubuntu'
		distro1_version='12.1'
		dis1=Distro(distro1_name,distro1_version)
		db_session.add(dis1)
		self.assertRaises(DataError,db_session.commit())
		
		distro2_name='openSUSE'
		distro2_version='123.3467653432'
		dis2=Distro(distro2_name,distro2_version)
		db_session.add(dis2)
		self.assertRaises(DataError,db_session.commit())
		
	#Test for DataError in adding a Architecture to database
	def test_data_error_architecture(self):
		arch='x86_64-i686-i386'
		new_arch=Arch(arch)
		db_session.add(new_arch)
		self.assertRaises(DataError,db_session.commit())
		
	#Test for a plain-text submission and package details
	def test_plain_text_submission(self):
		subm_text=('POPCORN 0.1 openSUSE 12.1 x86_64 test_hwuuid\n'
					'o test-xyz 1.1 1 None noarch http://test.url\n')
		parse_text(subm_text)
		sys=System.query.filter_by(sys_hwuuid='test_hwuuid').one()
		self.assertEqual(len(sys.submissions),1)
		
		sub=sys.last_submission.submission_packages
		self.assertEqual(sub[0].pkg_name,'test-xyz')
		self.assertEqual(sub[0].pkg_version,'1.1')
		self.assertEqual(sub[0].pkg_release,'1')
		self.assertEqual(sub[0].pkg_status,'old')
		self.assertEqual(sub[0].pkg_epoch,'')
		self.assertEqual(sub[0].pkg_arch,'noarch')
		
#Better output in running the test
#suite = unittest.TestLoader().loadTestsFromTestCase(TestClass)
#unittest.TextTestRunner(verbosity=2).run(suite)
		
