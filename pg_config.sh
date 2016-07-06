echo "***************************************
*********************************************
******  Start Provisioning VM ***************
*********************************************
*********************************************"
sudo apt-get -qqy update 
sudo apt-get -y upgrade
sudo apt-get -qqy install git
sudo apt-get -y install python-pip 

wget https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash
wget https://raw.githubusercontent.com/git/git/master/contrib/completion/git-prompt.sh
wget https://www.udacity.com/api/nodes/3333158951/supplemental_media/bash-profile-course/download

cat download >> .bashrc
rm download


echo"********************************************************
******************** git configs ****************************
*************************************************************"
gc1='git config --global user.name "Jeff Reiher"'
gc2='git config --global user.email "jreiher2003@yahoo.com"'
gc3='git config --global push.default upstream'
gc4='git config --global merge.conflictstyle diff3'
gc5='git config --global credential.helper "cache --timeout=10000"'
$gc1
$gc2
$gc3
$gc4
$gc5
echo "*********** done ************************"

sudo pip install virtualenvwrapper
# append these lines to .bashrc  
# export WORKON_HOME=$HOME/.virtualenvs
# source /usr/local/bin/virtualenvwrapper.sh
# run -- source .bashrc 
# deactivate to get out
# workon personal-site >> to activate
# set environmental vars
# sudo nano $VIRTUAL_ENV/bin/postactivate 
# export APP_SETTINGS=""

