{: .no_toc}
# System Design Concepts

- TOC
{:toc}

The ultimate primer: https://github.com/donnemartin/system-design-primer  

### [CAP Theorem](https://en.wikipedia.org/wiki/CAP_theorem)

> Distributed systems can achieve either Consistency or Availability given Partition Tolerance.
> However, see updated version of Eric Brewer's statement on this [here](https://research.google/pubs/pub45855/)

* **Consistency**: Every read receives the most recent write or error. 
* **Availability**: Every read receives a *mostly* recent write or error
* **Partition tolerance**: The system should operate despite network IO issues.

### Distributed Locking

* **Optimistic Locking** - read a record, take note of a version indicator( version number / timestamps / 
  checksums/hashes), confirm it hasn't changed before you write the record back
* **Pessimistic Locking** - assume the record has changed or will change. Lock resource before engaging in a read.

See also:
* [Impossibility of Distributed Consensus with One Faulty Process](https://www.the-paper-trail.org/post/2008-08-13-a-brief-tour-of-flp-impossibility)
* [Why RedLock won't work](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html) vs
[its rebuttal](http://antirez.com/news/101)

### [ACID](https://en.wikipedia.org/wiki/ACID)

> Properties of db transactions to guarantee data validity:
* **Atomicity**   - a transaction with multiple operations will either all occur, or none will occur.
* **Consistency** - a transaction will bring the db from one valid state to another, maintaining db invariants ex, FK, PK, Triggers etc.
* **Isolation**   - transactions executed in parallel, should be equivalent to if executed in serial
* **Durability**  - a transaction once committed will remain committed. 

### [BASE](https://en.wikipedia.org/wiki/Eventual_consistency)
> Basically available, Soft-state, Eventually consistent. Ex: NoSQL databases. 
> Requires a reconciliation strategy when conflicts happen
> Best practical example: DNS

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
> Network interfaces, physical, ARP, DNS, VPN, firewalls, cookies, forward/reverse proxy, 
> [ISP/IX](https://en.wikipedia.org/wiki/Internet_exchange_point)

### Encryption: TLS

* Client Hello - Asking for SSL/TLS Version, Cryptographic Algorithms Supported, Data Compression Supported
* Server Hello - Responds with Cryptographic Algorithm from list above, session id, server's digital certificate and server Public Key
* Client contact Server's CA and verify the servers digital certificate. 
* Client Key Exchange - Client sends `Shared Secret Key` encrypted with Server's Public Key
* Client sends a finished message encrypted with `Shared Secret Key`
* Server responds a finished message encrypted with `Shared Secret Key`
   
Note: A subset of the steps above, ex: 4,5,6 can in some sense be considered symmetric key exchange. 

### [Caching Patterns](https://codeahoy.com/2017/08/11/caching-strategies-and-how-to-choose-the-right-one/)

* Cache-Aside - check cache first - if miss then check db return to application - application updates cache
* Read-Through - check cache first - if miss then check db and update cache, then return result to application
* Write-Through - data is always first written to the cache and then to the database
* Write-Around - always write to db, only  data that is read makes it way into the cache.  
* Write-Back - write to cache which acknowledges immediately and after some delay writes to db.

### Estimation

* Signed b-bit Integer: 2^b
* Unsigned b-bit Integer: -2^(b-1) -- 2^(b-1)-1
* ASCII char - 8 bits ( really only 7 used) = 1 byte 
* Unicode char - 16 bits or 2^16 = 65536 = 2 bytes
* Long/Double number = 64 bits = 8 bytes
* Timestamp in nanoseconds = 8 bytes  
* UUID/GUID: 16 bytes  
* Sample Db Row:
** id (long) + username(10ch) + email ( 50ch) = 8+20+100  ~ 150 bytes
** 1 billion users: 150b * 10e9 = 145 gb
  
* Read sequentially from HDD: 30 MB/s
* Read sequentially from SSD: 1 GB/s
* Read sequentially from memory: 4 GB/s
* Read sequentially from 1Gbps Ethernet: 100MB/s

* SQL Db: 100-250GB. 25K conns per second
* Redis Cache: 300GB. 100k conns. per second
* Queues: 3000 messages per second ( seems low)

* LAN RTT: 5-50ms
* Continental RTT: 70-100ms
* International RTT: 100-200ms

* Base 62 Encoding of a Md5 Hash of a Long string.
* 7 digit base 62 - 62^7 = 3.5 Trillion combinations ( which takes < 2^43 bits to store)
*
