# declarations
GIT_URL="https://github.com/minelminel/celery-rabbitmq-example.git"
WORKDIR="artifice"

# install core dependencies
sudo yum update -y
sudo yum install -y install epel-release
sudo yum install -y python-pip python-devel gcc nginx
sudo pip install --upgrade pip setuptools wheel
sudo pip install virtualenv

# clone the repo in to place
mkdir ~/$WORKDIR
git clone $GIT_URL ~/$WORKDIR
cd ~/$WORKDIR

# enter virtualenv
virtualenv env
source env/bin/activate
pip install gunicorn

# install redis-server, rabbitmq, amqp
# configure redis password, start services

# install our package
pip install -e .

# configure server

# start the service
