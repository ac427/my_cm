#!/bin/bash -l 

cat <<EOF > /root/out/status.html 
<!DOCTYPE html>
<html> <head> <script src="jquery.js">
</script>
EOF

for file in $(find /root/tmp -name '*.html' -type f -printf "%f\n" )
do
div=$(echo $file | sed 's/.html//g')
cat <<EOF >> /root/out/status.html
	<script>
	\$(function(){
        	\$("#$div").load("$file");
	});
	</script>
EOF
done

cat <<EOF >> /root/out/status.html

</head>
<body>

EOF

for file in $(find /root/tmp -name '*.html' -type f -printf "%f\n" | sed 's/.html//g')
do

cat <<EOF >> /root/out/status.html
	<div id="$file"></div>
EOF
done
cat <<EOF >> /root/out/status.html

</body>
</html>

EOF
