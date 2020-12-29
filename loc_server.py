from flask import Flask, render_template
import subprocess, math, webbrowser, sys, os

app = Flask(__name__)
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# References = https://ammonsonline.com/is-it-hot-in-here-or-is-it-just-my-cpu/ &
# https://www.udoo.org/forum/threads/reading-cpu-temperature-with-python-on-windows-10.14818/

def handler():
    hand = """
    $t = Get-WmiObject MSAcpi_ThermalZoneTemperature -Namespace “root/wmi”
     
    while (1) {$t.CurrentTemperature; sleep 5}
    """
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    cmd = ['powershell.exe', '-Command', hand]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, startupinfo=si)
    dgree = '\u00b0'
    fd = open(r'templates/temp.txt', 'w')
    tmp = proc.stdout.readline()
    proc.stdout.readline()
    farr = (((int(tmp) / 10) - 273.15) * (9 / 5) + 42)
    farr_str = (f'OVERALL TEMP: {str(math.ceil(farr))}F')
    fd.write(farr_str)
    fd.close()


@app.route('/')
def hello():
    handler()
    with open('templates/temp.txt', 'r') as foo:
        stepuno = str(foo.read())
        dos = stepuno.split(';')
        data = [
            {
                'temp': f'{dos}]',
            }]
        return render_template("home.html", data=dos)


if __name__ == '__main__':
    webbrowser.open('http://localhost:5000', new=0)
    app.run(debug=True, host='0.0.0.0')
