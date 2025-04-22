import logging
logger = logging.getLogger(__name__)

class LogAndAudit:
    def __init__(self, tc):
        self.active = False
        self.tc = tc
        self.handler = None

    def activate(self):
        # Create a new stream for the log file
        self.handler = logging.FileHandler('data/temperature_control.log', mode='w')
        # Assign handler the same format as defined in main.py
        self.handler.setFormatter(logging.getLogger().handlers[0].formatter)
        # Add handler to the logger
        logging.getLogger().addHandler(self.handler)

        logger.info('Logging defense activated')
        self.active = True

    def deactivate(self):
        self.active = False
