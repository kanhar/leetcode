// ThrottlingTest.kt: checks the get() from GetWithRetries.kt against a fake server running on this machine.
// Exits with an error if any check fails.
import com.sun.net.httpserver.HttpExchange
import com.sun.net.httpserver.HttpServer
import java.net.InetSocketAddress
import java.util.concurrent.atomic.AtomicInteger

var throttleFailures = 0

fun throttleCheck(name: String, ok: Boolean) {
    println((if (ok) "ok    " else "FAIL  ") + name)
    if (!ok) throttleFailures++
}

fun throttleReply(exchange: HttpExchange, status: Int, body: String, headers: Map<String, String> = emptyMap()) {
    for ((key, value) in headers) exchange.responseHeaders.add(key, value)
    val bytes = body.toByteArray()
    exchange.sendResponseHeaders(status, bytes.size.toLong())
    exchange.responseBody.use { it.write(bytes) }
}

fun throttleFails(block: () -> Unit): ApiError? {
    return try {
        block()
        null
    } catch (e: ApiError) {
        e
    }
}

fun main(args: Array<String>) {
    val server = HttpServer.create(InetSocketAddress("127.0.0.1", 0), 0)
    val base = "http://127.0.0.1:${server.address.port}"
    val flakyCalls = AtomicInteger(0)
    val rateCalls = AtomicInteger(0)
    val missingCalls = AtomicInteger(0)
    val deadCalls = AtomicInteger(0)

    // fails twice with 503, then works
    server.createContext("/flaky") { ex ->
        if (flakyCalls.incrementAndGet() <= 2) throttleReply(ex, 503, "busy") else throttleReply(ex, 200, "{\"items\":[7]}")
    }
    // throttled once, with Retry-After: 1
    server.createContext("/rate") { ex ->
        if (rateCalls.incrementAndGet() == 1) throttleReply(ex, 429, "slow down", mapOf("Retry-After" to "1")) else throttleReply(ex, 200, "{\"items\":[8]}")
    }
    // a hopeless request must not be retried
    server.createContext("/missing") { ex ->
        missingCalls.incrementAndGet()
        throttleReply(ex, 404, "{}")
    }
    // always 503: must give up after MAX_ATTEMPTS
    server.createContext("/dead") { ex ->
        deadCalls.incrementAndGet()
        throttleReply(ex, 503, "down", mapOf("Retry-After" to "0"))
    }
    server.start()

    get("$base/flaky")
    throttleCheck("503 is retried until it works (3 calls)", flakyCalls.get() == 3)
    val before = System.currentTimeMillis()
    get("$base/rate")
    val waited = System.currentTimeMillis() - before
    throttleCheck("429 is retried (2 calls)", rateCalls.get() == 2)
    throttleCheck("Retry-After of 1 second is obeyed", waited >= 1000)
    throttleCheck("404 throws ApiError", throttleFails { get("$base/missing") } != null)
    throttleCheck("404 is not retried (1 call)", missingCalls.get() == 1)
    throttleCheck("a server that stays down is tried $MAX_ATTEMPTS times, then ApiError", throttleFails { get("$base/dead") } != null && deadCalls.get() == MAX_ATTEMPTS)
    throttleCheck("connection refused gives up with ApiError", throttleFails { get("http://127.0.0.1:1/x") } != null)
    throttleCheck("classify: 200 and 204 are OK", classify(200) == Verdict.OK && classify(204) == Verdict.OK)
    throttleCheck("classify: 408, 429, 500, 503 retry", listOf(408, 429, 500, 503).all { classify(it) == Verdict.RETRY })
    throttleCheck("classify: 301, 400, 401, 403, 404 fail", listOf(301, 400, 401, 403, 404).all { classify(it) == Verdict.FAIL })
    throttleCheck("waitMillis stays between 0 and the cap", (0..20).all { waitMillis(null, it) in 0..CAP_MILLIS })

    server.stop(0)
    if (throttleFailures > 0) {
        println("$throttleFailures check(s) failed")
        System.exit(1)
    }
    println("all checks passed")
}
