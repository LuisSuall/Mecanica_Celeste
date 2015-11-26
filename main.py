import numpy as np
import matplotlib.pyplot as plt

def u(t):
	return t * 2 *np.pi

class Planet:
	def __init__(self, a, epsilon, u):
		self.a = a
		self.epsilon = epsilon
		self.u = u

	def position(self, t):
		return np.multiply(self.a,(np.cos(self.u(t)) - self.epsilon,np.sqrt(1- self.epsilon ** 2) * np.sin(self.u(t))))

def main():
	
	earth = Planet(1, 0.017, u)

	time_samples = np.arange(0,1,0.001)
	print (time_samples[0])
	points = [earth.position(time) for time in time_samples]

	x = [point[0] for point in points]
	y = [point[1] for point in points]

	plt.plot(x,y)
	plt.show()

if __name__ == '__main__':
	main()
