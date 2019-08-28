```bash
sudo yum -y update
sudo amazon-linux-extras install -y epel
sudo yum install -y python3-devel gcc nginx
pip3 install --upgrade pip setuptools wheel --user
pip install virtualenv --user

mkdir $WORKDIR
cd $WORKDIR
virtualenv $WORKDIR/myprojectenv
source $WORKDIR/myprojectenv/bin/activate
# add the files below
deactivate
```

`~/myproject/myproject.py`
```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
```

`~/myproject/wgsi.py`
```python
from myproject import app as application

if __name__ == "__main__":
    application.run()
```

`/etc/systemd/system/myproject.service`
```ini
[Unit]
Description=Gunicorn instance to serve myproject
After=network.target

[Service]
User=user
Group=nginx
WorkingDirectory=/home/ec2-user/myproject
Environment="PATH=/home/ec2-user/myproject/myprojectenv/bin"
ExecStart=/home/ec2-user/myproject/myprojectenv/bin/gunicorn --workers 3 --bind unix:myproject.sock -m 007 wsgi

[Install]
WantedBy=multi-user.target
```

Enable the service to start at boot
```bash
sudo systemctl start myproject
sudo systemctl enable myproject
```

Add a server block to the default Nginx configuration file
`/etc/nginx/nginx.conf`
```conf
http {
    . . .

    include /etc/nginx/conf.d/*.conf;

    <!-- line 37 -->
    server {
      listen 80;
      server_name 172.31.42.93;

      location / {
          proxy_set_header Host $http_host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;
          proxy_pass http://unix:/home/ec2-user/myproject/myproject.sock;
      }
    }
    <!-- end insert -->
    server {
        listen 80 default_server;

        . . .
```

Add the nginx user to the user group, substituting the `user`
```bash
sudo usermod -a -G ec2-user nginx
# give execution permission to home directory
chmod 710 /home/ec2-user
# test nginx configuration for syntax errors
sudo nginx -t
```

Start and enable the Nginx process to occur automatically
```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```
