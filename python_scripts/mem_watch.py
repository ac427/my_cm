import subprocess
import time
import smtplib


WHITE_LIST= ['sshd','sftp-server','ssh','root']
WHITE_LIST_STR='|'.join(WHITE_LIST)
#print WHITE_LIST_STR
HEADER=['PID' ,  'USER' , 'PR' , 'NI' , 'VIRT' , 'RES' , 'SHR', 'S' ,'%CPU' ,'%MEM',    'TIME+ ', 'COMMAND']
NEWLINE="\n"
SPACE=" "
COLON=": "
SERVER='localhost'


def proc_watch():
	while True:
		top_cmd="top -b -n 1 | sed -n '8,17p'| egrep -v \" "+ WHITE_LIST_STR + "\" |  awk '{print $1}' "
		top_pids=subprocess.Popen(top_cmd,stdout=subprocess.PIPE,shell=True).communicate()[0].strip().split()
		time.sleep(900)
		for pid in top_pids:
			pid_info=["top -b -n 1 -p "+pid+"| sed -n '8,17p'"]
			pid_wall_cmd=[" ps -p "+pid+" --no-headers -o etime"]
	         	pid_wall_info=subprocess.Popen(pid_wall_cmd,stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
	         	rogue_info=subprocess.Popen(pid_info,stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
                	if rogue_info.poll() is None:
				cpu_pid = rogue_info.communicate()[0].split()
				print cpu_pid
				pid_wall = pid_wall_info.communicate()[0].split()
				try:
					if float(cpu_pid[9]) > 10:
						hostname_cmd = subprocess.Popen(['hostname','-s'], stdout=subprocess.PIPE)
						hostname=hostname_cmd.communicate()[0]
						SUBJECT= "mem intensive process " +cpu_pid[0] + " on " + hostname.rstrip() 
	       					TEXT=time.strftime("%d/%m/%Y-%H:%M:%S")+NEWLINE +hostname+NEWLINE 
						TEXT=TEXT+"wall time: " +  ' '.join(pid_wall) + NEWLINE
						for top,values in zip(HEADER,cpu_pid):
							TEXT=TEXT+ top +COLON + values+NEWLINE
						msg= 'Subject: %s\n\n%s' % (SUBJECT, TEXT)
#						msg = MIMEText(TEXT)
						FROM = 'engaging-admin@techsquare.com'
						TO = 'ac@techsquare.com'
						server = smtplib.SMTP(SERVER)
#						server.set_debuglevel(1)
						server.sendmail(FROM, TO, msg)
						server.quit()
				except:
					pass

def main():
                proc_watch()


if __name__ == '__main__':
        main()

