import smtplib 
try: 
    #Create your SMTP session 
    smtp = smtplib.SMTP('smtp.gmail.com', 587) 

   #Use TLS to add security 
    smtp.starttls() 

    #User Authentication 
    smtp.login("rithish2k18@gmail.com","rithish00$")

    #Defining The Message 
    message = "Message_you_need_to_send" 

    #Sending the Email
    smtp.sendmail("rithish2k18@gmail.com", "rithishkumar01092000@gmail.com",message) 

    #Terminating the session 
    smtp.quit() 
    print ("Email sent successfully!") 

except Exception as ex: 
    print("Something went wrong....",ex)
