import csv
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
import graphics as graphics

root = tk.Tk()

class Application(tk.Frame):
	def __init__(self,planets, master=None):
		tk.Frame.__init__(self, master)
		self.grid(column = 0, row = 0,padx=(50,50),pady=(10,10))
		self.columnconfigure(0,weight=1)
		self.rowconfigure(0,weight=1)
		self.time_entry = tk.Entry(self)
		self.Labels= []

		self.animation_time = 0
		self.planets = planets
		self.active_planets = []

		self.pack()
		self.createWidgets()
		self.draw()

	def time(self):
		if self.time_entry.get() != "":
			t = float(self.time_entry.get())
		else:
			self.animation_time += 1/30
			t = self.animation_time

		return t

	def draw(self):
		t = self.time()

		for i, planet in enumerate(self.planets):

			self.Labels[i*5].grid_remove()
			self.Labels[i*5+1].grid_remove()
			self.Labels[i*5+2].grid_remove()
			self.Labels[i*5+3].grid_remove()
			self.Labels[i*5+4].grid_remove()

			if(self.active_planets[i].get()):
				self.Labels[i*5] = tk.Label(self, text = "U: "+ str(planet.u(t)))
				self.Labels[i*5].grid(column = 2, row = i*5)
				self.Labels[i*5+1] = tk.Label(self, text = "C: "+ str(planet.angular_momentum(t)))
				self.Labels[i*5+1].grid(column = 2, row = i*5+1)
				self.Labels[i*5+2] = tk.Label(self, text = "H: "+ str(planet.energy(t)))
				self.Labels[i*5+2].grid(column = 2, row = i*5+2)
				self.Labels[i*5+3] = tk.Label(self, text = "X: "+ str(planet.position(t)))
				self.Labels[i*5+3].grid(column = 2, row = i*5+3)
				self.Labels[i*5+4] = tk.Label(self, text = " ")
				self.Labels[i*5+4].grid(column = 2, row = i*5+4)

		graphics.draw(self.planets,self.active_planets, t)

		self.after(500,self.draw)

	def createWidgets(self):
		for i, planet in enumerate(self.planets):
			self.active_planets.append(tk.IntVar())
			tk.Checkbutton(self, text=planet.name, variable = self.active_planets[i]).grid(column = 1, row = i*5)
			self.Labels.append(tk.Label(self,text = ""))
			self.Labels.append(tk.Label(self,text = ""))
			self.Labels.append(tk.Label(self,text = ""))
			self.Labels.append(tk.Label(self,text = ""))
			self.Labels.append(tk.Label(self,text = ""))

		#tk.Button(self, text="Hello World", command=lambda: self.say_hi(1)).pack(side="top")
		#tk.Button(self, text="Hello World 2", command=lambda: self.say_hi(2)).pack(side="top")
		#tk.Button(self, text="Hello World 3", command=lambda: self.say_hi(3)).pack(side="top")

		#self.num = tk.Label(self,text = "Num click: "+str(self.num_clicks),textvariable = self.text)
		#self.num.pack(side="top")

		self.time_entry.grid(column = 1, row = 50)

		self.QUIT = tk.Button(self, text="QUIT", fg="red",
		                                    command=root.destroy)
		self.QUIT.grid(column = 2, row = 50)

	def say_hi(self,num):
		print("hi there, everyone!")
		self.num_clicks += num
		self.text.set("Num click: "+str(self.num_clicks))
		print(str(self.num_clicks))

class Planet:
	def __init__(self, name, a, epsilon, period, initial_time, precision,r ,g ,b,radius):
		self.name = name
		self.a = a
		self.epsilon = epsilon
		self.period = period
		self.initial_time = initial_time
		self.precision = precision
		self.mu = (4 * np.pi**2 * self.a**3)/ (self.period**2)

		self.r = r
		self.g = g
		self.b = b
		self.radius = radius

	def u(self, t):
		current_u = np.pi
		last_u = 0

		xi = (2 * np.pi)/self.period *(t - self.initial_time)

		while (np.abs(current_u - last_u) > self.precision):
			last_u = current_u
			current_u = (self.epsilon * (np.sin(current_u) - current_u * np.cos(current_u))+ xi) / (1 - self.epsilon * np.cos(current_u))

		return current_u

	def du(self, t):
		return np.sqrt(self.mu) / (self.a ** (3/2) * (1 - self.epsilon* np.cos(self.u(t))))

	def position(self, t):
		return np.multiply(self.a,(np.cos(self.u(t)) - self.epsilon , np.sqrt(1- self.epsilon ** 2) * np.sin(self.u(t))))

	def energy(self, t):

		return (self.mu *(-1 + self.epsilon* np.cos(self.u(t)))) / (2* self.a*(1-self.epsilon*np.cos(self.u(t))))

	def angular_momentum(self, t):

		return  (0,0,self.a**2 * self.du(t) *np.sqrt(1-self.epsilon**2)*(1 - self.epsilon* np.cos(self.u(t))))


def main():

	planets = []

	with open('data.csv') as csvfile:
		reader = csv.DictReader(csvfile)

		for row in reader:
			print(row['name'])
			print('RGB: '+ row['r']+' '+ row['g'] + ' ' + row['b'])
			planets.append(Planet(row['name'],float(row['a']), float(row['epsilon']), float(row['period']), float(row['initial_time']), 0.0001,
								  float(row['r']),float(row['g']),float(row['b']),float(row['radius'])))

	graphics.initGlut("")
	graphics.initOpenGL()

	app = Application(planets, master=root)
	app.mainloop()
	#t = 0

	#while (t != -1):
	#	t = input("Set time: ")

	#	t = float(t)

	#	for planet in planets:
	#		print(planet.name)
	#		print("Energy: " +  str(planet.energy(t)))
	#		print("Anguar momentum: " +  str(planet.angular_momentum(t)))
	#		print("Eccentric anomaly: " + str(planet.u(t)))

	#time_samples = np.arange(0,1,0.001)

	#Draw orbit

	#points = [earth.position(time) for time in time_samples]

	#x = [point[0] for point in points]
	#y = [point[1] for point in points]

	#plt.plot(x,y)
	#plt.show()

if __name__ == '__main__':
	main()
