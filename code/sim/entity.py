from abc import ABC, abstractmethod

class IEntity(ABC):
	@abstractmethod
	def __init__():
		raise NotImplementedError("")

	@abstractmethod
	def update(self, env):
		raise NotImplementedError("")

	@abstractmethod
	def draw(self, graphics):
		raise NotImplementedError("")
