from sevencow import Cow

ACCESS_KEY = "zB0oT4SCMtPWhGlNqwn80AelM3xlkZvuyrOA_-AC"
SECRET_KEY = "ME1r6PXfZNNpdQlVp3yd_kS00M0_L8lNm4vbYN7N"
BUCKET = "orange"

cow = Cow(ACCESS_KEY, SECRET_KEY)
b = cow.get_bucket(BUCKET)

print cow.list_buckets()

print "files:"
for f in b.list_files()["items"]:
	print f["key"]

#b.put('thinking-in-go.mp4')

#base_url = qiniu.rs.make_base_url('', key)
#policy = qiniu.rs.GetPolicy()
#private_url = policy.make_request(base_url)