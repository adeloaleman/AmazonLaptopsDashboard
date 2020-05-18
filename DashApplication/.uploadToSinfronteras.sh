scp  -r  *  root@sinfronteras.ws:/var/www/sinfronteras/SADashboard
ssh  root@sinfronteras.ws  'systemctl restart SADashboard'



# # Some commands that can be useful to troubleshoot
# source SADashboard-env/bin/activate
# deactivate
# 
# python index.py
# http://62.171.143.243:8050
# 
# gunicorn --bind 0.0.0.0:5000 wsgi:server
# http://62.171.143.243:5000 
# 
# vi /etc/systemd/system/SADashboard.service
# systemctl daemon-reload
# sudo systemctl restart SADashboard
# sudo systemctl start   SADashboard
# sudo systemctl enable  SADashboard
# 
# sudo systemctl restart nginx.service
