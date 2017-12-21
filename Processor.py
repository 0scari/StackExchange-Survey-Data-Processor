# coding=utf-8
import csv

class Processor:

    # Filtered respondents
    respondents = 0

    # $$$
    # The rows in the band 0 - 2500 will be removed ONLY due to high risk of noisy data
    SALARY_BANDS = [0, 2500, 15000, 20000, 25000, 30000, 40000, 50000, 70000, 100000, 150000, float('inf')]

    CURRENCY_ABBREV = {
        'South African rands (R)'       : "ZAR",
        'Brazilian reais (R$)'          : "BRL",
        'U.S. dollars ($)'              : "USD",
        'Singapore dollars (S$)'        : "SGD",
        'Japanese yen (Œ«)'             : "JPY",
        'Euros (ä‰å)'                   : "EUR",
        'Swedish kroner (SEK)'          : "SEK",
        'Russian rubles (?)'            : "RUB",
        'Chinese yuan renminbi (Œ«)'    : "CNY",
        'Swiss francs'                  : "CHF",
        'British pounds sterling (Œ£)'  : "GBP",
        'Polish zloty (zl)'             : "PLN",
        'Indian rupees (?)'             : "INR",
        'Australian dollars (A$)'       : "AUD",
        'Mexican pesos (MXN$)'          : "MXN",
        'Canadian dollars (C$)'         : "CAD",
    }

    EXCHANGE_RATE = { # to USD on 19/12/2017 at http://www.xe.com/currencyconverter
        "ZAR": 0.0786562,
        "BRL": 0.303950,
        "SGD": 0.742433,
        "JPY": 0.00886015,
        "EUR": 1.18432,
        "SEK": 0.119028,
        "RUB": 0.0170147,
        "CNY": 0.0170147,
        "CHF": 1.01548,
        "GBP": 1.33867,
        "PLN": 0.281868,
        "INR": 0.0156102,
        "AUD": 0.766473,
        "MXN": 0.0520393,
        "CAD": 0.776566
    }

    @staticmethod
    def deleteNonProfessionals(fileName, newFileName):

        with \
            open(fileName,    'rU') as respondents, \
            open(newFileName, 'w') as respondents_studentless:

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
            Processor.respondents = professionals_count

    @staticmethod
    def makeNonNumericAttribsStrings():
        with \
            open('/Users/oscar/Desktop/test.csv',  'rU')  as respondents1, \
            open('/Users/oscar/Desktop/test1.csv', 'w') as respondents2:

            writer = csv.writer(respondents2)
            reader = csv.reader(respondents1)

            for row in reader:

                for colNr in range(len(row) -1):

                    if not row[colNr].isdigit():

                        row[colNr] = '"' + row[colNr] + '"'

                writer.writerow(row)

    @staticmethod
    def getStatsOfAttribute(colName, fileName):

        with open(fileName, 'rU') as respondents:

            reader      = csv.reader(respondents)
            variations  = {}
            colIndx     = Processor.findColumnIndx(colName, fileName)

            next(reader, None) #Skip header row

            for row in reader:

                if row[colIndx] in variations:
                    variations[row[colIndx]] += 1

                else:
                    variations[row[colIndx]] = 1

        return variations

    @staticmethod
    def findColumnIndx(colName, fileName):

        with open(fileName, 'rU')  as respondents:

            reader     = csv.reader(respondents)
            colCounter = 0

            roww = 5
            for row in reader:
                roww = row
                for column in row:
                    if column == colName:
                        return colCounter

                    colCounter += 1

                break # only title row

            raise Exception("No index found for " + colName, roww)

    @staticmethod
    def deleteIfPresent(criteria, colName, fileName, newFileName):
        """Delete a record who matches the criteria in the given column"""

        with \
            open(fileName,    'rU') as respondents, \
            open(newFileName, 'w') as newCSV_file:

            reader         = csv.reader(respondents)
            writer         = csv.writer(newCSV_file)
            # Index of the column "colName"
            colNameIndx    = Processor.findColumnIndx(colName, fileName)
            delRowsCounter = 0 # number of rows that were deleted

            # returns the headers or `None` if the input is empty
            headers = next(reader, None)
            if headers:
                writer.writerow(headers)

            for row in reader:
                colCounter = 0

                if row[colNameIndx] in criteria :
                    delRowsCounter += 1
                    continue

                writer.writerow(row)


        print("Respondents with "+colName+": "+", ".join(criteria)+" removed: " + str( delRowsCounter))
        Processor.respondents -= delRowsCounter

    @staticmethod
    def createSalaryBands(fileName, newFileName):

        with \
            open(fileName,    'rU') as respondents, \
            open(newFileName, 'w') as newCSV_file:

            reader = csv.reader(respondents)
            writer = csv.writer(newCSV_file)
            salaryColIndx   = Processor.findColumnIndx("Salary", fileName)
            currencyColIndx = Processor.findColumnIndx("Currency", fileName)

            # returns the headers or `None` if the input is empty
            headers = next(reader, None)
            headers.append("SalaryBand")
            if headers:
                writer.writerow(headers)

            for row in reader:

                USD_salary = Processor.calcUSD_salary(row[currencyColIndx], row[salaryColIndx])
                salaryBand = Processor.calcSalaryBand(USD_salary)

                row.append(salaryBand)
                writer.writerow(row)

        print ("Salary bands created, index in header: "
                + str(Processor.findColumnIndx("SalaryBand", newFileName)))

    @staticmethod
    def calcUSD_salary(currency, salary):

        currency = Processor.CURRENCY_ABBREV[currency]

        if currency == "USD":
            return float(salary)

        else:
            return Processor.EXCHANGE_RATE[currency] * float(salary)

    @staticmethod
    def calcSalaryBand (figure):

        for i in range(len(Processor.SALARY_BANDS) -1):

            if Processor.SALARY_BANDS[i] <= figure <= Processor.SALARY_BANDS[i+1]:
                return Processor.SALARY_BANDS[i]


        raise Exception("Failed to determine the salary band for ", figure)


############### MAIN #

Processor.deleteNonProfessionals("S_E_Survey_Raw.csv", "SE_professionals.csv")

Processor.deleteIfPresent(["NA"],
                           "Salary",
                           "SE_professionals.csv",
                           "SE_professionals_salaryPresent.csv")

Processor.deleteIfPresent(["NA", "Bitcoin (btc)"],
                           "Currency",
                           "SE_professionals_salaryPresent.csv",
                           "SE_professionals_salaryPresent_currencyPresent.csv")


Processor.deleteIfPresent(["NA"],
                           "JobSatisfaction",
                           "SE_professionals_salaryPresent_currencyPresent.csv",
                           "SE_professionals_salaryPresent_currencyPresent_SatisfactionPresent1.csv")

Processor.deleteIfPresent(["NA"],
                           "CareerSatisfaction",
                           "SE_professionals_salaryPresent_currencyPresent_SatisfactionPresent1.csv",
                           "SE_professionals_salaryPresent_currencyPresent_SatisfactionPresent2.csv")



Processor.createSalaryBands("SE_professionals_salaryPresent_currencyPresent_SatisfactionPresent2.csv",
                             "SE_professionals_salaryPresent_currencyPresent_SatisfactionPresent_salaryBands.csv")

Processor.deleteIfPresent(["0"],
                           "SalaryBand",
                           "SE_professionals_salaryPresent_currencyPresent_SatisfactionPresent_salaryBands.csv",
                           "SE_professionals_salaryPresent_currencyPresent_SatisfactionPresent_salaryBands1.csv")


countryStats = Processor.getStatsOfAttribute("Country", 'SE_professionals_salaryPresent_currencyPresent_SatisfactionPresent_salaryBands1.csv')
nonUK_Countries = [];
for country in countryStats.keys():
    if country != "United Kingdom":
        nonUK_Countries.append(country)



# will leave only UK respondents
Processor.deleteIfPresent(nonUK_Countries,
                           "Country",
                           "SE_professionals_salaryPresent_currencyPresent_SatisfactionPresent_salaryBands1.csv",
                           "SE_Survey_PyCleaned.csv")

print("Respondents in CSV:", Processor.respondents)

stats = Processor.getStatsOfAttribute("Country", 'SE_Survey_PyCleaned.csv')

res = ""
for key, count in stats.items():
    res += key + " :  " + str(count) + "\n"

print(res)
