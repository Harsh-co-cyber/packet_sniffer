from flask import Flask, request, jsonify
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

@app.route('/capture', methods=['POST'])
def capture_packets():
    try:
        data = request.json
        ip_address = data.get('ip_address', None)
        packet_type = data.get('packet_type', None)
        count = data.get('count', 10)  # Default to 10 packets

        filter_str = ''
        if packet_type:
            filter_str += packet_type.lower()
        if ip_address:
            filter_str += f' and host {ip_address}'
        
        captured_packets = sniff(filter=filter_str if filter_str else None, count=count)
        packet_list = [packet_callback(pkt) for pkt in captured_packets]
        
        return jsonify({'status': 'success', 'packets': packet_list})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)