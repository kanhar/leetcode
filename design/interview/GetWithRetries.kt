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
