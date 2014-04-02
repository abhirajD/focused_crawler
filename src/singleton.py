"""Author: Enfeng Huang @ NYU Polytechnic School of Engineering, 2014-02
Singleton design pattern"""

def singleton(cls):
	instances = {}
	def f(*args, **kwargs):
		if cls not in instances:
			instances[cls] = cls(*args, **kwargs)
		return instances[cls]
	return f

