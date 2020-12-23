PRESET=$1

PASS=VkkoIiMn3QEDhW
USER=Kimberley
HOST=82.202.236.23
ROOT_FOLDER=sitefront/web/dist
ZIP=debug

export SSHPASS=$PASS

cd $PRESET && zip -r upload.zip * &&

sshpass -e scp -P 22002 upload.zip Kimberley@82.202.236.23:sitefront/web/dist/images &&
sshpass -e ssh -p 22002 -t -o StrictHostKeyChecking=no $USER@$HOST <<EOF
    cd $ROOT_FOLDER/images
    unzip upload.zip -d catalog/
    rm upload.zip
EOF

rm upload.zip