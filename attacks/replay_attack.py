import logging
import time

logger = logging.getLogger(__name__)

class ReplayAttack:
    def __init__(self, tc):
        self.active = False
        self.tc = tc

    def attack(self):
        if not self.active:
            return

        #initial setup variables
        data = 'Initiating cooling cycle'
        delay = 2

        #simulates 20 captured messages
        for i in range(20):
            #creates a new message for each iteration
            timestamp = str(time.time())
            msg = f'{timestamp}:{data}'

            #Initial message
            logger.debug(f'\tOriginal System Message: {msg}')
            print(f'{msg}')
            time.sleep(delay)

            #Attacker captures and resends the message
            logger.debug(f'\tAttacker captures message: {msg}')
            time.sleep(delay)
            logger.debug(f'\tAttacker resends message: {msg}')
            print(f'{msg}')


    def activate(self):
        self.active = True
        logger.info(f'\tReplay Attack activated')