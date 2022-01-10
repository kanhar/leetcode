# KMP
### [CAP Theorem](https://en.wikipedia.org/wiki/CAP_theorem)

> Any distributed data store can only ensure Consistency or Availability given Partition Tolerance

* **Consistency**: Every read receives the most recent write or error. 
* **Availability**: Every request receives a *(possibly not most recent)* write or error
* **Partition tolerance**: The system operates despite message drops 

Two examples, ACID vs BASE ( Basically Available - No-SQL )

### [ACID](https://en.wikipedia.org/wiki/ACID)

> A set of properties of database transactions intended to guarantee data validity despite errors, power failures etc.
* **Atomicity**   - a transaction with multiple operations will either all occur, or none will occur.
* **Consistency** - a transaction will bring the db from one valid state to another, maintaining db invariants ex, FK, PK, Triggers etc.
* **Isolation**   - transactions executed in parallel, should be equivalent to if executed in serial
* **Durability**  - a transaction once committed will remain committed. 

### [BASE](https://en.wikipedia.org/wiki/Eventual_consistency)
> Basically available, Soft-state, Eventually consistent. Basically NoSQL databases. 
> Requires a reconciliation strategy when conflicts happen

### [Message-delivery guarantees](https://blog.bulloak.io/post/20200917-the-impossibility-of-exactly-once/)

> Producers recovering from a failure retransmit any messages for which an acknowledgement has not been 
> received. The consumer might have sent a confirmation that never reached the producer. A duplicate is inevitably created
>> There are only two hard problems in distributed systems :) 
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


