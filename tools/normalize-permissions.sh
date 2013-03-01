chown -R root:bvs ../bireme/
chown -R apache:bvs  ../bireme/media
chown -R apache:bvs  ../bireme/whoosh

find ../bireme -type f | xargs chmod 664
find ../bireme -type d | xargs chmod 775 
