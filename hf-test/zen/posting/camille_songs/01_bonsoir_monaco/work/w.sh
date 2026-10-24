w(){ while [ $(free -g | awk '/Mem/{print $7}') -lt 3 ]; do sleep 10; done; }
