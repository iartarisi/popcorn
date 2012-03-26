#!/usr/bin/python
from popcorn.models import System,Submission,SubmissionPackage,Arch,Distro
from popcorn.database import db_session
from popcorn.parse import parse_text,FormatError,DataError,EarlySubmissionError
from datetime import date,timedelta

class SubTests():
	def __init__(self):
		self.sys_hwuuid=System.query.all()[1].sys_hwuuid
		self.distro_name=Distro.query.first().distro_name
		self.distro_version=Distro.query.first().distro_version
		self.arch='x86_64'
		self.system=System(self.sys_hwuuid,self.arch,self.distro_name,self.distro_version)
		
		self.parse_data=("POPCORN 0.1 openSUSE 12.1 x86_64 730d880e-6d78-4d40-9dd6-61cd7f6c0855\n"
		"o libgmp3 4.3.2 1.13 None i586 openSUSE\n"
		"o libfolks0 0.2.0 1.2 None i586 obs://build.opensuse.org/GNOME\n"
		"v enchant 1.6.0 2.3 1 i586 openSUSE\n"
		"o libx264-112 0.112svn20110115 1.pm.2.6 None i586 http://packman.links2linux.de\n"
		"n myspell-british 20100316 16.1 None noarch Uknown\n")
		
	#Retrieve packages submitted in last submission
	def last_sub_details(self):
		pkgs=self.system.last_submission.submission_packages
		print pkgs
	
	#Retrieve packages in submission made on specific date
	def details_specific_date(self,date):
		pkgs=SubmissionPackage.query.filter_by(sub_date=date).all()
		for i in pkgs:
			print i.pkg_name,i.pkg_version,str(i.sub_date)+'\n'
			
	#Successfully parse plain-text data and make a submission
	def parse_plain_text(self,date):
		try:
			parse_text(self.parse_data)
			print 'Data Sent'
		except EarlySubmissionError:
			print 'Too early to submit'
		except FormatError:
			print 'Error in parse text format'
		except DataError:
			print 'Data Error'
			
	#Successfully make a submission on a date plus or minus today's date
	def make_submission(self,date):
		try:
			sub=Submission(self.sys_hwuuid,'POPCORN 0.1',date)
			db_session.add(sub)
			db_session.commit()
			print 'Submission Recorded'
		except EarlySubmissionError:
			print 'Too early to submit'
		
#Testing of the methods
#sub_tests=SubTests()
#sub_tests.last_sub_details()
#sub_tests.details_specific_date(date(2012,03,15))		
#sub_tests.parse_plain_text(date(2012,14,10))		
#sub_tests.make_submission(date(2014,07,10))
