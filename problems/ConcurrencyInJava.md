{: .no_toc}
# Concurrency

- TOC
{:toc}
#### Kotlin 101 Async    
Kotlin Sequential Async 

```kotlin
import kotlinx.coroutines.*
import kotlin.math.pow

suspend fun doWork(): String = withContext(Dispatchers.IO) {
    val networkResult = retryWithBackoff { getNetworkResult() }
    val dbResult = getDatabaseResult(networkResult)
    "Final Result: $dbResult" 
}

suspend fun <T> retryWithBackoff(
    retries: Int = 5,
    initialDelay: Long = 1000,
    block: suspend () -> T
): T {
    for (attempt in 0 until retries - 1) {
        try {
            return block()
        } catch (e: Exception) {
            // .pow() expects Double, so we cast 'attempt' and then the result to Long
            val delayTime = (initialDelay * 2.0.pow(attempt.toDouble())).toLong()
            delay(delayTime)
        }
    }

    return block() // Final attempt outside the loop
}   
```

Kotlin Parallel Async
```kotlin
suspend fun doWorkParallel(): String = withContext(Dispatchers.IO) {
    coroutineScope {
        val networkDeferred = async { retryWithBackoff { getNetworkResult() } }
        val dbDeferred = async { getDatabaseResult() }

        val networkResult = networkDeferred.await()
        val dbResult = dbDeferred.await()

        "Combined: $networkResult and $dbResult"
    }
}
```

Kotlin with flows
```kotlin
fun doWorkFlow(): Flow<String> = flow {    
    val result = retryWithBackoff { getNetworkResult() }
    emit(result) 
}
.flowOn(NetworkDispatcher) // <--- Changes the "Upstream" context

withContext(DbDispatcher) {     
    doWorkFlow().collect { networkResult ->
        saveToDatabase(networkResult) 
    }
}
```





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

```kotlin
val semaphore = Semaphore(10) // Concurrency limit
val client = HttpClient(CIO)

// supervisorScope -> continue if one fails
// coroutineScope -> exit all if one fails 
suspend fun main() = supervisorScope {
    val productIds = (1..1000).map { it.toString() }
        
    val results = productIds.map { id ->
        async(Dispatchers.IO) { fetchProduct(id) }
    }.awaitAll()
}

suspend fun fetchProduct(productId: String): String? {
    return retryWithBackoff {
        semaphore.withPermit {
            val response = client.get("https://api.example.com/products/$productId")
            if (response.status == HttpStatusCode.TooManyRequests) throw Exception("Rate limited")
            
            response.body<String>()
        }
    }
}

suspend fun <T> retryWithBackoff(
    retries: Int = 5,
    initialDelay: Long = 1000,
    block: suspend () -> T
): T? {
    // We loop from 0 up to (but not including) retries - 1
    for (attempt in 0 until retries - 1) {
        try {
            return block()
        } catch (e: Exception) {
            val delayTime = initialDelay * 2.0.pow(attempt).toLong()
            delay(delayTime)
        }
    }
    
    // Final attempt outside the loop (the "last stand")
    return try {
        block()
    } catch (e: Exception) {
        null 
    }
}
```

Alternative solution with flows and rate limiting:

```kotlin
// Rate Limiter (50 req/s)
class RateLimiter(eventsPerSecond: Int) {
    private val mutex = Mutex()
    private val intervalMillis = 1000L / eventsPerSecond
    private var lastEventTime = 0L

    suspend fun acquire() = mutex.withLock {
        val currentTime = System.currentTimeMillis()
        val elapsed = currentTime - lastEventTime
        if (elapsed < intervalMillis) {
            delay(intervalMillis - elapsed)
        }
        lastEventTime = System.currentTimeMillis()
    }
}

val rateLimiter = RateLimiter(50)

suspend fun main() = {
    val productIds = (1..1000).map { it.toString() }

    val results = productIds.asFlow()
        // Step 1: Throttling (Rate Limit)
        .onEach { rateLimiter.acquire() } 
        // Step 2: Concurrency (Semaphore replacement)
        .flatMapMerge(concurrency = 10) { id ->
            flow {
                val product = fetchProduct(id)
                emit(product)
            }.catch { e -> 
                println("Failed to fetch $id: ${e.message}")
                emit(null) // Emit null so we don't lose the index
            }
        }
        .flowOn(Dispatchers.IO)
        .toList() // Collects all results into a single List<String?>

    println("Successfully processed ${results.filterNotNull().size} products.")
}
```
