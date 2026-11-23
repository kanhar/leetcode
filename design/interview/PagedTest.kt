// PagedTest.kt: checks either version against a fake server running on this machine.
// Run with the argument "serial" or "parallel", plus "retry" if get() has been replaced by GetWithRetries.kt.
// Exits with an error if any check fails.
import com.sun.net.httpserver.HttpExchange
import com.sun.net.httpserver.HttpServer
import java.net.InetSocketAddress
import java.util.concurrent.Executors
import java.util.concurrent.atomic.AtomicInteger

var failures = 0

fun check(name: String, ok: Boolean) {
    println((if (ok) "ok    " else "FAIL  ") + name)
    if (!ok) failures++
}

fun reply(exchange: HttpExchange, status: Int, body: String, headers: Map<String, String> = emptyMap()) {
    for ((key, value) in headers) exchange.responseHeaders.add(key, value)
    val bytes = body.toByteArray()
    exchange.sendResponseHeaders(status, bytes.size.toLong())
    exchange.responseBody.use { it.write(bytes) }
}

fun pageNumber(exchange: HttpExchange): Int {
    return exchange.requestURI.query.substringAfter("page=").toInt()
}

fun failsWith(block: () -> Unit): ApiError? {
    return try {
        block()
        null
    } catch (e: ApiError) {
        e
    }
}

fun main(args: Array<String>) {
    val parallel = "parallel" in args
    val retry = "retry" in args
    val server = HttpServer.create(InetSocketAddress("127.0.0.1", 0), 0)
    val base = "http://127.0.0.1:${server.address.port}"
    val requests = AtomicInteger(0)
    val running = AtomicInteger(0)
    val mostRunning = AtomicInteger(0)
    val flakyCalls = AtomicInteger(0)
    val missingCalls = AtomicInteger(0)

    // a server with `pages` pages of two items each; page n holds 2n-1 and 2n.
    // Later pages answer faster than earlier ones, so results arrive out of order.
    fun paged(path: String, pages: Int, delayFor: (Int) -> Long) {
        server.createContext(path) { ex ->
            val n = pageNumber(ex)
            requests.incrementAndGet()
            val now = running.incrementAndGet()
            mostRunning.updateAndGet { maxOf(it, now) }
            Thread.sleep(delayFor(n))
            running.decrementAndGet()
            reply(ex, 200, "{\"items\":[${2 * n - 1},${2 * n}],\"total_pages\":$pages}")
        }
    }
    paged("/six", 6) { n -> (7 - n) * 40L }
    paged("/big", 40) { 50L }
    server.createContext("/one") { ex -> reply(ex, 200, "{\"items\":[1]}") }
    // page 3 is missing
    server.createContext("/broken") { ex ->
        if (pageNumber(ex) == 3) reply(ex, 404, "{}") else reply(ex, 200, "{\"items\":[1],\"total_pages\":5}")
    }
    server.createContext("/missing") { ex ->
        missingCalls.incrementAndGet()
        reply(ex, 404, "{}")
    }
    server.createContext("/flaky") { ex ->
        if (flakyCalls.incrementAndGet() <= 2) reply(ex, 503, "busy") else reply(ex, 200, "{\"items\":[7]}")
    }
    // the default server answers one request at a time, which would hide any parallelism
    server.executor = Executors.newCachedThreadPool()
    server.start()

    // the first request of a run is slow (class loading), so make one that does not count
    fetchAll("$base/one")

    // the basics
    val start = System.currentTimeMillis()
    val items = fetchAll("$base/six")
    val seconds = System.currentTimeMillis() - start
    check("all 12 items come back in page order", items.map { it.toString() } == (1..12).map { it.toString() })
    check("exactly 6 requests were made", requests.get() == 6)
    check("a response with no total_pages is one page", fetchAll("$base/one").size == 1)
    check("a missing page throws ApiError", failsWith { fetchAll("$base/broken") } != null)
    check("parsePage reads the count", parsePage("{\"items\":[],\"total_pages\":45}").totalPages == 45)
    check("parsePage: missing items means empty", parsePage("{}").items.isEmpty())

    // serial or parallel
    if (parallel) {
        check("parallel: pages overlapped", mostRunning.get() > 1)
        // one after another these six pages take 240+200+160+120+80+40 = 840 ms; together about 440 ms
        check("parallel: faster than one after another (took ${seconds}ms)", seconds < 650)
        mostRunning.set(0)
        val big = fetchAll("$base/big")
        check("parallel: 40 pages, 80 items", big.size == 80)
        check("parallel: never more than 8 at once (saw ${mostRunning.get()})", mostRunning.get() <= 8)
        check("parallel: really ran 8 at once", mostRunning.get() == 8)
    } else {
        check("serial: never more than one request at a time", mostRunning.get() == 1)
    }

    // the simple get() fails on the first bad answer; the version with retries is checked in ThrottlingTest.kt
    if (!retry) {
        check("without retries, a 404 throws ApiError", failsWith { get("$base/missing") } != null)
        check("without retries, a 503 throws ApiError", failsWith { get("$base/flaky") } != null)
    }

    server.stop(0)
    if (failures > 0) {
        println("$failures check(s) failed")
        System.exit(1)
    }
    println("all checks passed")
}
