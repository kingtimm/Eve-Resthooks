class DomainConflictException(Exception):
    """Eve Rest Hooks tried to patch your Eve app's domain, but found a subscriptions and/or _jobs endpoint already
    existed.
    """
    pass