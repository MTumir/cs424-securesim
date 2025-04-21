from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import logging
import threading
import time
from process_sim.temperature_control import TemperatureControl
from control_logic.tc_controller import TC_Controller
from attacks.false_data_injection import FalseDataInjection
from attacks.dos_attack import DoSAttack
from attacks.replay_attack import ReplayAttack
from defenses.log_and_audit import LogAndAudit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
logger = logging.getLogger(__name__)

# Shared simulation objects
tc = TemperatureControl(low_bound=40.0, high_bound=50.0)
controller = TC_Controller(tc)
injection = FalseDataInjection(tc)
dos = DoSAttack(tc)
replay = ReplayAttack(tc)
log_defense = LogAndAudit(tc)

# Store logs in memory for display
log_records = []

# Custom logging handler to capture logs for UI
class WebLogHandler(logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        log_records.append(msg)
        if len(log_records) > 100:  # Limit to 100 logs
            log_records.pop(0)
        socketio.emit('log_update', {'log': msg})

# Set up logging
handler = WebLogHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(handler)

def simulation_thread():
    """Run the simulation and emit temperature updates."""
    tc.start_simulation()
    controller.start_control()
    try:
        while True:
            temp = tc.get_temperature()
            socketio.emit('temperature_update', {
                'temperature': round(temp, 2),
                'low_bound': tc.low_bound,
                'high_bound': tc.high_bound,
                'change_rate': tc.temp_change
            })
            time.sleep(1)
    except Exception as e:
        logger.error(f"Simulation error: {e}")
    finally:
        tc.stop_simulation()
        controller.stop_control()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status')
def status():
    return jsonify({
        'temperature': round(tc.get_temperature(), 2),
        'low_bound': tc.low_bound,
        'high_bound': tc.high_bound,
        'change_rate': tc.temp_change,
        'injection_active': injection.active,
        'dos_active': dos.active,
        'replay_active': replay.active,
        'logging_active': log_defense.active
    })

@app.route('/toggle_attack', methods=['POST'])
def toggle_attack():
    attack_type = request.json.get('attack_type')
    state = request.json.get('state')
    if attack_type == 'injection':
        injection.activate() if state else injection.deactivate()
    elif attack_type == 'dos':
        dos.activate() if state else dos.deactivate()
    elif attack_type == 'replay':
        replay.activate() if state else replay.deactivate()
    logger.info(f"{attack_type} attack {'activated' if state else 'deactivated'}")
    return jsonify({'status': 'success'})

@app.route('/toggle_defense', methods=['POST'])
def toggle_defense():
    defense_type = request.json.get('defense_type')
    state = request.json.get('state')
    if defense_type == 'logging':
        log_defense.activate() if state else log_defense.deactivate()
    logger.info(f"{defense_type} defense {'activated' if state else 'deactivated'}")
    return jsonify({'status': 'success'})

@app.route('/logs')
def get_logs():
    return jsonify({'logs': log_records})

if __name__ == '__main__':
    # Start simulation in a separate thread
    sim_thread = threading.Thread(target=simulation_thread)
    sim_thread.daemon = True
    sim_thread.start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)