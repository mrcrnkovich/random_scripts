def merge_hashes(hashes):
    dictionaries = hashes.split("|")

    return merge(dict(dictionaries[0]), dict(dictionaries[1]))

def merge(D1 , D2):
    new = {}

    unique_keys = set((list(D1.keys())).extend(list(D2.keys())))
    
    for key in unique_keys:
        if (key in D1.keys() and key in D2.keys()):
            if type(D1[key]) == list:
                new[key] = D1[key].extend(D2[key])
            elif type(D1[key]) == dict:
                new[key] = merge(D1[key], D2[key])
            else:
                new[key] = D2[key]
        elif (key in D1.keys()):
            #add key from dict 1
            new[key] = D1[key]
        else:
            #add key from dict 2
            new[key] = D2[key]
        
    return new

if __name__ == "__main__":
    merge({"foo": "bar"} , {"foo": "baz", "fibonacci": [1, 1, 2, 3, 5]})