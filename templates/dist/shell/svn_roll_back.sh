<<<<<<< HEAD

cd /home/svnroot/code/;
svn co {{prefix}}/code/{{svn_package_path}} --username={{username}} --password={{password}} -r {{r}};
cd /home/svnroot/config/;
svn co {{prefix}}/config/{{svn_config_path}} --username={{username}} --password={{password}} -r {{r}};
chmod -R 777 /home/svnroot/code/{{svn_package_path}};
chmod -R 777 /home/svnroot/config/{{svn_config_path}};
mkdir /home/code_config_merge/tmp_{{date}}/;
rsync -av --exclude=.svn /home/svnroot/code/{{svn_package_path}}/ /home/code_config_merge/tmp_{{date}}/;
rsync -av --exclude=.svn /home/svnroot/config/{{svn_config_path}}/ /home/code_config_merge/tmp_{{date}}/;
rsync -e 'ssh -p 36000 -l Administrator' -azv --exclude=.svn /home/code_config_merge/tmp_{{date}}/ 192.168.2.140:/cygdrive/e/Publish/{{execute_machine}}/;
=======

cd /home/svnroot/code/;
svn co {{prefix}}/code/{{svn_package_path}} --username={{username}} --password={{password}} -r {{r}};
cd /home/svnroot/config/;
svn co {{prefix}}/config/{{svn_config_path}} --username={{username}} --password={{password}} -r {{r}};
chmod -R 777 /home/svnroot/code/{{svn_package_path}};
chmod -R 777 /home/svnroot/config/{{svn_config_path}};
mkdir /home/code_config_merge/tmp_{{date}}/;
rsync -av --exclude=.svn /home/svnroot/code/{{svn_package_path}}/ /home/code_config_merge/tmp_{{date}}/;
rsync -av --exclude=.svn /home/svnroot/config/{{svn_config_path}}/ /home/code_config_merge/tmp_{{date}}/;
rsync -e 'ssh -p 36000 -l Administrator' -azv --exclude=.svn /home/code_config_merge/tmp_{{date}}/ 192.168.2.140:/cygdrive/e/Publish/{{execute_machine}}/;
>>>>>>> 1cab5b5bd2c27b7751579bc34333bc3c51e66be5
rm -rf /home/code_config_merge/tmp_{{date}}/;