X=`cat README.txt`
git add .
git commit -m "'$X'"
num = $(echo $X + 0.1 | bc)
echo $num > README.txt
git push origin master

