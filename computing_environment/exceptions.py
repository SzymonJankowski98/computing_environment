from .constants import LANGUAGES

# Invitations
class AlreadyInvited(Exception):
    """User has a valid, pending invitation"""
    pass


class AlreadyAccepted(Exception):
    """User has already accepted an invitation"""
    pass


class UserRegisteredEmail(Exception):
    """This email is already registered by a site user """
    pass

#Job
class WrongLanguage(Exception):
    """language take only one of the following values: {}""".format(', '.join(map(lambda l: l[-1], LANGUAGES)))
    pass