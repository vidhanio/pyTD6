class pyTD6Exception(Exception):
    def __init__(self, message: str = None):
        if message is None:
            message = "pyTD6 had an error."
        super().__init__(message)


class BloonsTD6NotOpen(pyTD6Exception):
    def __init__(self):
        super().__init__("Bloons TD 6 is not open.")


class UpgradeError(pyTD6Exception):
    def __init__(self):
        super().__init__("Invalid upgrades.")


class CoordinateError(pyTD6Exception):
    def __init__(self):
        super().__init__("Invalid coordinates.")
