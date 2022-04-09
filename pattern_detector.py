import _thread
import time


class PatternDetector:
	pattern = []
	press_ms = 500
	pin = None
	callback_fn = None
	call_args = None
	state = 0
	CHECK = False

	def check_pattern():
		#await asyncio.sleep(0)
		if pin != None:
			self.state = self.pin.value()
		while CHECK:
			if self.state != self.pin.value()
				self.state = self.pin.value()
				self.pattern.append( self.state )
			#await asyncio.sleep(0)

		print(self.pattern)

	async def start():
		self.CHECK = True
		_thread.start_new_thread(check_pattern, ())
		time.sleep(press_ms)
		self.CHECK = False

	





