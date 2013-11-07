import qiniu.conf
import qiniu.rs
import qiniu.io


import urllib 
import urllib2 
import requests   


AK = "zB0oT4SCMtPWhGlNqwn80AelM3xlkZvuyrOA_-AC"
SK = "ME1r6PXfZNNpdQlVp3yd_kS00M0_L8lNm4vbYN7N"

qiniu.conf.ACCESS_KEY = AK
qiniu.conf.SECRET_KEY = SK
bucket_name = "for-ov-orange"

policy = qiniu.rs.PutPolicy(bucket_name)
uptoken = policy.token()

key = "zzh.jpg"
ret, err = qiniu.io.put(uptoken, key, "test string data")
print ret
if err is not None:
    print err
file_url = "http://%s.qiniudn.com/%s" % (bucket_name, key)
print file_url


base_url = qiniu.rs.make_base_url("for-ov-orange.qiniudn.com", "zzh.jpg")
policy = qiniu.rs.GetPolicy()
private_url = policy.make_request(base_url)

print private_url

url = private_url# 'http://www.blog.pythonlibrary.org/wp-content/uploads/2012/06/wxDbViewer.zip'  
print "downloading with urllib"
urllib.urlretrieve(url, "code.jpg") 