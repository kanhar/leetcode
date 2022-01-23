{: .no_toc}
# System Design Concepts

- TOC
{:toc}
### [CAP Theorem](https://en.wikipedia.org/wiki/CAP_theorem)

> Distributed systems can Consistency or Availability given Partition Tolerance

* **Consistency**: Every read receives the most recent write or error. 
* **Availability**: Every read receives a *mostly* recent write or error
* **Partition tolerance**: The system should operate despite network IO issues.

### [ACID](https://en.wikipedia.org/wiki/ACID)

> Properties of db transactions to guarantee data validity:
* **Atomicity**   - a transaction with multiple operations will either all occur, or none will occur.
* **Consistency** - a transaction will bring the db from one valid state to another, maintaining db invariants ex, FK, PK, Triggers etc.
* **Isolation**   - transactions executed in parallel, should be equivalent to if executed in serial
* **Durability**  - a transaction once committed will remain committed. 

### [BASE](https://en.wikipedia.org/wiki/Eventual_consistency)
> Basically available, Soft-state, Eventually consistent. Ex: NoSQL databases. 
> Requires a reconciliation strategy when conflicts happen

### [Message-delivery guarantees](https://blog.bulloak.io/post/20200917-the-impossibility-of-exactly-once/)

> Producers recovering from a failure retransmit messages for which no acknowledgment. 
> The consumer might have sent a confirmation that never reached the producer. 
> A duplicate message is inevitably sent
>> Or, better stated: there are only two hard problems in distributed systems ;) <BR>
>> 2 Exactly-once delivery <BR>
>> 1 Guaranteed order of messages <BR> 
>> 2 Exactly-once delivery <BR>

### Networking Fundamentals

> TCP
> UDP
> HTTP
> HTTPS
> DNS
> Network interfaces, physical, ARP, DNS, VPN, firewalls, cookies, forward/reverse proxy, ISP/IX

### Encryption

#### Assymetric Key

* Client Hello - Asking for SSL/TLS Version, Cryptographic Algorithms Supported, Data Compression Supported
* Server Hello - Responds with Cryptographic Algorithm from list above, session id, server's digital certificate and server Public Key
* Client contact Server's CA and verify the servers digital certificate. 
* Client Key Exchange - Client sends `Shared Secret Key` encrypted with Server's Public Key
* Client sends a finished message encrypted with `Shared Secret Key`
* Server responds a finished message encrypted with `Shared Secret Key`
   
Note: 4,5,6 can in some sense be considered symmetric key exchange. 