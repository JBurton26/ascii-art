import abc
import time
import logging

class Profiler(abc.ABC):
	def __init__(self):
		self.logger = logging.getLogger(f"{__name__}")

	@abc.abstractmethod
	def start(self):
		# Code to start here expanded in child classes
		pass
	@abc.abstractmethod
	def stop(self):
		# Code to stop here expanded in child classes
		pass
	@abc.abstractmethod
	def report(self):
		# Code to report profiling results expanded in child classes
		pass

class TimerProfile(Profiler):
	# Initialiser for class
	def __init__(self):
		# Values not assigned as they will be assigned during execution
		super().__init__()
		self.logger.debug("TimerProfiler Initialised")
		self.start_time = None 
		self.stop_time = None

	# Magic methods for using the class as a context manager
	def __enter__(self):
		self.start()
		return self

	def __exit__(self, *args):
		self.stop()
		self.report()
		return args

    # Full implementations of abstract methods
	def start(self):
		self.start_time = time.monotonic()

	def stop(self):
		self.stop_time = time.monotonic()

	def report(self):
		duration = self.stop_time - self.start_time if self.stop_time and self.start_time else None
		self.logger.info(f"Time taken: {duration:.2f} s")
		return duration