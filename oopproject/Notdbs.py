from Application import Application


class Notdbs(Application):

    def __init__(self, salarycreditacc, creditlimit, acctype, overdrafttype, file1, file2, document):

        Application.__init__(self, salarycreditacc, creditlimit, acctype, overdrafttype, file1, file2)
        self.__document = document
        if salarycreditacc.isdigit:
            if len(salarycreditacc) == 10:
                self.__salarycreditacc = salarycreditacc

    def get_document(self):
        return self.__document

    def set_document(self, document):
        self.__document = document

