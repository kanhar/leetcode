{: .no_toc}
# Paged REST API Client (Kotlin)

> A service returns its results in pages. Page 1 tells you how many pages there are in total. Write the code that gets all the items. Then make it faster.

<style>
/* Code on this page wraps instead of scrolling sideways, and the column is a little wider on desktop. */
pre, code { white-space: pre-wrap; overflow-wrap: anywhere; }
pre code { font-size: 12px; line-height: 1.45; }
@media (min-width: 961px) {
  .wrapper { width: 940px; }
  section { width: 640px; }
}
</style>

- TOC
{:toc}

### 1. What we are building

You call a service and it does not hand you everything at once. It gives you the first page of items, and tells you how many pages there are, so you know in advance which ones to ask for:

```
GET https://api.example.com/things?page=1
{ "items": [ ... ], "total_pages": 45 }
```

The job is to collect every item from every page. The plan, in the order of this page: write the simplest thing that works, then make it faster, then make it survive a server that pushes back, and then say out loud what you would do if you did not know the number of pages.

### 2. The simplest version: one page at a time

Get page 1, read the count, then loop from page 2 to the end. The whole program is the outline: `main` calls `fetchAll`, and everything else is a small function with one job (`getPage`, `parsePage`, `get`).

<details><summary markdown="span">Execute! (version 1: one page at a time)</summary>

```kotlin
// PagedSerial.kt: read every item from a paged REST API, one page at a time.
//
// GET <base>?page=N returns {"items": [...], "total_pages": 45}.
// Page 1 tells us how many pages there are, so we know in advance what to ask for.
//
// Library: kotlinx-serialization-json. Everything else is the JDK.

val client: HttpClient = HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(5)).build()

data class Page(val items: List<JsonElement>, val totalPages: Int)

class ApiError(message: String) : Exception(message)

fun main() {
    val items = fetchAll("https://api.example.com/things")
    println("got ${items.size} items")
}

// Get page 1 to learn the page count, then get pages 2..total, one after another.
fun fetchAll(baseUrl: String): List<JsonElement> {
    val first = getPage("$baseUrl?page=1")
    val items = mutableListOf<JsonElement>()
    items.addAll(first.items)
    for (n in 2..first.totalPages) {
        val page = getPage("$baseUrl?page=$n")
        items.addAll(page.items)
    }
    return items
}

// One URL in, one parsed Page out.
fun getPage(url: String): Page {
    val body = get(url)
    return parsePage(body)
}

// The shape of the response lives here and nowhere else.
fun parsePage(body: String): Page {
    val root = Json.parseToJsonElement(body).jsonObject
    val items = root["items"]?.jsonArray ?: emptyList()
    val totalPages = root["total_pages"]?.jsonPrimitive?.intOrNull ?: 1
    return Page(items, totalPages)
}

// One request: fail on anything that is not a success.
fun get(url: String): String {
    val request = HttpRequest.newBuilder(URI.create(url))
        .header("Accept", "application/json")
        .timeout(Duration.ofSeconds(10))
        .build()
    val response = client.send(request, HttpResponse.BodyHandlers.ofString())
    if (response.statusCode() !in 200..299) throw ApiError("HTTP ${response.statusCode()} from $url")
    return response.body()
}
```

</details>
<BR>


It reads from the top down. `fetchAll` asks for page 1, adds its items to a list, and then asks for pages 2 to the total, one after another. `getPage` is one URL in and one parsed page out. `parsePage` is the only place that knows the shape of the response. `get` is the only place that touches the network, and for now it fails on anything that is not a success.

### 3. Making it faster: all pages at once

Pages 2 to 45 do not depend on each other, so they can be fetched at the same time. **Only `fetchAll` changes.** Everything else is the same code. The program spends almost all its time waiting on the network, so doing the waits together helps a lot: with at most 8 at once, it is about 8 times faster than 45 separate waits in a row.

<details><summary markdown="span">Execute! (version 2: pages 2 to the end at the same time)</summary>

```kotlin
// PagedParallel.kt: the same program, but pages 2..total are fetched at the same time.
//
// GET <base>?page=N returns {"items": [...], "total_pages": 45}.
// Only fetchAll changed. getPage, parsePage and get are exactly as before.
//
// Libraries: kotlinx-serialization-json and kotlinx-coroutines-core. Everything else is the JDK.

// never more than this many requests at the same time
const val MAX_PARALLEL = 8

val client: HttpClient = HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(5)).build()

data class Page(val items: List<JsonElement>, val totalPages: Int)

class ApiError(message: String) : Exception(message)

fun main() {
    val items = fetchAll("https://api.example.com/things")
    println("got ${items.size} items")
}

// Get page 1 to learn the page count, then start pages 2..total together and wait for all of them.
fun fetchAll(baseUrl: String): List<JsonElement> {
    return runBlocking {
        val first = getPage("$baseUrl?page=1")
        val pool = Dispatchers.IO.limitedParallelism(MAX_PARALLEL)
        val rest = (2..first.totalPages).map { n ->
            async(pool) { getPage("$baseUrl?page=$n") }
        }.awaitAll()
        // awaitAll keeps the order of the list, so the items come back in page order
        first.items + rest.flatMap { it.items }
    }
}

// One URL in, one parsed Page out.
fun getPage(url: String): Page {
    val body = get(url)
    return parsePage(body)
}

// The shape of the response lives here and nowhere else.
fun parsePage(body: String): Page {
    val root = Json.parseToJsonElement(body).jsonObject
    val items = root["items"]?.jsonArray ?: emptyList()
    val totalPages = root["total_pages"]?.jsonPrimitive?.intOrNull ?: 1
    return Page(items, totalPages)
}

// One request: fail on anything that is not a success.
fun get(url: String): String {
    val request = HttpRequest.newBuilder(URI.create(url))
        .header("Accept", "application/json")
        .timeout(Duration.ofSeconds(10))
        .build()
    val response = client.send(request, HttpResponse.BodyHandlers.ofString())
    if (response.statusCode() !in 200..299) throw ApiError("HTTP ${response.statusCode()} from $url")
    return response.body()
}
```

</details>
<BR>


Three lines do the work. `async(pool) { getPage(...) }` starts one fetch as a coroutine, which is a cheap task that can pause while it waits, and returns at once with a promise of the result. The `map` starts one for every page. `.awaitAll()` waits for all of them, and gives the results **in the order of the list**, not in the order they finished, so page 7 finishing before page 3 does not scramble the items. If one fetch throws, the others are cancelled and the error comes out of `awaitAll`, so a failure is never silent. And `Dispatchers.IO.limitedParallelism(MAX_PARALLEL)` is the polite part: at most 8 requests are in flight at once. Without it, 10,000 pages would mean 10,000 requests at the same moment, and the server would throttle you.

### 4. Being throttled

The simple `get` gives up on the first bad answer, which is not good enough for a real service. Here is a replacement. Delete `get`, paste these functions in, and everything else stays the same, in either version.

<details><summary markdown="span">Execute! (a get that retries, waits and gives up properly)</summary>

```kotlin
// GetWithRetries.kt: a drop-in replacement for get() in either version, to survive being throttled.
// Delete the old get(), paste this in, and add these imports:
//   import java.io.IOException
//   import kotlin.random.Random
const val MAX_ATTEMPTS = 5
const val BASE_MILLIS = 500L
const val CAP_MILLIS = 30_000L

enum class Verdict { OK, RETRY, FAIL }

// Retry the failures that can get better, give up on the ones that cannot.
fun get(url: String): String {
    for (attempt in 0 until MAX_ATTEMPTS) {
        // a network error or timeout gives no response at all, so treat it as retryable
        val response = try {
            send(url)
        } catch (e: IOException) {
            null
        }
        if (response != null) {
            val verdict = classify(response.statusCode())
            if (verdict == Verdict.OK) return response.body()
            if (verdict == Verdict.FAIL) throw ApiError("HTTP ${response.statusCode()} from $url")
        }
        Thread.sleep(waitMillis(response, attempt))
    }
    throw ApiError("gave up on $url after $MAX_ATTEMPTS attempts")
}

// The one place that touches the network.
fun send(url: String): HttpResponse<String> {
    val request = HttpRequest.newBuilder(URI.create(url))
        .header("Accept", "application/json")
        .timeout(Duration.ofSeconds(10))
        .build()
    return client.send(request, HttpResponse.BodyHandlers.ofString())
}

// Error codes in one place: success, worth retrying, or hopeless?
fun classify(status: Int): Verdict {
    if (status in 200..299) return Verdict.OK
    if (status == 408 || status == 429) return Verdict.RETRY
    if (status >= 500) return Verdict.RETRY
    // 401, 403, 404, 422... will fail the same way next time
    return Verdict.FAIL
}

// How long to wait: the server's Retry-After if it sent one, otherwise exponential backoff with full jitter.
fun waitMillis(response: HttpResponse<String>?, attempt: Int): Long {
    val retryAfter = response?.headers()?.firstValue("retry-after")?.orElse("")?.toLongOrNull()
    if (retryAfter != null) return retryAfter * 1000
    val ceiling = minOf(CAP_MILLIS, BASE_MILLIS * (1L shl attempt))
    return Random.nextLong(0, ceiling + 1)
}
```

</details>
<BR>


`get` is a loop with three outcomes: return the body, fail now, or wait and try again. Which status means which is decided in one small function, `classify`. A `2xx` is success. A `429` means you are being throttled, and a `5xx` or a `408` means the server is busy or timed out, and none of those are your fault, so wait and retry. A network error or a timeout gives no answer at all, which could be a blip, so retry that too. Anything else, a `400`, `401`, `403`, `404`, means the request itself is wrong and will fail the same way next time, so fail now.

How long to wait is `waitMillis`. If the server sent a `Retry-After`, that is the server saying exactly how long to wait, and it wins. Otherwise the wait is **exponential backoff**: half a second, one, two, four, up to a cap of 30 seconds. And the wait is **random** between zero and that limit, which is called full jitter. When a crowd of clients were all throttled at once, jitter stops them all from coming back at the same instant.

### 5. What if you do not know the page count?

Then it cannot be parallel. Page 2's address only arrives with page 1, so each page has to wait for the one before it. The loop is:

```kotlin
var url: String? = firstUrl
while (url != null) {
    val page = getPage(url)
    items.addAll(page.items)
    url = page.next
}
```

Say so out loud. It shows you understand *why* the known count is what makes parallel possible. If the server points back at a page you already read, this loops forever, so keep a set of the URLs you have seen.

### 6. How it was checked

I compiled and ran all of it, Kotlin 2.0 on Java 21, against a fake server on this machine. Both versions: every item comes back in page order even when later pages answer first, the right number of requests is made, a response with no `total_pages` counts as one page, and a missing page throws an error. The serial version never makes more than one request at a time. The parallel version really overlaps, is faster than one after another, and never goes over 8 at once. The retries: a 503 is retried until it works, a 429 with `Retry-After` waits as told, a 404 is not retried, a server that stays down is tried 5 times and then given up on, and a refused connection gives up. I also broke the code on purpose, with an off-by-one in the loop, scrambled order, no limit, errors ignored, a 404 retried and `Retry-After` ignored, to check that the checks notice. The checks are in the repo next to the code.

To build it, add this to `build.gradle.kts`. The versions are examples, and the parallel version also needs coroutines:

```
implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.3")
implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.8.1")
```

### 7. Edge cases and what to watch for

**Coroutines, threads or `sendAsync`.** A fixed thread pool (`ExecutorService`) does the same job with more code. `HttpClient.sendAsync` returns a `CompletableFuture` and needs no library. Coroutines read the shortest and cancel cleanly.

**How many at once.** Eight is a guess. The right number is what the server tolerates, so start small, watch for `429`, and let `Retry-After` tell you more.

**Memory.** Collecting everything is fine for 45 pages. For millions of items, hand each page to the caller as it arrives instead of holding them all.

**One page fails.** `awaitAll` fails the whole run if one page fails. To keep going, catch the error per page, collect the page numbers that failed, and retry only those. After the attempts run out, fail with a clear error, or report the failed pages.

**Is the order kept?** Yes. `awaitAll` returns the results in the order they were started, so items stay in page order.

**Offsets and cursors.** Page numbers can skip or repeat items if the data changes while you read. Cursor-style APIs avoid that, but they make parallel fetching impossible.

**Testing it.** `parsePage` with plain strings, and the rest against a small fake server. Give the fake server several threads, or it will answer one request at a time and hide the parallelism.

**Caching.** Send `If-None-Match` with the saved ETag. A `304` answer is cheap and does not count against the rate limit.

Sources:

* [Kotlin coroutines: `async` and `awaitAll`](https://kotlinlang.org/docs/composing-suspending-functions.html)
* [MDN: `Retry-After`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Retry-After)
* [MDN: 429 Too Many Requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429)
