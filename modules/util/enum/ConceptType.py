from modules.util.enum.BaseEnum import BaseEnum


class ConceptType(BaseEnum):
    STANDARD = 'STANDARD'
    VALIDATION = 'VALIDATION'
    PRIOR_PREDICTION = 'PRIOR_PREDICTION'

    @staticmethod
    def is_enabled(value, context=None):
        if context == "prior_pred_enabled":
            return True
        else: # prior_pred_disabled
            return value in [ConceptType.STANDARD, ConceptType.VALIDATION]

