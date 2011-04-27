from testify import *

from tron import event

class SimpleStoreTestCase(TestCase):
	@setup
	def build_store(self):
		self.store = event.FixedLimitStore({event.INFO: 2})
	
	@setup
	def add_data(self):
		self.store.append("test1", event.INFO)
		self.store.append("test2", event.INFO)
		self.store.append("test3", event.INFO)
		self.store.append("test4", event.INFO)

		self.store.append("test5", event.ERROR)
		self.store.append("test6", event.ERROR)
		self.store.append("test7", event.ERROR)
		self.store.append("test8", event.ERROR)
		self.store.append("test9", event.ERROR)
	def test(self):
		values = list(self.store)
		
		assert_not_in("test1", values)
		assert_not_in("test2", values)
		assert_in("test3", values)
		assert_in("test4", values)

		assert_in("test5", values)
		assert_in("test6", values)
		assert_in("test7", values)
		assert_in("test8", values)
		assert_in("test9", values)

class ParentEventRecorderTestCase(TestCase):
	@setup
	def build_recorders(self):
		self.parent_recorder = event.EventRecorder(self)
		self.recorder = event.EventRecorder(self, parent=self.parent_recorder)
	
	def test(self):
		self.recorder.record(event.Event(self, event.INFO, "hello"))
		self.recorder.emit_notice("hello again")
		
		assert_equal(self.recorder.list(), self.parent_recorder.list())

		assert_equal(len(self.recorder.list(min_level=event.ERROR)), 0)
		assert_equal(len(self.recorder.list(min_level=event.INFO)), 2)