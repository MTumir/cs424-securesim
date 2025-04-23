#!/usr/bin/python3

import time
import random
import argparse
import logging
import threading
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO

from process_sim.temperature_control import TemperatureControl
from control_logic.tc_controller import TC_Controller
from attacks.false_data_injection import FalseDataInjection
from attacks.dos_attack import DoSAttack
from attacks.replay_attack import ReplayAttack
from defenses.log_and_audit import LogAndAudit
from defenses.anomaly_detection import AnomalyDetection
from defenses.command_authentication import CommandAuthentication


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
logger = logging.getLogger(__name__)
current_user = 'admin' #Default user

# Shared simulation objects
tc = TemperatureControl(low_bound=40.0, high_bound=50.0)
controller = TC_Controller(tc)
injection = FalseDataInjection(tc)
dos = DoSAttack(tc)
replay = ReplayAttack(tc)
log_defense = LogAndAudit(tc)
anomaly_defense = AnomalyDetection(tc)
auth_defense = CommandAuthentication(tc)

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

def setup_logging(debug):
    """Set up logging with file and web handlers."""
    log_format = '%(asctime)s - %(filename)s - %(levelname)s - %(message)s'
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format=log_format)
    
    # Add web handler for UI
    web_handler = WebLogHandler()
    web_handler.setFormatter(logging.Formatter(log_format))
    logging.getLogger().addHandler(web_handler)

def simulation_thread():
    """Run the simulation and emit temperature updates."""
    tc.start_simulation()
    controller.start_control()
    try:
        for _ in range(2000):
            randint = random.randint(1, 10)

            if not auth_defense.active or auth_defense.authenticate_command(current_user):
                # Execute attacks randomly
                if randint % 2 == 0:
                    injection.attack()
                if randint >= 5:
                    dos.attack()
                if randint <= 6:
                    replay.attack()
            # else:
            #     logger.warning(f"Attack attempted by unauthorized user '{current_user}' - BLOCKED")    

            anomaly_defense.defend()    

            temp = tc.get_temperature()
            socketio.emit('temperature_update', {
                'temperature': round(temp, 2),
                'low_bound': tc.low_bound,
                'high_bound': tc.high_bound,
                'change_rate': tc.temp_change
            })
            logger.info(f"Temperature: {temp:.2f}°C | Change Rate: {tc.temp_change:.2f}°C/s")
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
        'logging_active': log_defense.active,
        'anomaly_active': anomaly_defense.active
    })

@app.route('/toggle_attack', methods=['POST'])
def toggle_attack():

    if auth_defense.active and not auth_defense.authenticate_command(current_user):
        logger.warning(f"unauthorized attack toggle attempt")
        return jsonify({'status': 'error', 'message': 'Unauthorized user cannot toggle attacks'})

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
    elif defense_type == 'authentication':
        auth_defense.activate() if state else auth_defense.deactivate()
    elif defense_type == 'anomaly':
        anomaly_defense.activate() if state else anomaly_defense.deactivate()
    logger.info(f"{defense_type} defense {'activated' if state else 'deactivated'}")
    return jsonify({'status': 'success'})

@app.route('/logs')
def get_logs():
    return jsonify({'logs': log_records})

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', '-de', action='store_true', help='Enable debug messages')
    parser.add_argument('--injection', '-i', action='store_true', help='Activate injection attacks')
    parser.add_argument('--dos', '-d', action='store_true', help='Activate DoS attacks')
    parser.add_argument('--replay', '-r', action='store_true', help='Activate replay attacks')
    parser.add_argument('--logging', '-l', action='store_true', help='Activate logging defense')
    parser.add_argument('--anomaly', '-an', action='store_true', help='Activate anomaly detection defense')
    parser.add_argument('--authentication', '-a', action='store_true', help='Activate authentication defense')
    parser.add_argument('--ui', '-u', action='store_true', help='Run with UI')
    parser.add_argument('--authentication1', action='store_true', help='Simulate admin command authentication')
    parser.add_argument('--authentication2', action='store_true', help='Simulate intruder command authentication')
    
    args = parser.parse_args()
    
    # Set up logging
    setup_logging(args.debug)

    global current_user
    if args.authentication2:
        current_user = 'intruder'
    else:
        current_user = 'admin'

    # Activate attacks based on args
    if args.injection:
        injection.activate()
    if args.dos:
        dos.activate()
    if args.replay:
        replay.activate()
    if args.logging:
        log_defense.activate()
    if args.anomaly:
        anomaly_defense.activate()
    if args.authentication or args.authentication1 or args.authentication2:
        auth_defense.activate()    
    if args.authentication1:
        demo_command_authentication('admin')
    elif args.authentication2:
        demo_command_authentication('intruder')
    else:
        demo_command_authentication()

    if args.ui:
        # Start simulation in a separate thread
        sim_thread = threading.Thread(target=simulation_thread)
        sim_thread.daemon = True
        sim_thread.start()
        # Run Flask app
        socketio.run(app, host='0.0.0.0', port=5001, debug=args.debug)
    else:
        # Run simulation directly
        try:
            simulation_thread()
        except KeyboardInterrupt:
            print("Stopping simulation...")
    

def demo_command_authentication(user=None):
    print("\n--- Command Authentication Defense Demo ---")
    if user is None:
        users = ['admin', 'intruder']
    else:
        users = [user]
    
    for test_user in users:
        if auth_defense.authenticate_command(test_user):
            print(f"User '{test_user}': Authorized (command allowed)")
        else:
            print(f"User '{test_user}': Unauthorized (command blocked)")
            
    #  display current user status
    print(f"\nCurrent user: '{current_user}'")
    auth_result = auth_defense.authenticate_command(current_user)
    print(f"Attack commands: {'ALLOWED' if auth_result else 'BLOCKED'}")

if __name__ == "__main__":
    main()