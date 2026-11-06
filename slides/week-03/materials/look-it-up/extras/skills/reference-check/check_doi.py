"""Print the Crossref record for a DOI: python3 check_doi.py <doi>"""
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

doi = sys.argv[1].strip()
url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
try:
    with urllib.request.urlopen(url, timeout=30) as r:
        m = json.load(r)["message"]
except urllib.error.HTTPError as e:
    print(f"NOT FOUND (Crossref {e.code}): {url}")
    sys.exit(1)
print(f"url: {url}")
print(f"title: {(m.get('title') or [''])[0]}")
print(f"authors: {', '.join(a.get('family', '') + ' ' + a.get('given', '')[:1] for a in m.get('author', []))}")
print(f"journal: {(m.get('container-title') or [''])[0]}")
print(f"year: {m['issued']['date-parts'][0][0]}")
print(f"volume: {m.get('volume')}  issue: {m.get('issue')}  pages: {m.get('page')}")
