import subprocess
import time
import smtplib
from email.mime.text import MIMEText


WHITELIST='sshd|sftp-server|scp|defunct>'

HEADER=['UID' ,  'CPU' , 'MEM' , 'BSDTIME' , 'USER' , 'PID' , 'COMM']
NEWLINE="\n"
SPACE=" "
COLON=": "
# removed cmd as it is having problem parsing list when there are spaces in cmd; replaced with comm
PS_FORMAT="uid,%cpu,%mem,bsdtime,user,pid,comm"
COLUMNS="$(echo "+PS_FORMAT +"| awk -F, '{print NF}')"
USERS=[]


def proc_watch():

        while True:
		global WHITELIST		
                cmd="ps axo " + PS_FORMAT+" |awk '$1 > 1000 {print}' |awk '$2 > 5 || $3 > 5 {print}' | egrep -v '( " +WHITELIST + ")$'"
                pids=subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True).communicate()[0].strip().split()

                # range([start], stop[, step]), to get uids from the pids list 
                for uid in range(0,len(pids),7):
                        global USERS
                        USERS=[pids[uid]]
		# converting list to set to get unique values and converting back to list 
		for USER in list(set(USERS)):
			try:
				user_cmd="ps o "+PS_FORMAT +" -u " + USER +" | awk '$2 > 5 || $3 > 5 {print}' |  egrep -v '( " +WHITELIST + ")$'"
				user_pids=subprocess.Popen(user_cmd,stdout=subprocess.PIPE,shell=True)	
			# check the process state 
				hostname_cmd = subprocess.Popen(['hostname','-s'], stdout=subprocess.PIPE)
				hostname=hostname_cmd.communicate()[0]
				user_pids_list=user_pids.communicate()[0].split()
				BODY=''
				BODY+=time.strftime("%d/%m/%Y-%H:%M:%S")+NEWLINE +hostname+NEWLINE
                                BODY+=','.join(HEADER) + NEWLINE
				for item in range(0,len(user_pids_list),7):
					BODY+=', '.join(user_pids_list[0:7]) + NEWLINE

				fromaddr= "ac@techsquare.com"
        			toaddr= "ac@techsquare.com"
				user_email_cmd = "ldapsearch -LLL -x -H ldap://eofe-ldap -b dc=cm,dc=cluster cn=" +user_pids_list[4] +"| grep mail | awk '{print $2}'"
				user_email=subprocess.Popen(user_email_cmd,stdout=subprocess.PIPE,shell=True).communicate()[0]
	                	subject = "resource intensive process on "+ hostname.rstrip()
				msg="Content-Type: text/plain; \n" 
				msg=msg+'Subject: %s \n' % subject
				msg=msg+'From: %s \n' % fromaddr
				msg=msg+'To: %s \n\n' % toaddr
				if user_pids.poll() is None:
					BODY+=time.strftime("%d/%m/%Y-%H:%M:%S")+NEWLINE +hostname+NEWLINE
					BODY+=','.join(HEADER) + NEWLINE
					hostname_cmd = subprocess.Popen(['hostname','-s'], stdout=subprocess.PIPE)
					hostname=hostname_cmd.communicate()[0]
					BODY+=time.strftime("%d/%m/%Y-%H:%M:%S")+NEWLINE +hostname+NEWLINE
					BODY+=','.join(HEADER) + NEWLINE
					user_pids_list=user_pids.communicate()[0].split()
					for item in range(0,len(user_pids_list),7):
						BODY+=', '.join(user_pids_list[0:7]) + NEWLINE
				msg+=user_email
				msg+=BODY
				server = smtplib.SMTP('localhost')
#				server.set_debuglevel(1)
				server.sendmail(fromaddr, toaddr, msg)
				server.quit()
				time.sleep(900)			
			except: 
				pass
			

def main():
                proc_watch()


if __name__ == '__main__':
        main()


