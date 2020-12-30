import imaplib
import email

mail = imaplib.IMAP4_SSL('imap.gmail.com')  # impap object to establish our connection
mail.login('test782057@gmail.com', 'test@12344321')
mail.list()
# Out: list of "folders" aka labels in gmail.
mail.select("inbox")  # connect to inbox.

result, data = mail.search(None, 'ALL')

ids = data[0]  # data is a list.
id_list = ids.split()  # ids is a space separated string
latest_email_id = id_list[-1]  # get the latest

result, data = mail.fetch(latest_email_id, "(RFC822)")  # fetch the email body (RFC822)             for the given ID

raw_email = data[0][1].decode('utf-8')  # here's the body, which is raw text of the whole email
decoder_targetmail = email.message_from_string(raw_email)
from_sender = decoder_targetmail["from"]
from_list = []  # create an empty list to split from_sender as it can contain name and email id and we only need email
from_list = from_sender.split()  # split the contents of email
from_list_size = len(from_list)  # find length so that we can get the index of our email
email_id_to_search = from_list[from_list_size - 1]  # use this variable to search emails
print("searching and analyzing all the emails from : {}".format(email_id_to_search))
target_items = []
target_items = decoder_targetmail["ARC-Authentication-Results"].split()
smtp_current = target_items[3]  # will compare this field with previously recieved emails from sender
print(smtp_current)


def get_emails(result_bytes):  # for extracting all the emails from the intedend target
    msgs = []  # all the email data are pushed inside an list
    for num in result_bytes[0].split():
        typ, data1 = mail.fetch(num, '(RFC822)')
        msgs.append(data1)

    return msgs


def search(key, value, mail):
    result1, data1 = mail.search(None, key, '"{}"'.format(value))
    return data1


msgs = get_emails(search('FROM', email_id_to_search, mail))  # this is a list which will contain all the previous mails
total_number_emailRecived = len(msgs) - 1  # -1 because current email will not be counted for our algo
print(total_number_emailRecived)


def get_smtp(var):  # will return the smtp of previous email recived from the target
    temp_mail1 = msgs[var]
    temp_mail2 = temp_mail1[0][1].decode('utf-8')  # our string variable which contains mail info
    temp1 = email.message_from_string(temp_mail2)
    target_items_old = []
    target_items_old = temp1["ARC-Authentication-Results"].split()
    return target_items_old[3]


def check_hits():  # to give total number of matches

    count = 0
    for j in range(0, total_number_emailRecived):
        if smtp_current == get_smtp(j):
            count += 1
    return count


def one_email():  # when the email is recived for the first time
    if target_items[2] == "dkim=pass" and target_items[6] == "spf=pass" and target_items[17] == "dmarc=pass":
        print("Chances of email being spoofed is very less")
        return True
    else:
        print("high proability that this email is being spoofed")
        return False


# result portion of the program begins from here
if total_number_emailRecived <= 4:
    one_email()
else :
    if check_hits() >= (total_number_emailRecived-1) / 2 and one_email():
        print("chances of email being spoofed is quite low ")
    else:
        print("high chances that this email is spoofed ")



