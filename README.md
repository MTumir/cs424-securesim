# ICS Security Final Project: SecureSim

## Contributors
- **Max Tumir**
- **Munib Ahmed**
- **Brandon Nanhthanong**
- **Jackson Price**

---

## Project Overview

**SecureSim** is a simulation of a temperature control system for a chemical tank. It is like what you'd find in an actual industrial control system (ICS). It's built in Python and includes a full **SCADA-style web dashboard**, **cyber-attacks**, and **defensive mechanisms**.

The simulation includes:
- **Natural temperature decay**
- **Control logic** that heats or cools the tank based on thresholds
- **Cyber-attacks** like DoS, False Data Injection, and Replay
- **Defenses** like Logging, Anomaly Detection, and Command Authentication
- **A real-time UI** with Plotly graphs, toggle switches, and system logs

---

## Project Structure

```
├── README.md
├── attacks
│   ├── __pycache__
│   │   ├── dos_attack.cpython-313.pyc
│   │   ├── false_data_injection.cpython-313.pyc
│   │   └── replay_attack.cpython-313.pyc
│   ├── dos_attack.py
│   ├── false_data_injection.py
│   └── replay_attack.py
├── control_logic
│   ├── __pycache__
│   │   └── tc_controller.cpython-313.pyc
│   └── tc_controller.py
├── data
│   ├── temperature_control.log
│   └── temperature_control.log.example
├── defenses
│   ├── __pycache__
│   │   ├── command_authentication.cpython-313.pyc
│   │   └── log_and_audit.cpython-313.pyc
│   ├── anomaly_detection.py
│   ├── command_authentication.py
│   └── log_and_audit.py
├── main.py
├── process_sim
│   ├── __pycache__
│   │   └── temperature_control.cpython-313.pyc
│   └── temperature_control.py
├── requirements.txt
├── scada_ui
│   └── placeholder.txt
├── templates
│   └── index.html
├── tests
│   ├── test_false_data_injection.py
│   ├── test_tc_controller.py
│   └── test_temperature_control.py
└── ui
    ├── __init__.py
    └── visualization_server.py

14 directories, 27 files
```

---

##  Setup Instructions

### Prerequisites

- Python 3.6 or higher (we recommend Python 3.9+)
- `pip` package manager
- A modern web browser (Chrome or Firefox)
- Internet connection (for dashboard assets like Plotly and Tailwind)

### Installation Steps

1. **Clone the repo:**

   ```bash
   git clone https://github.com/MTumir/cs424-securesim.git
   cd cs424-securesim
   ```

2. **Install required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

---

## How to Run the Program

You can run the simulation in **command-line mode** or with the **web dashboard**.

### ▶️ Option 1: CLI Mode (Terminal Only)

```bash
python main.py [options]
```

#### Example:

```bash
python main.py --debug --injection --dos
```

This will run the simulation for 2000 cycles, showing logs and temperature data in the terminal.

#### Available Options:

- `--debug` – Enable debug-level logging
- `--injection` – Activate False Data Injection attack
- `--dos` – Activate Denial of Service attack
- `--replay` – Activate Replay attack
- `--logging` – Enable Logging & Auditing defense
- `--authentication` – Enable Command Authentication defense
- `--anomaly` – Enable Anomaly Detection defense (basic version)
- `--authentication1` – Simulate an **authorized** admin command
- `--authentication2` – Simulate an **unauthorized** intruder command

---

### Option 2: Web Dashboard (Recommended)

1. Start the simulation with UI enabled:

   ```bash
   python main.py --ui --debug --logging
   ```

2. Open your browser and visit:

   ```
   http://localhost:5001
   ```

3. Use the dashboard to:
   - Monitor temperature in real time
   - Toggle attacks and defenses
   - View system logs live
   - Check safe operating bounds
   - See all team members who contributed

---

## Stopping the Simulation

Use `Ctrl + C` in the terminal to shut down the simulation and the server. This will cause keyboard interrupt and close the application from the terminal.

---

## Notes

- Logs are stored in memory and shown in the UI log viewer.
- The default safe temperature range is **40°C to 50°C**.
- You can adjust which features are activated using command-line flags.
- The dashboard uses [Plotly.js](https://plotly.com/javascript/) and [Tailwind CSS](https://tailwindcss.com/) via CDN.
