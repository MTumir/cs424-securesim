class CommandAuthentication:
    def __init__(self, tc):
        self.active = False
        self.tc = tc
        self.authorized_users = set()  # set of user IDs or names for future extensions

    def activate(self):
        # Add a default authorized user or load from config
        self.authorized_users.add('admin')
        self.active = True

    def deactivate(self):
        self.active = False

    def authenticate_command(self, user):
        if not self.active:
            return True  # If defense is not active, allow all
        return user in self.authorized_users