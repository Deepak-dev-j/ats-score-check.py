import sys
import PyPDF2
import re
import mysql.connector as mysql
from datetime import datetime
current_date_time = datetime.now()
current_day = current_date_time.day
current_month = current_date_time.month
current_year = current_date_time.year
coe=True
apply_after=0
try:
    Ats_score = 0
    last_applied_date=[]
    result_list = []   
    # Connecting  to the MySQL server
    mydb = mysql.connect(
        host="localhost",
        user="root",
        password="12345",
        database="science_day" 
    )
    mycursor = mydb.cursor()
    # Executing a SELECT querys.
    role_query = "SELECT role FROM science_day.keyword_role"
    mycursor.execute(role_query) 
    role_results=mycursor.fetchall()
    print("The Available Roles Are")
    for item in range (len(role_results)):
        print(f"Role ID => {item} : {role_results[item][0]}")
    applied_role=int(input("Enter Role Id To Apply :"))
    role=str(role_results[applied_role][0])
    query = "SELECT Keyword1, Keyword2, Keyword3, Keyword4, Keyword5 FROM science_day.keyword_role WHERE Role='{}'".format(role)
    mycursor.execute(query)  
    # Fetch rows
    result = mycursor.fetchall()
    tuple_values = result[0]
    # Creating a list to store the split values
    result_list = []
    # Splitting each value in the tuple and adding to the result list
    for value in tuple_values:
        result_list.extend(value.split())
    vueb = []
    extracted = ""
    pdfFileObj = open('check.pdf', 'rb')
    indian_mobile_pattern = re.compile(r'(\+91|0)?[\s-]?[789]\d{9}')
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    # Get the number of pages in the PDF
    num_pages = len(pdfReader.pages)
    # Extract text from all pages
    for i in range(num_pages):
        pageObj = pdfReader.pages[i]
        extracted_text = pageObj.extract_text().lower()
        extracted_text = extracted_text.replace("/", "").replace("\xa0", "").replace("\n", " ")#Repalcing the unwanted values
        extracted += extracted_text
        vueb.extend(extracted.split())  # Adding In List
        mobile_numbers = indian_mobile_pattern.findall(extracted)
        email_addresses = email_pattern.findall(extracted)
        email = ', '.join(email_addresses)
        #Converting the Mail and Mobile Number To Str Format To Update in Database
        mb_num = ', '.join(mobile_numbers)
    if (mobile_numbers and email_addresses == []):
        sys.exit("No mobile numbers or email addresses found in the PDF.")
        #Exiting Here Because Useless To Execute An Ats Without Knowing The Contact Information Of An Person
    for b in result_list:
        if b in vueb:
            Ats_score += 1
            result_list.remove(b)
    if (email_addresses == []):
        email = "xyz"
        cid = mb_num
    elif (mobile_numbers == []):
        cid = email
        mb_num = 12456
    else:
        cid=email
    def reject_reterive(cid):
        rejected_query= "SELECT current_year,current_month,current_day FROM science_day.rejected_canditae WHERE cid='{}'".format(cid)
        mycursor.execute(rejected_query)
        rejected_result = mycursor.fetchall()
        if(rejected_result != []):
            coe=False
        for bb in rejected_result:
            last_applied_date.extend(bb)
        extracted_date=last_applied_date[0]
        extracted_month=last_applied_date[1]
        extracted_year=last_applied_date[2]     
#given_date = datetime(2022, 5, 17)
        given_date = datetime(extracted_year,extracted_month,extracted_date)
        date_difference=current_date_time-given_date
        total_days = date_difference.days
        apply_after+=total_days
        if total_days>=100:
            coe= True
    if(coe):
        if Ats_score >= 4:
            insert_query1 = "INSERT INTO slected_canditate (email,mobile_number,cid) VALUES (%s, %s, %s)"
            # Execute the update query with values
            mycursor.execute(insert_query1, (email, mb_num, cid))
            # Commit the changes
            mydb.commit()
        else:
            insert_query2 = "INSERT INTO rejected_canditate (email,mobile_number,cid,current_day,current_month,current_year) VALUES (%s, %s, %s,%s,%s,%s)"
            mycursor.execute(insert_query2, (email, mb_num, cid, current_day, current_month, current_year))
            mydb.commit()
    else:
        print(f"currently you are not eligible to apply for this role you can apply after:{apply_after} Days")
except ValueError:
    print("Input is not an integer. Please enter a valid role ID.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    try:
        pdfFileObj.close()
    except NameError:
        pass  # pdfFileObj may not be defined if an exception occurred before it was assigned
    try:
        mycursor.close()
        mydb.close()
    except NameError:
        pass  # mycursor or mydb may not be defined if an exception occurred before they were assigned