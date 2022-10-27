import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

G = 10

# menghitung waktu terbang hingga menyentuh sasaran


def t(yt, xt, degree):
    sudut = np.radians(degree)
    return round(np.sqrt((((xt/np.cos(sudut))*np.sin(sudut)-yt)/(1/2))/G), 2)


# menghitung kecepatan awal yang diperlukan untuk mencapai sasaran

def v0(yt, xt, degree):
    sudut = np.radians(degree)
    return round((xt/np.cos(sudut))/t(yt, xt, degree), 2)


# menghitung waktu terbang hingga menyentuh tanah

def t_ground(v0, degree):
    return (2*v0*np.sin(np.radians(degree))/G)


# menghitung jarak horizontal


def x(v0, t, degree):
    t_max = t_ground(v0, degree)
    v_horizontal = v0*np.cos(np.radians(degree))
    if (t <= t_max):
        return v_horizontal*t
    else:
        return v_horizontal*t_max


# menghitung jarak vertikal

def y(v0, t, degree):
    v_vertikal = v0*np.sin(np.radians(degree))
    h = v_vertikal*t - 0.5*G*t**2
    if h > 0:
        return h
    else:
        return 0


# MAIN PROGRAM
tinggi_sasaran = float(input("masukkan Tinggi Sasaran (m): "))
jarak_sasaran = int(input("masukkan Jarak Sasaran (m): "))

sudut_pemanah = int(input("masukkan Sudut Elevasi (derajat): "))
v0 = v0(tinggi_sasaran, jarak_sasaran, sudut_pemanah)
t = t(tinggi_sasaran, jarak_sasaran, sudut_pemanah)


# Penetapan interval waktu
time_interval = 0.1
time_steps = np.arange(0, t + time_interval, time_interval)


def update_category(num, lines):
    for i in range(len(lines)):
        lines[i].set_data(x[i][0: num], y[i][0: num])
    tm = np.round(num*time_interval, 1)
    plt.title('Kecepatan awal: {} m/s | Waktu simulasi: {} detik'.format(v0, tm))
    return lines


# Penetapan jarak horizontal dan vertikal
x = [[x(v0, time_step, sudut_pemanah)
      for time_step in np.arange(0, t, time_interval)]]
y = [[y(v0, time_step, sudut_pemanah)
      for time_step in np.arange(0, t, time_interval)]]

# membuat plot animasi
h_max = np.ceil(max([max(x[i]) for i in range(len(x))]))
v_max = np.ceil(max([max(y[i]) for i in range(len(y))]))

fig, ax = plt.subplots()
ax.set_xlim(0, v_max)
ax.set_ylim(0, h_max)
plt.gca().set_aspect('equal', adjustable='box')
plt.xlabel('Jarak horizontal (m)')
plt.ylabel('Jarak vertikal (m)')
plt.grid(True, which='both')

lines = [ax.plot([], [], label='{} degree'.format(sudut_pemanah))[0]]
ax.axis([0, h_max, 0, v_max])
ax.scatter(jarak_sasaran, tinggi_sasaran, c='r', label='Sasaran')
ax.legend()

ani = animation.FuncAnimation(fig, update_category, frames=len(
    time_steps), fargs=[lines], interval=1000*time_interval)

plt.show()
