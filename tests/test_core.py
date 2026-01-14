import unittest
from unittest import mock

from modules.Attack.BruteForce.bruteforce import Bruteforce
from modules.Attack.core import Core


def mock_fun():
    return "pass"


class TestCoreClass(unittest.TestCase):

    def test_import_in_core(self):
        core = Core("Bruteforce")
        self.assertEqual(core.class_, "Bruteforce")
        self.assertEqual(core.module, 'bruteforce')


    def test_core_run(self):
        with mock.patch.object(Bruteforce, "run") as mock_method:
            bruteforce = Core("Bruteforce")
            bruteforce.run()
            mock_method.assert_called_once()
