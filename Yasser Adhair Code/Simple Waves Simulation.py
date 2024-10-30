import matplotlib as mpl
import matplotlib.pyplot as plt
import math
import numpy as np

A = 1
waveLength = 0.5
c = 340
phase_shift = 0
f_unit = 'Hz'
t_unit = 'ms'
a_unit = 'm'
waveLength_unit = 'm'
c_unit = 'm/s'


N_waves = 4
points = 1000
x_values =  np.linspace(0,N_waves*waveLength,points)

f = c/waveLength
omega = math.pi * 2 * f
k = (2 * math.pi) / waveLength

T = 1/f
start_time = 0
time = 0
dt = T/8


wave1_disturbance = []
wave2_disturbance = []

for x in x_values:
    disturbance_temp = A * math.cos((k*x) - (omega*start_time) - phase_shift)
    wave1_disturbance.append(disturbance_temp)
    disturbance_temp = A * math.cos((k*x) - (omega*(start_time+dt)) - phase_shift)
    wave2_disturbance.append(disturbance_temp)

fig, ax = plt.subplots()
wave1 = ax.plot(x_values,wave1_disturbance, color = 'blue', label = 't = t')

wave2 = ax.plot(x_values,wave2_disturbance, color = 'red', label = 't = t + delta_t')
ax.set_ylabel('Wave Disturbance')
ax.set_xlabel('X-location /m')
ax.legend()
ax.grid()
ax.axis([0,N_waves*waveLength,-A*1.5,A*1.5])
plt.show()


