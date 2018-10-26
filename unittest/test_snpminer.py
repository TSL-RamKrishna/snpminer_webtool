import unittest
from uploadScript imort upload
import cgi, cgitb

cgitb.enable(logdir=log_dir)
form = cgi.FieldStorage()


class Test_Snpminer(unittest.TestCase):
	def test_upload(self, filename="~/Testfiles/Sample1.vcf"):
		assert os.path.exists(filename)
		upload = uploadScript.upload(filename)
		assert upload == True:
