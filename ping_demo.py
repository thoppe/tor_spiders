from tor_spiders import tor_request_pool

if __name__ == "__main__":

    T = tor_request_pool(2)

    url = 'https://api.ipify.org?format=json'
    
    for x in range(10):
        T.put(url)

    for r in T:
        print r.text
