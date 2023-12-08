from abc import ABC, abstractmethod


class Agent(ABC):
	fitness = None

	@abstractmethod
	def __init__(self,level):
		raise NotImplementedError("")



class simpleAgent(Agent):
	def __init__(self, level):
		self.point = []
		self.types = []
