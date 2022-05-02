import ssl
import sys
import paho.mqtt.client as suscriptor
import paho.mqtt.publish as publicador
broker = "192.168.0.20"
def on_connect(client, userdata, flags, rc):
	print('Conectado (%s)' % client._client_id.decode())
	client.subscribe(topic='OT', qos=2)

def on_message(client, userdata, message):
	print('-------------------')
	print('topic: %s' % message.topic)
	print('payload: %s' % message.payload)
	print('qos: %d' % message.qos)
	auth={'username':"SCADA_LOLIN_DOWN", 'password':"SCADA_LOLIN_DOWN"}
	publicador.single("OT_DOWN", message.payload,message.qos, auth= auth, hostname=broker)

def main():
	client = suscriptor.Client(client_id='SCADA_LOLIN_DOWN', clean_session=False)
	client.username_pw_set('SCADA_LOLIN_DOWN', 'SCADA_LOLIN_DOWN')
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(host=broker)
	#client.tls_set("/etc/mosquitto/certs/server.crt")
	#client.tls_insecure_set(True)
	#client.connect('192.168.0.18',8883,60)
	client.loop_forever()
if __name__ == '__main__':
	main()
sys.exit(0) 
