class OutOfSampleError(Exception):
    """
    Raised when a new input contains feature values
    outside the historical min/max range.
    """
    def __init__(self, feature_name, value, minimum, maximum):
        message = (
            f"{feature_name} with value {value} is outside "
            f"historical range [{minimum}, {maximum}]"
        )
        super().__init__(message)
