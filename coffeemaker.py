from flask import Flask, render_template
#import coffeemaker_class
import time, threading, math, datetime

class CoffeeMaker :
	CUP_WEIGHT = 3
	POT_WEIGHT = 15

	def __init__(self) :
		self.weight = 51
		self.cups = 5
 		self.off_scale = False
 		self.running_low = False
 		self.status = "Good"
 		self.last_filled_time = time.time()

 		self.start_scale_timer()

 	def start_scale_timer(self) :
 		self.read_scale()
 		self.handle_weight()
 		threading.Timer(10, self.start_scale_timer).start()

 	def read_scale(self) :
 		# gonna need to put something in here to handle force on the pot. 
 		# maybe if it's signigicantly greater than the last weight, throw that weight out and mark a flag
 		# if it's significantly more twice in a row, accept the increased weight 
		self.weight = self.weight - 1
		if self.weight == 0 :
			self.weight = 51

	def handle_weight(self):
		self.cups = math.floor((self.weight- self.POT_WEIGHT) / self.CUP_WEIGHT)
		if (self.cups <= 0) :
			self.check_for_present()
		elif (self.cups <= 2) :
			self.running_low = True
			self.status = "Low"
		else :
			self.running_low = False

	def check_for_present(self) :
		self.read_scale()
		if(self.weight < self.POT_WEIGHT) :
			self.off_scale = True
			self.status = "Off"
			threading.Timer(2, self.check_for_present).start()
		else :
			self.off_scale = False
			self.status = "Good"
			self.last_filled_time = time.time()

		
	
app = Flask(__name__)
cm = CoffeeMaker()

@app.route("/")
def homepage():
	time_since = datetime.datetime(1,1,1) + datetime.timedelta(seconds=time.time()-cm.last_filled_time)
	return render_template('index.html', weight=cm.weight, status=cm.status, cups=cm.cups, time_since_last=time_since.minute)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
