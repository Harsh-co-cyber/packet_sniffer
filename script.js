async function capturePackets() {
    const ipAddress = document.getElementById('ip_address').value;
    const packetType = document.getElementById('packet_type').value;
    const count = document.getElementById('count').value;

    const requestBody = {
        ip_address: ipAddress,
        packet_type: packetType,
        count: parseInt(count)
    };

    try {
        const response = await fetch('/capture', {  // Note: No need for localhost:5000, Flask handles this
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });

        const result = await response.json();

        if (result.status === 'success') {
            displayPackets(result.packets);
        } else {
            displayError(result.message);
        }
    } catch (error) {
        displayError('Error capturing packets: ' + error.message);
    }
}

function displayPackets(packets) {
    const outputDiv = document.getElementById('output');
    outputDiv.innerHTML = '';

    packets.forEach(packet => {
        const packetDiv = document.createElement('div');
        packetDiv.innerHTML = `
            <strong>Summary:</strong> ${packet.summary}<br>
            <strong>Source:</strong> ${packet.src}<br>
            <strong>Destination:</strong> ${packet.dst}<br>
            <strong>Protocol:</strong> ${packet.proto}<br>
            <strong>Payload:</strong> ${packet.payload}<br><br>
        `;
        outputDiv.appendChild(packetDiv);
    });
}

function displayError(message) {
    const outputDiv = document.getElementById('output');
    outputDiv.innerHTML = `<span style="color: red;">${message}</span>`;
}
