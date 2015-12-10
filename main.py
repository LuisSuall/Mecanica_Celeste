import numpy as np
import matplotlib.pyplot as plt

class Planet:
	def __init__(self, a, epsilon, period, initial_time, precision):
		self.a = a
		self.epsilon = epsilon
		self.period = period
		self.initial_time = initial_time
		self.precision = precision

	def u(self, t):
		current_u = np.pi
		last_u = 0

		xi = (2 * np.pi)/self.period *(t - self.initial_time)

		while (np.abs(current_u - last_u) > self.precision):
			last_u = current_u
			current_u = (self.epsilon * (np.sin(current_u) - current_u * np.cos(current_u))+ xi) / (1 - self.epsilon * np.cos(current_u))

		return current_u

	def position(self, t):
		return np.multiply(self.a,(np.cos(self.u(t)) - self.epsilon , np.sqrt(1- self.epsilon ** 2) * np.sin(self.u(t))))

	def energy(self, t):
		mu = (4 * np.pi**2 * self.a**3)/ (self.period**2)

		return (mu *(-1 + self.epsilon* np.cos(self.u(t)))) / (2* self.a*(1-self.epsilon*np.cos(self.u(t))))

	def angular_momentum(self, t):
		return (0,0,1 - self.epsilon* np.cos(self.u(t)))


def main():

	earth = Planet(1, 0.017, 1,0,0.0001)

	t = 0

	while (t != -1):
		t = input("Set time: ")

		t = float(t)

		print("Energy: " +  str(earth.energy(t)))
		print("Anguar momentum: " +  str(earth.angular(t)))
		print("Eccentric anomaly: " + str(earth.u(t)))

		time_samples = np.arange(0,1,0.001)

	#Draw orbit

	points = [earth.position(time) for time in time_samples]

	x = [point[0] for point in points]
	y = [point[1] for point in points]

	plt.plot(x,y)
	plt.show()

if __name__ == '__main__':
	main()
