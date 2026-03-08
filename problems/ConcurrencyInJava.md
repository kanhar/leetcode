{: .no_toc}
# Concurrency

- TOC
{:toc}
#### Executor, Futures and Callables

Simple way to do threads:
```java
Runnable task1 = () -> someReallyLongProcess();
Runnable task2 = () -> anotherReallyLongProcess();
Thread thread1 = new Thread(task1);
thread1.start()
Thread thread2 = new Thread(task1);
thread2.start()
```

Using a thread pool (more efficient, uses queues)
```java
Executor executor = Executors.newSingleThreadExecutor();
Runnable task1 = () -> someReallyLongProcess();
Runnable task2 = () -> anotherReallyLongProcess();
executor.execute(task1);
executor.execute(task2)
```

Using a thread pool ( with a Callable vs a Runnable)
```java
Callable<String> task = () -> buildPatientReport();
Future<String> future = executor.submit(task);
String result = future.get();
```

#### Locks

Original/Intrinsic
```java
Object key = new Object();
synchronized(key) {
// do some stuff
}
```

Improved/Extrinsic: interruptible, timed and fair
```java
Lock lock = new ReentrantLock(); // Add isFair=True to make fair
if (lock.tryLock()) {            // Add Timeout to invocation.
    try {
        // guarded block of code
    } 
    finally {
        lock.unlock();
    }
}
```

#### Producer Consumer (Intrinsic)

Intrinsic Locking solution

```java
class Producer {
    public void produce() {
        synchronized(lock) {
            while (isFull(buffer))
                lock.wait();
            buffer[count++] = 1;
            lock.notifyAll();
        }
   }
}

class Consumer {
    public void consume() {
        synchronized(lock) {
        while (isEmpty(buffer))
            lock.wait();
        buffer[--count] = 0;
        lock.notifyAll();
        }
    }
}
```

#### Producer Consumer (Extrinsic)

Intrinsic Locking solution

```java
class Producer {
    public void produce() {
        synchronized(lock) {
            while (isFull(buffer))
                lock.wait();
            buffer[count++] = 1;
            lock.notifyAll();
        }
   }
}

class Consumer {
    public void consume() {
        synchronized(lock) {
        while (isEmpty(buffer))
            lock.wait();
        buffer[--count] = 0;
        lock.notifyAll();
        }
    }
}
```

#### write a file and stream

```
import kotlinx.coroutines.*
import kotlinx.coroutines.channels.BufferOverflow
import kotlinx.coroutines.flow.*
import java.io.File
import java.net.Socket

fun streamFileToSocket(file: File, host: String, port: Int) = runBlocking {
    // 1. Create the producer flow
    val fileFlow = flow {
        file.bufferedReader().use { reader ->
            reader.forEachLine { line ->
                emit(line)
            }
        }
    }.flowOn(Dispatchers.IO) // Keeps file I/O off the main/caller thread

    // 2. Consume the flow and send to TCP Socket
    try {
        Socket(host, port).use { socket ->
            val writer = socket.getOutputStream().bufferedWriter()
            
            fileFlow
                .buffer(100, onBufferOverflow = BufferOverflow.SUSPEND) // Backpressure: pause reader if socket is slow
                .collect { line ->
                    writer.write(line)
                    writer.newLine()
                    writer.flush() // Ensure data is sent over the wire
                }
        }
    } catch (e: Exception) {
        println("Streaming failed: ${e.message}")
    }
}

```

