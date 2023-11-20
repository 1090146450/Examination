#! /bin/bash
echo "开始拉取代码"
git stash
git pull origin master
git stash pop
echo "进入虚拟环境"
source /home/an/python_examin/bin/activate python_examin
echo "进入成功"
cd /home/an/Examin/Examination/
pip3 install -r requirments.txt
du="`netstat -ntulp|grep 8002`"
if [[ "${du}" != "" ]];then
 lis=$IFS
 IFS=" "
 ardu=($du)
 IFS=$lis
 for var in ${ardu[@]}
  do
  if [[ "${var}" =~ "/" ]]; then
   dd=$IFS
   IFS="/"
   tes=($var)
   IFS=$dd
   echo "进程号为:"${tes}
   kill -9 ${tes}
   echo "kill success"
  fi
 done
else
 echo "无进程直接创建"
fi
sleep 2
echo "加载uwsgi服务"
uwsgi --ini uwsgi.ini
echo "重启NGINX服务"
nginx -s reload
cd ../
git add .
git commit -m "更新PID"
git push origin master

