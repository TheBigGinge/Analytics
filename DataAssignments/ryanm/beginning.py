from pyzipcode import ZipCodeDatabase
import csv



zcdb = ZipCodeDatabase()

years_exp = {"< 1 year": .5, ">1 but <= 3 years": 2, ">3 but <= 8 years": 5, ">8 but <= 13 years": 10.5,
             ">13 but <=20 years": 16.5, ">20 years": 20.5}

num_employee = {"> 25000": 25100, ">250 but <= 1500": 875, ">1500 but <= 2500": 2000, ">2500 but <= 15000": 8750,
                ">15000 but <= 25000": 20000, ">150 but <= 250": 200, ">25 but <= 150": 87.5}

'''
def find_zip(zip_item, state):
    try:
        for item in zip_item:
            if str(item.state).lower() == str(state).lower():
                return item.zip
    except:
        return None


record_counter = 0
with open("C:\\users\\ryanm\\desktop\\eq_testing.tsv", 'wb') as W:
    writer = csv.writer(W, delimiter='\t', lineterminator='\n')

    write_header = ["RecordID", "Holder", "NAICS", "Holder", "City", "State", "ZipCode", "Title", "Holder", "Holder",
                    "Holder", "Holder", "Holder", "GrossIncome", "Holder", "Holder", "Holder", "Holder", "Holder",
                    "Holder", "Holder", "YearsExperience"]

    writer.writerow(write_header)

    with open("c:\\users\\ryanm\\desktop\\eq.tsv", 'rb') as R:
        reader = csv.reader(R, delimiter='\t')

        header = reader.next()

        for row in reader:
            if record_counter % 1000 == 0 and record_counter != 0:
                print "%s records written " % record_counter

            city = row[header.index("CITY")]
            state = row[header.index("STATE")]
            job = row[header.index("CLEAN_JOBTITLE")]
            pay = row[header.index("TOTAL_PAY")]
            exp_range = row[header.index("AVG_YEARS_EXPERIENCE")]
            experience = years_exp[exp_range]
            comp_range = row[header.index("COMPANY_SIZE")]
            comp_size = num_employee[comp_range]
            zip_finder = zcdb.find_zip(city=city)
            zip_code = find_zip(zip_finder, state)

            final_row = record_counter, 1, "Financial Services", 1, 1, city, state, zip_code, job, 1, 1, 1, 1, 1, pay,\
                1, 1, 1, 1, 1, 1, 1, experience
            writer.writerow(final_row)

            record_counter += 1
'''
jobs = {"Bank Teller": "Bank Teller", "Personal Banker": "Personal Banker", "Senior Teller": "Senior Teller",
        "Business Systems Consultant": "Business Systems Consultant",
        "Customer Service Representative (CSR)": "Customer Service Representative (CSR)",
        "Member Service Representative": "Member Service Representative", "Fraud Analyst": "Fraud Analyst",
        "ADMINISTRATIVE ASSISTANT III": "Administrative Assistant", "FINANCIAL ADVISOR": "Financial Advisor",
        "FRAUD ANALYST I": "Fraud Analyst", "FRAUD ANALYST II": "Fraud Analyst",
        "CUSTOMER SERVICE REPRESENTATIVE": "Customer Service Representative (CSR)",
        "CUSTOMER SERVICE REPRESENTATIVE II": "Customer Service Representative (CSR)",
        "CUSTOMER SERVICE REPRESENTATIVE III": "Customer Service Representative (CSR)",
        "OPERATIONS ANALYST": "Operations Analyst", "WEB DEVELOPER": "Web Developer",
        "ADMINISTRATIVE ASSISTANT II": "Administrative Assistant",
        "ADMINISTRATIVE ASSISTANT IV": "Administrative Assistant", "AUDITOR": "Auditor",
        "AUDITOR II": "Auditor", "CREDIT ANALYST I": "Credit Analyst", "CREDIT ANALYST II": "Credit Analyst",
        "CREDIT ANALYST III": "Credit Analyst", "DATABASE ANALYST": "Database Analyst",
        "HUMAN RESOURCES MANAGER": "Human Resources (HR) Manager"}

counting = 0
with open("C:\\users\\ryanm\\desktop\\NewRandomSample.tsv", 'wb') as W:
    writer = csv.writer(W, delimiter='\t', lineterminator='\n')

    with open("C:\\users\\ryanm\\desktop\\Main\\Analyses\\2014\\Rob Stuff\\Equifax\\eq_testing.tsv", 'rb') as R:
        reader = csv.reader(R, delimiter='\t')

        header = reader.next()

        writer.writerow(header)

        for row in reader:
            counting += 1
            if counting % 1000 == 0:
                print "%s rows written..." % counting
            job = row[header.index('Title')]
            try:
                final_job = jobs[job]
                row_capture = row
                row_capture[header.index('Title')] = final_job
                zip = row[header.index("ZipCode")]
                income = row[header.index("GrossIncome")]

                if zip != "":
                    if income != "":
                        if float(income) >= 20000:
                            writer.writerow(row_capture)
            except KeyError:
                continue
