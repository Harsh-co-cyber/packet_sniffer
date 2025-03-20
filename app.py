from flask import Flask, render_template, request, jsonify
from scapy.all import sniff, IP, TCP, UDP

app = Flask(__name__)

captured_packets = []

def packet_callback(packet):
    """Callback function to process captured packets"""
    if IP in packet:
        packet_info = {
            "summary": packet.summary(),
            "src": packet[IP].src,
            "dst": packet[IP].dst,
            "proto": "TCP" if TCP in packet else "UDP" if UDP in packet else "Other",
            "payload": str(packet.payload)
        }
        captured_packets.append(packet_info)

@app.route('/')
def index():
    return render_template("index.html", packets=[])

@app.route('/capture', methods=['POST'])
def capture_packets():
    global captured_packets
    captured_packets = []  # Reset packet storage

    ip_address = request.json.get("ip_address")
    packet_type = request.json.get("packet_type").upper()
    count = int(request.json.get("count"))

    # Packet filter logic
    filter_str = ""
    if ip_address:
        filter_str += f"host {ip_address} "
    if packet_type in ["TCP", "UDP"]:
        filter_str += f"and {packet_type.lower()}"

    # Start capturing packets
    sniff(filter=filter_str.strip(), prn=packet_callback, count=count, store=False)

    return jsonify({"status": "success", "packets": captured_packets})

if __name__ == "__main__":
    app.run(debug=True)
