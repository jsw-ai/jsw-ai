# block until >=3 GB available (free -g, available column); my gates run strictly sequentially in one queue
while [ $(free -g | awk '/Mem/{print $7}') -lt 3 ]; do sleep 5; done
