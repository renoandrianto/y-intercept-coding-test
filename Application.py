from LogComponent import ILog
import asyncio
import datetime

# Test writing 100000 lines of strings
async def test_write():
	logger = ILog()
	await logger.start()
	for _ in range(100000):
		await logger.write("Test")
	print("Some other task...") # This will print first

# Two files will be created
async def test_midnight():
	logger_now = ILog()
	await logger_now.start()
	await logger_now.write("Today")

	tomorrow_date = datetime.datetime.now() + datetime.timedelta(days=1)
	logger_tomorrow = ILog(tomorrow_date)
	await logger_tomorrow.start()
	await logger_tomorrow.write("Tomorrow")

# Not working as expected, I intend to compare the number of lines printed if we stop right away or wait to finish writing outstanding logs
async def test_stop(wait=False):
	logger = ILog()
	await logger.start()
	for _ in range(100000):
		await logger.write("Test")
	await asyncio.sleep(0.2)
	await logger.stop_write(False)

	with open(f"{datetime.datetime.now().date()}.txt", 'r') as file:
		lines = file.readlines()
		print(len(lines))

if __name__ == "__main__":
	# Uncomment the lines to test out different requirements
	asyncio.run(test_write())
	# asyncio.run(test_midnight())
	# asyncio.run(test_stop(wait=True))
	# asyncio.run(test_stop())
	print("Finished asynchronous writing!")