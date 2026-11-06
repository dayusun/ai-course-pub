# A small MCP server with one tool. OpenCode starts it (see opencode-mcp.json) and talks to
# it over stdin and stdout; the agent sees the tool name, the docstring and the arguments.
import json
import urllib.error
import urllib.parse
import urllib.request

from mcp.server.mcpserver import MCPServer  # mcp 2.x; in 1.x this was FastMCP

mcp = MCPServer("crossref")


@mcp.tool()
def lookup_doi(doi: str) -> dict:
    """Look up a DOI in Crossref. Returns title, authors, journal, year, volume and pages,
    or an error if Crossref has no record of the DOI."""
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi.strip())
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            m = json.load(r)["message"]
    except urllib.error.HTTPError as e:
        return {"doi": doi, "error": f"Crossref returned {e.code}", "url": url}
    return {
        "doi": m["DOI"], "url": url,
        "title": (m.get("title") or [""])[0],
        "authors": [a.get("family", "") + " " + a.get("given", "")[:1] for a in m.get("author", [])],
        "journal": (m.get("container-title") or [""])[0],
        "year": m["issued"]["date-parts"][0][0],
        "volume": m.get("volume"), "pages": m.get("page"),
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
