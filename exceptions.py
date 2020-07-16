class pyTD6Exception(Exception):
    def __init__(self, message: str = None):
        if message is None:
            message = "pyTD6 had an error."
        super().__init__(message)


class BloonsTD6NotOpen(pyTD6Exception):
    def __init__(self):
        super().__init__("Bloons TD 6 is not open.")


class MonkeyPlaced(pyTD6Exception):
    def __init__(self):
        super().__init__("The monkey has already been placed.")


class MonkeyNotPlaced(pyTD6Exception):
    def __init__(self):
        super().__init__("The monkey has not been placed.")


class CoordinateError(pyTD6Exception):
    def __init__(self):
        super().__init__("Invalid coordinates.")


class UpgradeError(pyTD6Exception):
    def __init__(self):
        super().__init__("Invalid upgrades.")


class TargetingError(pyTD6Exception):
    def __init__(self):
        super().__init__("Invalid targeting.")


class MonkeySold(pyTD6Exception):
    def __init__(self):
        super().__init__("The monkey has been sold.")
