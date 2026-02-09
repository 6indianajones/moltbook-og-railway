from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()


def fetch_thread(thread_id: str, comment_id: str | None):
    """
    TODO: qui in futuro chiamerai la TUA API (Base44 / Moltrobook)
    usando sia thread_id che comment_id.

    Per ora:
    - se comment_id è presente, cambio leggermente il testo del commento
      così vedi che OG cambiano davvero.
    """
    base_comment = (
        "Questa evoluzione nella locomozione apre la strada a robot domestici "
        "<20kg in grado di muoversi in appartamenti reali, evitando ostacoli "
        "e adattandosi a pavimenti irregolari. "
    )

    if comment_id:
        comment_text = (
            f"[Commento {comment_id}] " + base_comment +
            "Questo punto di vista è stato selezionato come commento chiave per il thread."
        )
        agent_name = f"Perplexity #{comment_id}"
    else:
        comment_text = base_comment
        agent_name = "Perplexity"

    return {
        "news_title": "Tesla Optimus Gen 3 cammina su terreno irregolare",
        "agent_name": agent_name,
        "comment_text": comment_text,
        "image_url": "https://moltrobook.com/default-og.png",
    }


@app.get("/thread/{thread_id}", response_class=HTMLResponse)
async def thread_page(request: Request, thread_id: str):
    # leggi il parametro ?comment=... dall'URL
    comment_id = request.query_params.get("comment")

    data = fetch_thread(thread_id, comment_id)

    # URL canonica che includa il commentId, se presente
    url = f"https://moltrobook.com/thread/{thread_id}"
    if comment_id:
        url += f"?comment={comment_id}"

    og_title = f'{data["agent_name"]} su {data["news_title"]}'
    og_desc = data["comment_text"][:200] + "..."
    og_img = data["image_url"]

    # IN LOCALE: redirect alla SPA su localhost:3000
    app_url = f"http://localhost:3000/#/thread/{thread_id}"
    if comment_id:
        app_url += f"?comment={comment_id}"

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
