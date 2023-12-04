from flask import Flask, request, jsonify
import subprocess, os
from sys import platform

app = Flask(__name__)

hash = 'ym8ZTDQtgN5eTaqJz38gGxYkYCz223KmWYMh93RZGwUTwSSybDp5CF9HqmnuermXvQKvPBCta94NRWUzBxwpXvgJVBdezkdbx2jzykuGyDTm'
path = os.path.abspath(os.path.dirname(__file__))
real = False
if platform == "linux" or platform == "linux2":
    # linux
    real = True


@app.route('/ping/<hashcode>', methods=["GET"])
def ping(hashcode):
	if hashcode == hash:
		return "SERVED"
#		return jsonify(isError=False,
#					   message="Success",
#					   statusCode=200,
#					   data={"data":"served"})"""
	else:
		return ""


@app.route('/pings', methods=["POST"])
def pings():
	hashcode = request.headers.get("hashcode")
#	hashcode = request.args.get('hashcode')
	if hashcode:
		if hashcode == hash:
			return "SERVED"
	#		return jsonify(isError=False,
	#					   message="Success",
	#					   statusCode=200,
	#					   data={"data":"served"})"""
	return ""


@app.route('/change/<interface>/<mode>', methods=["POST"])
def change(interface, mode):
	hashcode = request.args.get('hashcode')
	if hashcode:
		if hashcode == hash:
			if real:
				default_command = ['sudo', 'pipenv', 'run', 'python', f'{path}/setting_config.py', '-i', f'{interface}', '-m', f'{mode}']
			else:
				default_command = ['pipenv', 'run', 'python', f'{path}/setting_config.py', '-i', f'{interface}', '-m', f'{mode}']
			if interface == "wifi":
				ssid = request.args.get('ssid')
				passw = request.args.get('pass')
				default_command = default_command + ['-ssid', f'{ssid}', '-pass', f'{passw}']
			if mode == "static":
				ip = request.args.get('ip')
				netmask = request.args.get('netmask')
				gateway = request.args.get('gateway')
				dns1 = request.args.get('dns1')
				dns2 = request.args.get('dns2')
				default_command = default_command + ['-ip', f'{ip}', '-nm', f'{netmask}', '-g', f'{gateway}', '-dns1', f'{dns1}', '-dns2', f'{dns2}']
			#print(default_command)
			res = subprocess.run(default_command, capture_output=True, text=True)

			return f"{res.stdout}"

@app.route('/getSetting', methods=["GET", "POST"])
def getSetting():
	hashcode = request.args.get('hashcode')
	if hashcode:
		if hashcode == hash:
			if real:
				default_command = ['sudo', 'pipenv', 'run', 'python', f'{path}/setting_config.py', '-i', 'setting']
			else:
				default_command = ['pipenv', 'run', 'python', f'{path}/setting_config.py', '-i', 'setting']
			#print(default_command)
			res = subprocess.run(default_command, capture_output=True, text=True)
			#print(res.stdout)
			return f"{res.stdout}"

@app.route('/reboot', methods=["POST"])
def reboot():
	hashcode = request.args.get('hashcode')
	if hashcode:
		if hashcode == hash:
			command_kill = ['sudo', 'killall', 'wpa_supplicant']
			res = subprocess.run(command_kill, capture_output=True, text=True)

#			command = ['sudo', 'systemctl', 'restart', 'NetworkManager']
#			res = subprocess.run(command, capture_output=True, text=True)
#			if res.stdout == "":

			command = ['sudo', 'ip', 'addr', 'flush', 'dev', 'eth0']
			res = subprocess.run(command, capture_output=True, text=True)

			command = ['sudo', 'ip', 'addr', 'flush', 'dev', 'wlan0']
			res = subprocess.run(command, capture_output=True, text=True)

			command = ['sudo', 'systemctl', 'restart', 'networking']
			res = subprocess.run(command, capture_output=True, text=True)
			if res.stdout == "":
				return f"SUCCESS"
	#return ""
#change wifi and etc here


# main driver function
if __name__ == '__main__':

	# run() method of Flask class runs the application
	# on the local development server.
	app.run(host='0.0.0.0', port=8789)
