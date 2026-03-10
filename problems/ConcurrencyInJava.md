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

#### Throttled Batch Processor

This is a classic "High-Throughput Resiliency" problem.

You have a list of 1,000 Product IDs. You need to fetch details for each from a REST API, but the API allows a maximum of 10 concurrent requests and a global rate limit of 50 requests per second. We must balance three competing constraints: Concurrency (active connections), Rate Limiting (requests per window), and Error Handling (resiliency).

```

```

