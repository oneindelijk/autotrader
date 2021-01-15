import unittest
import shutil
import appdirs
from utils.common import get_mysql_secrets
from utils.at_exceptions import MissingParameter
class TestSecrets(unittest.TestCase):

    def setUp(self):

        ''' create config files to be used '''

        self.non_existent_cfg = '/tmp/nonexistentconfig.cfg4566654'
        self.emptytestfile = '/tmp/example_emptytestfile.cfg'
        self.nousertestfile = '/tmp/example_nousertestfile.cfg'
        self.nopasswordtestfile = '/tmp/example_nopasswordtestfile.cfg'
        self.oktestfile = '/tmp/example_oktestfile.cfg'
        self.oktestfile_upper_param = '/tmp/example_oktestfile_upper_param.cfg'
        cts = ''
        with open(self.emptytestfile, 'w') as FD:
            FD.write(cts)
        cts = 'password = verys3cr3T\n'
        with open(self.nousertestfile, 'w') as FD:
            FD.write(cts)
        cts = 'user = user\n'
        with open(self.nopasswordtestfile, 'w') as FD:
            FD.write(cts)
        cts = 'password = verys3cr3T\nuser = user\n'
        with open(self.oktestfile, 'w') as FD:
            FD.write(cts)
        cts = 'password = verys3cr3T\nuser = user\nPORT = 5566\n'
        with open(self.oktestfile_upper_param, 'w') as FD:
            FD.write(cts)


    def test_setup(self):

        ''' test if test conditions are okay '''

        self.assertFalse(shutil.os.path.exists(self.non_existent_cfg))
        self.assertTrue(shutil.os.path.exists(self.emptytestfile))
        self.assertTrue(shutil.os.path.exists(self.nousertestfile))
        self.assertTrue(shutil.os.path.exists(self.nopasswordtestfile))
        self.assertTrue(shutil.os.path.exists(self.oktestfile))
        self.assertTrue(shutil.os.path.exists(self.oktestfile_upper_param))

    def test_file_absent(self):

        ''' test if error is raised with non-existing file '''
        
        with self.assertRaises(FileNotFoundError):
            get_mysql_secrets(self.non_existent_cfg)

    def test_missing_contents(self):

        ''' test exceptions raised with empty file '''
        
        with self.assertRaises(MissingParameter):
            get_mysql_secrets(self.emptytestfile)

    def test_missing_user(self):

        ''' test exceptions raised with user missing '''

        with self.assertRaises(MissingParameter):
            get_mysql_secrets(self.nousertestfile)

    def test_missing_passwd(self):

        ''' test exceptions raised with user missing '''

        with self.assertRaises(MissingParameter):
            get_mysql_secrets(self.nopasswordtestfile)

    def test_return_dictionnary(self):

        ''' test exceptions raised with user missing '''

        obj = get_mysql_secrets(self.oktestfile)
        self.assertIsInstance(obj, dict)

    def test_upper_parameter_name(self):

        ''' test parameters in uppercase valid'''

        obj = get_mysql_secrets(self.oktestfile_upper_param)
        self.assertTrue('port' in obj)

    def tearDown(self):
        files =[self.non_existent_cfg,
                self.emptytestfile,
                self.nousertestfile,
                self.nopasswordtestfile,
                self.oktestfile,
                self.oktestfile_upper_param,]
        for file in files:
            if shutil.os.path.exists(file):
                shutil.os.remove(file)