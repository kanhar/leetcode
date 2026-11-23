// PagedParallel.kt: the same program, but pages 2..total are fetched at the same time.
//
// GET <base>?page=N returns {"items": [...], "total_pages": 45}.
// Only fetchAll changed. getPage, parsePage and get are exactly as before.
//
// Libraries: kotlinx-serialization-json and kotlinx-coroutines-core. Everything else is the JDK.
import java.net.URI
import java.net.http.HttpClient
import java.net.http.HttpRequest
import java.net.http.HttpResponse
import java.time.Duration
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.async
import kotlinx.coroutines.awaitAll
import kotlinx.coroutines.runBlocking
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
import kotlinx.serialization.json.intOrNull
import kotlinx.serialization.json.jsonArray
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive

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
