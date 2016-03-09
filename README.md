First
初次导入请手动下载当前完整的cve归档
下载地址：https://nvd.nist.gov/download.cfm
然后手工导入，暂时没有做好自动初始化的功能

使用实例：
python nvdparse.py -H localhost -u root -p root -f nvdcve-2.0-2002.xml

second
日后的同步工作
同步工作通过sync_nvd来进行，会自动下载每天更新的Modify.xml进行导入

可以这样做：
crontab -u root -e 
在末尾添加：
0 10 * * * /root/sync_nvd > /dev/null 2>&1  这个规则的用处是每天上午10点，执行同步任务
