from flask import Flask, render_template, request
from sympy import symbols, integrate, Rational, cancel

app = Flask(__name__)


# Mendefinisikan simbol-simbol
x, y = symbols("x y")
f = None  # Memberikan nilai awal kosong ke f

@app.route('/')
def first_page():
    return render_template('first.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/materi')
def materi():
    return render_template('materi.html')

@app.route('/hasil', methods=['POST'])
def hasil():
    global f  # Menggunakan f yang didefinisikan di luar fungsi hasil()
    
    # Mendapatkan data dari form
    fungsi_input = request.form['fungsi']
    pilihan_integrasi = request.form['integrasi']
    x_lower = float(request.form['x_lower'])
    x_upper = float(request.form['x_upper'])
    y_lower = float(request.form['y_lower'])
    y_upper = float(request.form['y_upper'])

    # Membuat fungsi
    try:
        f = eval(fungsi_input)  # Evaluasi ekspresi matematika
    except Exception as e:
        return f"Fungsi yang dimasukkan tidak valid: {e}"

    # Menentukan metode integrasi
    if pilihan_integrasi == "dy":
        hasil_integral = integrate(f, (y, y_lower, y_upper), (x, x_lower, x_upper))
    elif pilihan_integrasi == "dx":
        hasil_integral = integrate(f, (x, x_lower, x_upper), (y, y_lower, y_upper))
    else:
        return "Pilihan integrasi tidak valid!"

    # Menampilkan hasil integral dalam bentuk pecahan
    try:
        hasil_pecahan = Rational(float(hasil_integral)).limit_denominator()
    except Exception as e:
        hasil_pecahan = f"Gagal mengonversi ke pecahan: {e}"

    return render_template('index.html', hasil_integral=hasil_integral, hasil_pecahan=hasil_pecahan)

if __name__ == '__main__':
    app.run(debug=True)
