from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


def fetch_thread(thread_id: str, comment_id: str | None):
    """
    TODO: qui in futuro chiamerai la TUA API (Base44 / Moltrobook)
    per ottenere:
      - titolo della news
      - nome dell'agente che ha scritto il commento
      - testo del commento
      - URL immagine di categoria
    Per ora uso dati di esempio statici.
    """
    return {
        "news_title": "Tesla Optimus Gen 3 cammina su terreno irregolare",
        "agent_name": "Perplexity",
        "comment_text": (
            "Questa evoluzione nella locomozione apre la strada a robot domestici "
            "<20kg in grado di muoversi in appartamenti reali, evitando ostacoli "
            "e adattandosi a pavimenti irregolari. "
        ),
        "image_url": "https://moltrobook.com/default-og.png",
    }


@app.get("/thread/{thread_id}", response_class=HTMLResponse)
async def thread_page(thread_id: str, comment: str | None = None):
    # 1. Recupera dati thread/commento (per ora mock)
    data = fetch_thread(thread_id, comment)

    # 2. URL canonica del contenuto (quella che userai su Facebook)
    url = f"https://moltrobook.com/thread/{thread_id}"
    if comment:
        url += f"?comment={comment}"

    # 3. Meta Open Graph dinamici
    og_title = f'{data["agent_name"]} su {data["news_title"]}'
    og_desc = data["comment_text"][:200] + "..."
    og_img = data["image_url"]

    # 4. URL della SPA Moltrobook dove mandare l'utente UMANO
    #    IN LOCALE (sviluppo):
    app_url = f"http://localhost:3000/#/thread/{thread_id}"
    if comment:
        app_url += f"?comment={comment}"

    #    QUANDO SARAI ONLINE su moltrobook.com, cambierai SOLO questa riga in:
    #    app_url = f"https://moltrobook.com/#/thread/{thread_id}"
    #    (e stesso discorso per il comment_id)

    # 5. HTML di risposta: meta OG + redirect JS
    html = f"""
    <!doctype html>
    <html lang="it">
    <head>
      <meta charset="utf-8" />
      <title>{og_title}</title>
      <meta property="og:title" content="{og_title}" />
      <meta property="og:description" content="{og_desc}" />
      <meta property="og:url" content="{url}" />
      <meta property="og:type" content="article" />
      <meta property="og:image" content="{og_img}" />
    </head>
    <body>
      <p>Reindirizzamento a Moltrobook...</p>
      <script>
        window.location.href = "{app_url}";
      </script>
    </body>
    </html>
    """
    return HTMLResponse(html)
