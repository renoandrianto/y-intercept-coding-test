import datetime
import asyncio

class ILog:
	def __init__(self, ct = datetime.datetime.now()):
		self.file_name = f"{ct.date()}.txt" # If midnight has passed, then filename will change
		self.queue = asyncio.Queue()
		self.writing = True
		self.running = True

	async def write(self, content):
		# Add string to buffer queue
		if self.writing:
			await self.queue.put(content)
	
	async def stop_write(self, wait=False):
		self.writing = False # Stop putting more strings to the buffer
		if wait:
			while not self.queue.empty():
				# If wait, keep blocking the stop task for 0.2 sec and continue writing until outstanding logs are empty
				asyncio.sleep(0.2) 
		self.running = False # Stop the main logging routine
		print("Writing finished")

	async def main_logger(self):
		while self.running:
			message = await self.queue.get()
			# Use try catch to prevent application from being put down
			try:
				with open(self.file_name, 'a') as file: # If filename changes, new file is created, else append
					file.write(message + '\n')
			except Exception as e:
				print(f"An error occured during write to file {e}")
			self.queue.task_done()

	 # Starts the logger by creating a writer subroutine
	async def start(self):
		asyncio.create_task(self.main_logger())
