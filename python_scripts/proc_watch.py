import pdb
import subprocess
import time
import smtplib
from email.mime.text import MIMEText


WHITE_LIST= ['sshd','rsync','sftp-server','ssh','root']
WHITE_LIST_STR='|'.join(WHITE_LIST)
#print WHITE_LIST_STR


def proc_watch():
	while True:
		top_cmd="top -b -n 1 | sed -n '8,17p'| egrep -v \" "+ WHITE_LIST_STR + "\" |  awk '{print $1}' "
		top_pids=subprocess.Popen(top_cmd,stdout=subprocess.PIPE,shell=True).communicate()[0].strip().split()
		time.sleep(15)
		count=0
		for pid in top_pids:
			pid_info=["top -b -n 1 -p "+pid+"| sed -n '8,17p'"]
	         	rogue_info=subprocess.Popen(pid_info,stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
                	if rogue_info.poll() is None:
				cpu_pid = rogue_info.communicate()[0].split()
				try:
					if float(cpu_pid[8]) > 90:
						print "found pid > 90"
						s=smtplib.SMTP('localhost')
						s.set_debuglevel(1)
	       					body=time.strftime("%d/%m/%Y-%H:%M:%S")
       						body+="\n"+cpu_pid 
						msg = MIMEText(body)
						sender = 'engaging-admin@techsquare.com'
						recipients = ['ananta.c@gmail.com']
						msg['Subject'] = "rogue pid" + cpu_pid[0]
						msg['From'] = sender
						msg['To'] = ", ".join(recipients)
						s.sendmail(sender, recipients, msg.as_string())
						s.quit()
						print 'not printing this line'
				except:
					pass

def main():
                proc_watch()


if __name__ == '__main__':
        main()

