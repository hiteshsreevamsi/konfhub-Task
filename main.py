import http.client
import json
from nltk.tokenize import word_tokenize
import numpy as np

finalAns = {}
conn = http.client.HTTPSConnection("o136z8hk40.execute-api.us-east-1.amazonaws.com")
payload = ''
headers = {}
conn.request("GET", "/dev/get-list-of-conferences", payload, headers)
res = conn.getresponse()
data = json.loads(res.read().decode("utf-8"))

"""for val in data.get("paid"):
    print("conference name : " + val.get("confName"))
    print("venue : " + val.get("venue"))
    print("payment status : " + val.get("entryType"))
    print("conference start date : " + val.get("confStartDate"))
    print()
"""


def cosine_similarity(x, y):
    x, y = str(x).lower(), str(y).lower()
    x, y = set(word_tokenize(x)), set(word_tokenize(y))
    rvector = x.union(y)
    x_vec = np.zeros(len(rvector))
    y_vec = np.zeros(len(rvector))
    if x:
        x_vec = np.array([1 if _x in x else 0 for _x in rvector])
    if y:
        y_vec = np.array([1 if _x in y else 0 for _x in rvector])
    cosine = np.dot(x_vec, y_vec) / len(rvector) ** 2
    return 0 if np.isnan(cosine) else cosine


def calc_similarity(x: dict, y: dict):
    cosine_arr = list()
    keys_to_compare = ["searchTerms", "confName", "keywordSupport", "confUrl", "confRegUrl"]
    for k in keys_to_compare:
        cosine_arr.append(cosine_similarity(x[k], y[k]))
    return np.array(cosine_arr).mean()


def ExactlySimilar():
    tempresult = {}
    for var in data.get("paid"):
        if var.get("confName") in tempresult:
            tempresult[var.get("confName")].append(var)
        else:
            temporary = list()
            temporary.append(var)
            tempresult[var.get("confName")] = temporary

    for var1 in data.get("free"):
        if var1.get("confName") in tempresult:
            tempresult[var1.get("confName")].append(var)
        else:
            temporary = list()
            temporary.append(var)
            tempresult[var1.get("confName")] = temporary
    for k, v in tempresult.items():

        if len(v) > 1:

            n = 0
            store = ""
            store1 = ""
            store2 = ""
            for dif in v:

                if n == 0:
                    store = dif.get("confUrl")
                    store1 = dif.get("confStartDate")
                    store2 = dif.get("venue")
                    store3 = dif.get("entryType")
                    n = n + 1
                    continue
                if store == dif.get("confUrl") and store1 == dif.get("confStartDate") and store2 == dif.get("venue"):
                    li = 1
                    if li == 1:
                        print("conference Name : " + k)
                        print("conference url : " + dif.get("confUrl"))
                        print("conference venue : " + dif.get("venue"))
                        print("start date : " + dif.get("confStartDate"))
                        print("Entry type : " + dif.get("entryType"))
                        print()
                        li = li - 1

                    print("conference Name : " + k)
                    print("conference url : " + dif.get("confUrl"))
                    print("conference venue : " + dif.get("venue"))
                    print("start date : " + dif.get("confStartDate"))
                    print("Entry type : " + dif.get("entryType"))
                    print()


ExactlySimilar()


def partiallySimilar():
    local = {}
    for var2 in data.get("paid"):
        if len(local) < 1:
            once = list()
            once.append(var2)
            local[var2.get("confName")] = once
        else:
            max = 0.1
            temp5 = var2.get("confName")
            temp_d = list(local.keys())
            for temp2 in temp_d:
                num = np.array([calc_similarity(var2, o) for o in local[temp2]]).max()
                if num > max:
                    max = num
                    temp5 = temp2
            try:
                local[temp5].append(var2)
            except KeyError:
                simpl = list()
                simpl.append(var2)
                local[temp5] = simpl
    for var2 in data.get("free"):
        if len(local) < 1:
            once = list()
            once.append(var2)
            local[var2.get("confName")] = once
        else:
            max = 0.1
            temp5 = var2.get("confName")
            temp_d = list(local.keys())
            for temp2 in temp_d:
                num = np.array([calc_similarity(var2, o) for o in local[temp2]]).max()
                if num > max:
                    max = num
                    temp5 = temp2
            try:
                local[temp5].append(var2)
            except KeyError:
                simpl = list()
                simpl.append(var2)
                local[temp5] = simpl

    for value in local.values():
        for dif1 in value:
            print("conference Name : " + dif1.get("confName"))
            print("conference url : " + dif1.get("confUrl"))
            print("conference venue : " + dif1.get("venue"))
            print("start date : " + dif1.get("confStartDate"))
            print("Entry type : " + dif1.get("entryType"))
            print()


partiallySimilar()
