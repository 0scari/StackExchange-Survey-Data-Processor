import csv

class Procsessor:

    respondents = 0;

    @staticmethod
    def deleteNonProfessionals(fileName, newFileName):

        with \
            open(fileName,    'rb') as respondents, \
            open(newFileName, 'wb') as respondents_studentless:

            writer = csv.writer(respondents_studentless)
            reader = csv.reader(respondents)

            # returns the headers or `None` if the input is empty
            headers = next(reader, None)
            if headers:
                writer.writerow(headers)

            professionals_count = 0;
            for row in reader:

                if row[1] == "Professional developer":

                    writer.writerow(row)
                    professionals_count += 1

            print ("Professionals: " + str(professionals_count))
            Procsessor.respondents = professionals_count

    @staticmethod
    def makeNonNumericAttribsStrings():
        with \
            open('/Users/oscar/Desktop/test.csv', 'rb')  as respondents1, \
            open('/Users/oscar/Desktop/test1.csv', 'wb') as respondents2:

                writer = csv.writer(respondents2)
                reader = csv.reader(respondents1)

                for row in reader:

                    for colNr in range(len(row) -1):

                        if not row[colNr].isdigit():

                            row[colNr] = '"' + row[colNr] + '"'

                    writer.writerow(row)

    @staticmethod
    def getStats(colName, fileName):

        with open(fileName, 'rb') as respondents:

            reader      = csv.reader(respondents)
            variations  = {}
            colIndx     = Procsessor.findColumnIndx(colName, fileName)

            for row in reader:

                if row[colIndx] in variations:
                    variations[row[colIndx]] += 1

                else:
                    variations[row[colIndx]] = 1

        return variations

    @staticmethod
    def findColumnIndx(colName, fileName):

        with open(fileName, 'rb')  as respondents:

                reader     = csv.reader(respondents)
                colCounter = 0


                for row in reader:

                    for column in row:
                        if column == colName:
                            return colCounter

                        colCounter += 1

                    break # only title row

        raise Exception("No index found for" + colName)

    @staticmethod
    def deleteIfNotPresent(colName, fileName, newFileName):

        with \
            open(fileName,    'rb') as respondents, \
            open(newFileName, 'wb') as newCSV_file:

                reader         = csv.reader(respondents)
                writer         = csv.writer(newCSV_file)
                # Index of the column "colName"
                colNameIndx    = Procsessor.findColumnIndx(colName, fileName)
                delRowsCounter = 0 # number of rows that were deleted

                # returns the headers or `None` if the input is empty
                headers = next(reader, None)
                if headers:
                    writer.writerow(headers)

                for row in reader:
                    colCounter = 0

                    if row[colNameIndx] == "NA" :
                        delRowsCounter += 1
                        continue

                    writer.writerow(row)


        print("Respondents without "+colName+" removed:", delRowsCounter)
        Procsessor.respondents -= delRowsCounter



############### MAIN #

# Procsessor.deleteNonProfessionals("S_E_Survey.csv", "SE_professionals.csv")
#
# Procsessor.deleteIfNotPresent("Salary", \
#                               "SE_professionals.csv", \
#                               "SE_professionals_salaryPresent.csv")
#
# Procsessor.deleteIfNotPresent("JobSatisfaction", \
#                               "SE_professionals_salaryPresent.csv", \
#                               "SE_professionals_salaryPresent_JobSatisfactionPpresent.csv")
#
print("Respondents in CSV:", Procsessor.respondents)
stats = Procsessor.getStats("Salary", 'SE_professionals_salaryPresent_JobSatisfactionPpresent.csv')

for key, count in stats.items():
    print(key, count)
