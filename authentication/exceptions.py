

class UserCreationError(Exception):
    pass

class SuperuserCreationError(Exception):
    pass

class UsernameMissingError(Exception):
    pass

class EmailMissingError(Exception):
    pass

class StaffMissingError(Exception):
    pass

class SuperuserMissingError(Exception):
    pass

class InvalidSuperuserError(Exception):
    pass

class TokenGenerationError(Exception):
    pass
