{: .no_toc}
# Concurrency

- TOC
{:toc}

#### Reactive Backpressured File Streaming - Producer Consumer Streaming

Concepts:

1. The Architectural Name: The Producer-Consumer Stream
This is the classic computer science label. You have a Producer (the file reader) and a Consumer (the socket writer). Using Flow with .buffer() is the modern Kotlin way of decoupling these two entities so they can work at different speeds.

2. The Performance Name: Non-Blocking I/O with Backpressure

Non-Blocking: You aren't loading the whole file into RAM (which would cause an OutOfMemoryError on a 10GB file).
Backpressure: The BufferOverflow.SUSPEND strategy ensures that if the network is slow, the file reader "pauses" rather than flooding the memory with un-sent strings.

3. The Pattern Name: Pipeline Decoupling
By using flowOn(Dispatchers.IO), you have effectively created a Thread-Confinement Pipeline. The file reading happens on one thread pool, while the socket writing (the collection) happens on another (the caller's context). This prevents a slow disk from slowing down your network logic and vice versa.

```kotlin
fun streamFileToSocket(file: File, host: String, port: Int) = runBlocking {    
    val fileFlow = flow {
        file.bufferedReader().use { reader ->
            reader.forEachLine { line ->
                emit(line)
            }
        }
    }.flowOn(Dispatchers.IO) 

    Socket(host, port).use { socket ->
        val writer = socket.getOutputStream().bufferedWriter()
        
        fileFlow
            .buffer(100, onBufferOverflow = BufferOverflow.SUSPEND) // Backpressure: pause reader if socket is slow
            .collect { line ->
                writer.write(line)
            }
    }
}
```

Memory optimization if Line is >

```kotlin
    val fileFlow = flow {
        file.bufferedReader().use { reader ->
            val buffer = CharArray(8192)
            var charsRead = reader.read(buffer)
            
            while (charsRead != -1) {                
                emit(String(buffer, 0, charsRead))
                charsRead = reader.read(buffer)
            }
        }
    }
```

#### Throttled Batch Processor

This is a classic "High-Throughput Resiliency" problem.

You have a list of 1,000 Product IDs. You need to fetch details for each from a REST API, but the API allows a maximum of 10 concurrent requests. 

```
val semaphore = Semaphore(10) // Concurrency limit
val client = HttpClient(CIO)

suspend fun fetchProduct(productId: String): String? {
    return retryWithBackoff {
        semaphore.withPermit {
            val response = client.get("https://api.example.com/products/$productId")
            if (response.status == HttpStatusCode.TooManyRequests) throw Exception("Rate limited")
            
            response.body<String>()
        }
    }
}

// Resiliency: Exponential Backoff implementation
suspend fun <T> retryWithBackoff(
    retries: Int = 5,
    initialDelay: Long = 1000,
    block: suspend () -> T
): T? {
    repeat(retries - 1) { attempt ->
        try { return block() } 
        catch (e: Exception) {
            val delayTime = initialDelay * 2.0.pow(attempt).toLong()
            delay(delayTime)
        }
    }
    return block() // Final attempt
}

suspend fun main() = coroutineScope {
    val productIds = (1..1000).map { it.toString() }
    
    // Coroutine collection to process all
    val results = productIds.map { id ->
        async(Dispatchers.IO) { fetchProduct(id) }
    }.awaitAll()
}
```

Add to this a global rate limit of 50qps


```
suspend fun main() = coroutineScope {
    val productIds = (1..1000).map { it.toString() }

    // 1. Define the Pipeline (The Producer)
    val productFlow = productIds.asFlow()
        .onEach { delay(20L) } // Rate limit: 50 QPS (1000ms / 50 = 20ms)
        .flatMapMerge(concurrency = 10) { id ->
            flow {
                val result = fetchProduct(id)
                emit(id to result) // Emit a Pair so we know which ID the result belongs to
            }
        }

    // 2. The Consumer (The bit that collects)
    val successfulResults = mutableListOf<String>()
    
    println("Starting batch processing...")
    val startTime = System.currentTimeMillis()

    productFlow.collect { (id, detail) ->
        if (detail != null) {
            successfulResults.add(detail)
            println("Processed Product: $id")
        } else {
            println("Failed to fetch Product: $id after retries")
        }
    }

    val totalTime = System.currentTimeMillis() - startTime
    println("Completed ${successfulResults.size} products in ${totalTime}ms")
}
```

