class InvalidItemOptionsException(Exception):
    """InvalidItemOptionsException is raised when someone attempts to add
    a product to the shopping cart or order but fails to define one or more of
    the following options:
        * the product itself
        * the quantity
        * the shipping address for the product
    """
    pass

class NoAddressSpecifiedException(Exception):
    """NoAddressSpecifiedException is raised when an address is needed and
    either one is not passed or the address that was passed was incorrect in
    some manner.
    """
    pass
