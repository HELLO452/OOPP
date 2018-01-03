from Application import Application


class Dbs(Application):
    def __init__(self, salarycreditacc, creditlimit, acctype, overdrafttype, file1, file2):

        Application.__init__(self, salarycreditacc, creditlimit, acctype, overdrafttype, file1, file2)
        if salarycreditacc.isdigit:
            if len(salarycreditacc) == 9:
                self.__salarycreditacc = salarycreditacc



