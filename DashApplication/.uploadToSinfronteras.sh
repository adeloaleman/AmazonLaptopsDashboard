# scp  -r  *  root@sinfronteras.ws:/var/www/sinfronteras/SADashboard

# rsync  -av    --exclude  'data/NRC-Sentiment-Emotion-Lexicons'    .    root@sinfronteras.ws:/var/www/sinfronteras/SADashboard


# ssh -i   /home/adelo/desktop/it_cct/.tr4sh-it_cct/Cloud_and_Virtualisation_Frameworks/CA2/adelo-laptop.pem   ubuntu@34.205.203.124   'mkdir /home/ubuntu/temp'
# rsync  -rave     "ssh -i   /home/adelo/desktop/it_cct/.tr4sh-it_cct/Cloud_and_Virtualisation_Frameworks/CA2/adelo-laptop.pem"     --exclude  'data/NRC-Sentiment-Emotion-Lexicons'       .        ubuntu@34.205.203.124:/home/ubuntu/temp
# ssh -i   /home/adelo/desktop/it_cct/.tr4sh-it_cct/Cloud_and_Virtualisation_Frameworks/CA2/adelo-laptop.pem   ubuntu@34.205.203.124   'sudo mv /home/ubuntu/temp/* /var/www/html/SADashboard'

# ssh -i   /home/adelo/.aws_ssh_key_pem/my-laptop.pem   ubuntu@34.244.10.211   'mkdir /home/ubuntu/temp'
# rsync  -rave     "ssh -i   /home/adelo/.aws_ssh_key_pem/my-laptop.pem"     --exclude  'data/NRC-Sentiment-Emotion-Lexicons'       .        ubuntu@34.244.10.211:/home/ubuntu/temp
# ssh -i   /home/adelo/.aws_ssh_key_pem/my-laptop.pem   ubuntu@34.244.10.211   'sudo mv /home/ubuntu/temp/* /var/www/html/SADashboard'


rsync  -rave     "ssh -i   /home/adelo/.aws_ssh_key_pem/my-laptop.pem"     --exclude  'data/NRC-Sentiment-Emotion-Lexicons'       .        ubuntu@54.217.40.182:/home/ubuntu/SADashboard 


# ssh  root@sinfronteras.ws  'systemctl restart SADashboard'




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
