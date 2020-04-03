from scipy.integrate import odeint

class predictor:

	def __init__(self, p, z0, t):

		self.p = p
		self.z0 = z0
		self.t = t

	# function to return dz/dt
	def seirs_model(self, z, t):
		p = self.p
		S = z[0]
		E = z[1]
		I = z[2]
		C = z[3]
		R = z[4]
		D = z[5]
		
		N = S+E+I+C+R
		dSdt = p[0]*N + p[9]*R - p[1]*S - p[2]*S*(I/N) - p[3]*S*(C/N)
		dEdt = p[2]*S*(I/N) + p[3]*S*(C/N) - p[1]*E - p[4]*E - p[5]*E  
		dIdt = p[4]*E - p[1]*I - p[6]*I
		dCdt = p[5]*E - p[1]*C - p[7]*C - p[8]*C
		dRdt = p[7]*C + p[6]*I - p[1]*R - p[9]*R
		dDdt = p[8]*C
		return [dSdt, dEdt, dIdt, dCdt, dRdt, dDdt]

	def predict(self):
		return odeint(self.seirs_model, self.z0, self.t)