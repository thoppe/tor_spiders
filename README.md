# Tor spiders

Information online has limits. 
These limits are often enforced per-user and sometimes per IP address. 
To circumvent these limits and to keep your identity secret, you'll need a way to simultaneously create multiple anonymous IP identities.
For this we can tap into the darknet and leverage the power of Tor.

Tor (The Onion Router) is a network protocol that enables anonymous communication. Specifically [onion routing](https://en.wikipedia.org/wiki/Tor_(anonymity_network):

> ... is implemented by encryption in the application layer of a communication protocol stack, nested like the layers of an onion. Tor encrypts the data, including the destination IP address, multiple times and sends it through a virtual circuit comprising successive, randomly selected Tor relays. Each relay decrypts a layer of encryption to reveal only the next relay in the circuit in order to pass the remaining encrypted data on to it. The final relay decrypts the innermost layer of encryption and sends the original data to its destination without revealing, or even knowing, the source IP address.

This is perfect for creating a small batch of agents to spider data across the web.

## Usage

Import a `tor_request_pool` with the specified number of Tor connections. These take a long time to initialize the first time so be patient, subsequent runs are much faster. Fill up the internal queue with `.put` and the results will begin downloading when you iterate over the object. Internally threading is used to allow simultaneous connections. The results are stored in a `requests` like object:


    from tor_spiders import tor_request_pool

    T = tor_request_pool(2)
    url = 'https://api.ipify.org?format=json'
    
    for x in range(10):
        T.put(url)

    for r in T:
        print r.text

## requirements

    requesocks==0.10.8
    stem==1.4.0