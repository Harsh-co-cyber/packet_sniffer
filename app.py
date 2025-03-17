from flask import Flask, request, render_template
from scapy.all import sniff

app = Flask(__name__)
def packet_callback(packet):
    return {
        'summary': packet.summary(),
        'src': packet.src if hasattr(packet, 'src') else None,
        'dst': packet.dst if hasattr(packet, 'dst') else None,
        'proto': packet.proto if hasattr(packet, 'proto') else None,
        'payload': str(packet.payload)
    }
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
@app.route('/capture', methods=['POST'])
def capture_packets():
    ip_address = request.form.get('ip_address')
    packet_type = request.form.get('packet_type')
    count = int(request.form.get('count', 10))

    filter_str = ''
    if packet_type:
        filter_str += packet_type.lower()
    if ip_address:
        filter_str += f' and host {ip_address}'
    captured_packets = sniff(filter=filter_str, count=count)
    packet_list = [packet_callback(pkt) for pkt in captured_packets]
    return render_template('index.html', packets=packet_list)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)