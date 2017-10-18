X=`cat README.txt`
git add .
git commit -m "'$X'"
echo $(($X + 1)) > README.txt
git push origin master

