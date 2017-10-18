X=`cat README.txt`
git add .
git commit -m "'$X'"
num=$(python -c "print $X + 0.1")
echo $num > README.txt
git push origin master

