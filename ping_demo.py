from tor_spiders import tor_request_pool


if __name__ == "__main__":

    T = tor_request_pool(3)

    for x in range(10):
        url = 'https://api.ipify.org?format=json'
        r = T.get(url)
        print r.text
