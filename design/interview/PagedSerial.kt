// PagedSerial.kt: read every item from a paged REST API, one page at a time.
//
// GET <base>?page=N returns {"items": [...], "total_pages": 45}.
// Page 1 tells us how many pages there are, so we know in advance what to ask for.
//
// Library: kotlinx-serialization-json. Everything else is the JDK.
import java.net.URI
import java.net.http.HttpClient
import java.net.http.HttpRequest
import java.net.http.HttpResponse
import java.time.Duration
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
import kotlinx.serialization.json.intOrNull
import kotlinx.serialization.json.jsonArray
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive

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
