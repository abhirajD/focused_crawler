#!/usr/bin/python

"""Author: Enfeng Huang @ NYU Polytechnic School of Engineering, 2014-02"""

import threading
import singleton

@singleton.singleton
class Downloader:
	def __init__(self):
		self.thread_list = []

	def start(self, xtarget, *args, **kwargs):
		t = threading.Thread(target = xtarget, *args, **kwargs)
		t.start()
		self.thread_list.append(t)

	def join(self):
		for t in self.thread_list:
			t.join()

