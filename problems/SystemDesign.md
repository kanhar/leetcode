# KMP
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
>> Or, better stated: there are only two hard problems in distributed systems ;)
>> 2. Exactly-once delivery 
>> 1. Guaranteed order of messages 
>> 2. Exactly-once delivery

### Networking Fundamentals

> TCP
> UDP
> HTTP
> HTTPS
> DNS
> Network interfaces, physical, ARP, DNS, VPN, firewalls, cookies, forward/reverse proxy, ISP/IX


