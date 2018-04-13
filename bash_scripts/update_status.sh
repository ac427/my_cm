#!/bin/bash -l 

x=1
for i in $(ls /home/run/Maildir/cur/);do 
echo "<div> <pre> " >  /root/tmp/status_$x.html
echo "Email update #$x" >> /root/tmp/status_$x.html
grep multipart/alternative  /home/run/Maildir/cur/$i &> /dev/null 
if [ $? -eq 0 ]; then
	sed -n '/Content-Type: text\/plain/,/--/p' /home/run/Maildir/cur/$i |  egrep -v "^Content|^\-"  >> /root/tmp/status_$x.html 
	echo "</pre> </dev> " >>  /root/tmp/status_$x.html
	x=$((x+1))
else
	cat /home/run/Maildir/cur/$i  |  formail -k -X From: -X Subject: | egrep -v "^Content|^\-" |  iconv -f UTF-8 -t ISO-8859-1 >> /root/tmp/status_$x.html 
	echo  >> /root/tmp/status_$x.html 
	echo "</pre> </dev> " >>  /root/tmp/status_$x.html
	x=$((x+1))
fi
done

for i in $(ls /home/run/Maildir/new/);do
echo "<div> <pre> " >  /root/tmp/status_$x.html
echo "Email update #$x" >> /root/tmp/status_$x.html
grep multipart/alternative  /home/run/Maildir/new/$i &> /dev/null 
if [ $? -eq 0 ]; then
        sed -n '/Content-Type: text\/plain/,/--/p' /home/run/Maildir/new/$i |  egrep -v "^Content|^\-"  >> /root/tmp/status_$x.html
	echo "</pre> </dev> " >>  /root/tmp/status_$x.html
	x=$((x+1))
else
        cat /home/run/Maildir/new/$i  |  formail -k -X From: -X Subject: | egrep -v "^Content|^\-" |  iconv -f UTF-8 -t ISO-8859-1 >> /root/tmp/status_$x.html
        echo  >> /root/tmp/status_$x.html
	echo "</pre> </dev> " >>  /root/tmp/status_$x.html
        x=$((x+1))
fi
done

/root/cron/script.sh

mv /root/tmp/*.html /var/www/runacrun.com/public_html/
mv /root/out/status.html /var/www/runacrun.com/public_html/
