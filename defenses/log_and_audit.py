import logging

class LogAndAudit:
    def __init__(self, tc):
        self.active = False
        self.tc = tc
        self.log = logging.getLogger(__name__)
        self.handler = None

    def activate(self):
        self.handler = logging.FileHandler('temperature_control.log', mode='w')
        self.handler.setFormatter(logging.getLogger().handlers[0].formatter)
        logging.getLogger().addHandler(self.handler)

        self.log.info('Logging defense activated')
        self.active = True

    def deactivate(self):
        self.active = False
