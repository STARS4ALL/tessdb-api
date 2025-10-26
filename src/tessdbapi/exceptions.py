class DuplicatedNameError(RuntimeError):
    '''Photometer name has more than one registry entry'''
    def __str__(self):
        s = self.__doc__
        if self.args:
            s = "{0}: '{1}' N={2!s}".format(s, self.args[0], self.args[1])
        s = '{0}.'.format(s)
        return s

class MissingNameError(RuntimeError):
    '''Photometer name not found'''
    def __str__(self):
        s = self.__doc__
        if self.args:
            s = "{0}: '{1!s}'".format(s, self.args[0])
        s = '{0}.'.format(s)
        return s