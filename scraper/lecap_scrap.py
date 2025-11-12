#!/usr/bin/env python3
"""Pequeño scraper para comprobar el funcionamiento del contenedor scraper.

Extrae información de https://www.acuantoesta.com.ar/lecaps usando Playwright
para renderizar la página (sitio dinámico) y BeautifulSoup para parsear el HTML.

Guarda el resultado en `scraper/scrap_data/lecaps.csv`.
"""
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import os
import sys
import time
import logging


def scrape_lecaps(output_dir: str = "scrap_data") -> int:
    url = "https://www.acuantoesta.com.ar/lecaps"
    logging.info(f"Navegando a {url} ...")
    #!/usr/bin/env python3
    """Minimal scraper you can run quickly.

    Fetches https://www.acuantoesta.com.ar/lecaps with requests and extracts
    some visible text into a small CSV. This is intentionally simple and may
    miss data rendered only by JavaScript (it's not using Playwright).
    """
    import requests
    from bs4 import BeautifulSoup
    import csv
    import os
    import sys
    import logging
    from playwright.sync_api import sync_playwright


    URL = "https://www.acuantoesta.com.ar/lecaps"


    def simple_scrape(output_dir: str = "scrap_data") -> int:
        logging.info(f"Using Playwright to render {URL}")
        rows = []
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(URL, wait_until="networkidle", timeout=30000)
                # wait for either a table or some content
                try:
                    page.wait_for_selector("table, .card, .lecaps-list, .lecaps-item", timeout=10000)
                except Exception:
                    pass
                html = page.content()
                browser.close()
        except Exception as e:
            logging.error(f"Playwright error: {e}")
            return 4

        soup = BeautifulSoup(html, "lxml")
        table = soup.find("table")
        if table:
            for tr in table.find_all("tr"):
                cols = [td.get_text(strip=True) for td in tr.find_all(["th", "td"])]
                if cols:
                    rows.append(cols)
        else:
            items = soup.select(".card, .list, .item, .lecaps-list, .lecaps-item, li")
            for it in items[:500]:
                text = it.get_text(" ", strip=True)
                if text:
                    rows.append([text])

        if not rows:
            title = soup.title.string.strip() if soup.title else "no-title"
            rows = [[title]]

        os.makedirs(output_dir, exist_ok=True)
        outpath = os.path.join(output_dir, "lecaps.csv")
        with open(outpath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for r in rows:
                writer.writerow(r)

        logging.info(f"Wrote {len(rows)} rows to {outpath}")
        return 0


    if __name__ == "__main__":
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
        sys.exit(simple_scrape())
