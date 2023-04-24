#!/usr/bin/env python3

import multiprocessing
import socket
from unittest import TestCase, main, mock
import time

import sqroots
import server


class TestSqroots(TestCase):
    def test_sqr1(self):
        self.assertEqual(sqroots.sqroots("1 2 1"), "-1.00")

    def test_sqr2(self):
        self.assertEqual(sqroots.sqroots("1 2 0"), "-2.00 0.00")

    def test_sqr3(self):
        self.assertEqual(sqroots.sqroots("1 2 3"), "")

    def test_sqr4(self):
        with self.assertRaises(ValueError):
            sqroots.sqroots("1 2")

    def test_sqr5(self):
        with self.assertRaises(ValueError):
            sqroots.sqroots("0 2 3")


class TestServer(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proc = multiprocessing.Process(target=server.serve)
        cls.proc.start()
        time.sleep(2)  # Да, это костыль!

    def setUp(self):
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.connect(("localhost", 1337))
        self.s = _socket

    def test_server1(self):
        self.assertEqual(sqroots.sqrootnet("1 2 1", self.s), "-1.00\n")

    def test_server2(self):
        self.assertEqual(sqroots.sqrootnet("1 2 0", self.s), "-2.00 0.00\n")

    def test_server3(self):
        self.assertEqual(sqroots.sqrootnet("1 2 3", self.s), "\n")

    def test_server4(self):
        self.assertEqual(sqroots.sqrootnet("1 2", self.s), "\n")

    def test_server5(self):
        self.assertEqual(sqroots.sqrootnet("0 2 3", self.s), "\n")

    def tearDown(self):
        self.s.close()

    @classmethod
    def tearDownClass(cls):
        cls.proc.kill()


# class TestSqrootnet(TestCase):

#     def setUp(self):
#         self.s = mock.MagicMock()
#         self.s.sendall = mock.MagicMock()
