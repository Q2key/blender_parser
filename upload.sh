SOURCE=$1
DEST=$2
EXT=$3

PASS=VkkoIiMn3QEDhW
USER=Kimberley
HOST=82.202.236.23

export SSHPASS=$PASS

cd $SOURCE && 
ls &&
zip upload.zip *.$EXT &&

sshpass -e scp -P 22002 upload.zip Kimberley@82.202.236.23:sitefront/web/images/$DEST &&
sshpass -e ssh -p 22002 -t -o StrictHostKeyChecking=no $USER@$HOST <<EOF
    cd sitefront/web/images/$DEST
    unzip upload.zip
    rm upload.zip
EOF

rm upload.zip