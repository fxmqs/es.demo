
import string
import random
import time
import os
from elasticsearch import Elasticsearch
from elasticsearch import helpers  

models = []
versions = []
vendors = ["dahua", "lechange"]
es = Elasticsearch()


for i in range(0, 5000) :
    model = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    models.append(model)


for i in range(0, 5000) :
    version = ''.join(random.sample(string.ascii_letters + string.digits, 32))
    versions.append('version' + version)


date1 = (2016,1,1,0,0,0,-1,-1,-1)
time1 = time.mktime(date1)
date2 = (2017,1,1,0,0,0,-1,-1,-1)
time2 = time.mktime(date2)

once = 1000


f = open('process.txt', 'w')
# for i in range(0, 100000) :
for i in range(0, 10000) :
    f.write(str(i) + "\n")
    f.flush()
    print(i)
    actions = []
    for j in range(0, once) : 
        no = i * once + j
        sn = ''.join(random.sample(string.ascii_letters + string.digits, 24))
        model = models[random.randint(0, 4999)]
        version = versions[random.randint(0, 4999)]
        vendor = vendors[random.randint(0, 1)]
        random_time = random.uniform(time1,time2)
        register = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(random_time))
        device = {"sn": sn, "model": model, "version": version, "vendor": vendor, 
                    "region_level_1": "中国", "region_level_2": "", "region_level_3": "", 
                    "first_regist_time": register}

        action = {  
            "_index":"devices-new",  
            "_type":"device",  
            "_id":no,  
            "_source":device
        }  
        actions.append(action)  


        # res = es.index(index = "devices", doc_type = "device", body = device, id = no)
    helpers.bulk(es, actions)  
    #     cmd = cmd + "curl -H \"Content-Type: application/json\" -XPOST 'localhost:9200/devices/device/{}' \
    #         -d '{}\"sn\":\"{}\", \"model\": \"{}\", \"version\": \"{}\", \"region_level_1\": \"中国\", \
    #         \"region_level_2\": \"\", \"region_level_3\": \"\", \"vendor\": \"{}\", \
    #         \"first_regist_time\": \"{}\"{}';".format(no, "{", 'sn' + sn, models[model], versions[version], \
    #         vendors[vendor], register, "}")
        
    # os.system(cmd)

f.close()

if __name__=='__main__':
    f = open('models.txt', 'w')
    for o in models : 
        f.write(o + "\n")
    f.close()

    f = open('versions.txt', 'w')
    for o in versions : 
        f.write(o + "\n")
    f.close()

    f = open('vendors.txt', 'w')
    for o in vendors : 
        f.write(o + "\n")
    f.close()