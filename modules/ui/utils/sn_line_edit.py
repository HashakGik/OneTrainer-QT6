
import PySide6.QtWidgets as QtW
import PySide6.QtGui as QtG

# Scientific Notation Line Edit Widget.
class SNLineEdit(QtW.QLineEdit):
    def __init__(self, contents=None, parent=None, min=None, max=None):
        super().__init__(contents, parent)

        #self.setValidator(QtG.QDoubleValidator(parent)) # TODO: Validator does not work for locales which do not use the decimal point .
        self.setValidator(QtG.QRegularExpressionValidator("[+-]?\d\.?\d*([eE][+-]?\d+)?", parent)) # A regular expression seems more reliable.
        #self._min = min
        #self._max = max

        #self.editingFinished.connect(lambda: self.setText(self.__fixRange(self.text())))

    #def setMin(self, val):
    #    self._min = val
    #    if self._max is not None and self._max < self._min:
    #        self._max = self._min

    #def setMax(self, val):
    #    self._max = val
    #    if self._min is not None and self._min > self._max:
    #        self._min = self._max

    #def min(self):
    #    return self._min

    #def max(self):
    #    return self._max


    #def __fixRange(self, input):
    #    try:
    #        val = float(input.replace(",", ".")) # TODO: BUG: with non En-US locales, the decimal separator (,) is not recognized by float() and the base validator does not convert it to standard dot.
            #if self._min is not None:
            #    val = max(self._min, val)
            #if self._max is not None:
            #    val = min(self._max, val)

     #       if "e" in input.lower():  # Scientific notation.
    #            return "{:e}".format(val)
     #       else:
     #           return str(val)
     #   except:
    #        return input
