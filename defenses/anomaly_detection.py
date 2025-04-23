import logging

logger = logging.getLogger(__name__)

class AnomalyDetection:
    def __init__(self, tc):
        self.active = False
        self.tc = tc
        self.init_low_bound = self.tc.low_bound

    def defend(self):
        if not self.active:
            return
        
        ## Check for change to low bound from injection attack
        current_low_bound = self.tc.low_bound
        if current_low_bound != self.init_low_bound:
            logger.debug(f"Lower bound changed from {self.init_low_bound} to {current_low_bound}")
            logger.info(f"Reverting lower bound to: {self.init_low_bound}")
            self.tc.low_bound = self.init_low_bound

    def activate(self):
        self.active = True
        logger.info("Anomaly detection activated")

    def deactivate(self):
        self.active = False