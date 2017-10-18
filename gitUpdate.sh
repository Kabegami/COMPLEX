#script pour incrementer la version car j'ai la fleme de le faire à la main
X=`cat README.txt`
git add .
git commit -m "$X"
num=$(python -c "print $X + 0.1")
echo $num > README.txt
git push origin master

