##### create emails.csv file and enter emails in below format. Don't forget ","  
you can use any text editor) and save the file as emails.csv 

Example from emails.csv ( csv stands for comma separated values) 

first,last,dummyemail@dummy.com

#####configure .muttrc with your email ( i have example for gmail in this repo)


##### greeting.txt is your template . DON'T edit FIRSTNAME. You can replace everything. FIRSTNAME is replaced with the first value in emails.csv while sending out email. 

here is the code to send out email 
```
while read -r i;do email=$(echo $i | awk -F, '{print $NF}'); name=$(echo $i | awk -F, '{print $1}'); cp greeting.txt $email.txt ; sed -i '' "s/FIRSTNAME/$name/g" $email.txt;done < emails.csv

for i in $(cat emails.csv | awk -F, '{print $3}');do echo $i; mutt -s "Ananta Chakravartula" $i < $i.txt; done

```
