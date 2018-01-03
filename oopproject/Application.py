import datetime


class Application:

    def __init__(self, salarycreditacc, creditlimit, acctype, overdrafttype, file1, file2):
        self.__salarycreditacc = salarycreditacc
        currentdatetime = datetime.datetime.now()
        created_date = str(currentdatetime.day) + "/" + str(currentdatetime.month) + "/" + str(currentdatetime.year)  # DD-MM-YYYY format
        self.__created_date = created_date
        self.__creditlimit = creditlimit
        self.__acctype = acctype
        self.__overdrafttype = overdrafttype
        self.__file1 = file1
        self.__file2 = file2

    def get_salarycreditacc(self):
        return self.__salarycreditacc

    def get_created_date(self):
        return self.__created_date

    def get_creditlimit(self):
        return self.__creditlimit

    def get_acctype(self):
        return self.__acctype

    def get_overdrafttype(self):
        return self.__overdrafttype

    def get_file1(self):
        return self.__file1

    def get_file2(self):
        return self.__file2

    def set_salarycreditacc(self, salarycreditacc):
        self.__salarycreditacc = salarycreditacc

    def set_created_date(self, created_date):
        self.__created_date = created_date

    def set_creditlimit(self, creditlimit):
        self.__creditlimit = creditlimit

    def set_acctype(self, acctype):
        self.__acctype = acctype

    def set_overdrafttype(self, overdrafttype):
        self.__overdrafttype = overdrafttype

    def set_file1(self, file1):
        self.__file1 = file1

    def set_file2(self, file2):
        self.__file2 = file2

