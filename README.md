# Google News Monitor - Full Text & Real URLs

Monitor Google News for keywords, site: queries and topics in any country; decoded publisher URLs, optional full text, only-new mode.

[![Run on Apify](https://img.shields.io/badge/Run%20on-Apify-0f9f74)](https://apify.com/datagrit/google-news-rss-monitor) [![Docs](https://img.shields.io/badge/docs-getdatagrit.github.io-0e1726)](https://getdatagrit.github.io/google-news-rss-monitor/)

**from $3.50 per 1,000 results + $10 per run (pay per result; the rate depends on your Apify plan).** Export as JSON, CSV or Excel, call it through the API, or schedule it on Apify.

## What it does

Google News Monitor watches Google News for your keywords, site: searches and topic sections in any country and language, and returns every article as a clean row: headline, source, publication time, the **real publisher URL** decoded from the Google News link and, if you want it, the **full article text**, author and image. Switch on **Only new articles** and schedule it, and each run returns just the articles you have not received yet. It is built for brand and competitor monitoring, PR and media tracking, market news for trading or research, and news feeds for AI agents and n8n, Make or Zapier workflows.

## Quick start

1. Open [Google News Monitor - Full Text & Real URLs on Apify Store](https://apify.com/datagrit/google-news-rss-monitor) and click **Try for free**.
2. Fill in the input form (or paste the JSON below) and run it.
3. Download the dataset, or fetch it from the API.

```json
{
  "queries": [
    "openai",
    "\"electric vehicles\""
  ],
  "editions": [
    "US:en"
  ],
  "timeRange": "1d",
  "maxItems": 20
}
```

## Input

| Field | Type | What it does |
|---|---|---|
| `queries` | array | Google News searches, one per line. Google News operators work: "exact phrase", OR, -exclude, site:reuters.com, intitle:word, when:1d, after:2026-09-01 and before:2026-09-30. Each query is read in every edition below. An article found by several queries or editions is returned once, with all of them in matchedQueries and matchedEditions. Leave empty when you only monitor topics. |
| `topics` | array | Optional Google News sections to monitor in every edition: TOP (top stories), WORLD, NATION, BUSINESS, TECHNOLOGY, ENTERTAINMENT, SPORTS, SCIENCE or HEALTH. Rows from a section have the query topic:NAME, for example topic:TECHNOLOGY. Unknown names are skipped and listed in the run status. |
| `editions` | array | Google News editions to read, as COUNTRY:language codes: US:en, GB:en, IN:en, AU:en, CA:en, CA:fr, DE:de, FR:fr, ES:es, IT:it, NL:nl, PL:pl, JP:ja, BR:pt-419, MX:es-419 and other editions Google News offers. en-US style codes are accepted and UK is read as GB. Each edition is one feed per query, so 3 queries x 2 editions read 6 feeds. Google serves another edition for a pair it does not offer (for example PL:en returns US:en); such an edition is skipped, returns no articles, is not charged and is named in the run status. If none of the editions exists, the run fails. |
| `timeRange` | string | Keep only articles published within this period before the run. The Actor adds the matching when: operator to every query that has no when:, after: or before: of its own, and then checks the publication date of every article again against the time range and the query's own when:, after: and before: (the last two with one day of tolerance), because Google News sometimes returns older articles (on 30 September 2026, 8 of 100 results of site:bbc.co.uk when:1d were from 2011 to 2025). Topic sections are filtered by the same date check. |
| `maxItems` | integer | Most articles to return in one run, newest first, across all queries, topics and editions. One Google News feed holds about 100 articles at most, so this is the practical maximum per query and edition. |
| `onlyNew` | boolean | Return only articles that an earlier run with the same queries, topics, editions and time range has not returned yet. The memory is kept per combination of those settings in your account, so two monitors with different queries never hide each other's articles, and only articles that were actually returned are remembered. Use it with a schedule to get a stream of fresh news. |
| `resolveUrls` | boolean | Google News links point to news.google.com, not to the publisher. When on, the Actor decodes every returned article to its original publisher URL (originalUrl) and checks site: queries against it too. This takes one request per article plus one per 10 articles to Google News (about 1.1 per article), so a run of 100 articles takes one to two minutes longer. Always on when Full text is on. |
| `fullText` | boolean | Open each article on the publisher's site and extract the article text, author, main image and summary (snippet). Plain HTTP, no browser: paywalled and script-rendered pages return partial or no text, which fullTextStatus reports per article. Adds roughly one second per article. |
| `proxyConfiguration` | object | Optional proxy for requests to Google News and publishers. Not needed in normal use. |

## Output

| Field | Type | Description |
|---|---|---|
| `query` | string | The first query or topic (topic:NAME) in your input that found the article. On the single status row (found = false) it lists all queries and topics that were read, comma-separated. |
| `matchedQueries` | array | Every query and topic that found this article, in input order. Duplicates across queries and editions are merged into one row, so this list shows all of them. Empty on the status row. |
| `title` | string | Headline as Google News shows it, without the " - Source" suffix. |
| `sourceName` | string | Publisher name from the Google News feed. |
| `sourceDomain` | string | Domain of the publisher homepage from the feed, without www. |
| `sourceHomepage` | string | Publisher homepage URL from the feed. |
| `publishedAt` | string | Publication time from the feed, ISO 8601 in UTC. |
| `hoursSincePublished` | number | Hours between publication and the start of the run, one decimal. The time range filter is checked against this value. |
| `originalUrl` | string | Publisher URL of the article decoded from the Google News link. Null when decoding is off or failed (see urlStatus). |
| `urlStatus` | string | resolved = originalUrl decoded; failed = Google did not decode this link; notRequested = Decode original article URLs was off. Null only on the status row. |
| `googleNewsUrl` | string | Article link as published in the Google News feed (news.google.com). It redirects to the publisher in a browser. |
| `articleId` | string | Google News article identifier (the guid of the feed item). The same article has the same ID in every edition and query. |
| `snippet` | string | Article summary from the publisher page (structured data description, og:description or meta description). Filled only with Full text on: the Google News feed itself carries no summary, only the headline. |
| `language` | string | Language of the edition in which the article was found first, for example en, de or es-419. |
| `country` | string | Country code of the edition in which the article was found first. |
| `matchedEditions` | array | Every edition (COUNTRY:language) whose feed contained this article. |
| `fullText` | string | Article text extracted from the publisher page (up to 100,000 characters), paragraphs separated by blank lines. Null unless Full text is on and text was found. |
| `fullTextStatus` | string | ok = 500 or more characters extracted; partial = shorter text (paywall teaser, video page or short item); empty = page without readable paragraphs; blocked = publisher answered 401, 402, 403, 429 or 451; failed = other HTTP error or not an HTML page; noUrl = original URL could not be decoded; notRequested = Full text was off. Null only on the status row. |
| `author` | string | Author names from the publisher page, separated by semicolons. Filled only with Full text on. |
| `imageUrl` | string | Main image of the article from the publisher page. Filled only with Full text on. |
| `found` | boolean | True for every article. False only on the single status row written when a run returns no article; its query field and the run status say why. |
| `scrapedAt` | string | ISO 8601 time when the run started reading the feeds. |

Sample record:

```json
{
  "query": "openai",
  "matchedQueries": [
    "openai",
    "topic:TECHNOLOGY"
  ],
  "title": "FTC launches broad investigation into Anthropic, OpenAI",
  "sourceName": "The Washington Post",
  "sourceDomain": "washingtonpost.com",
  "sourceHomepage": "https://www.washingtonpost.com",
  "publishedAt": "2026-09-30T17:44:14.000Z",
  "hoursSincePublished": 0.6,
  "originalUrl": "https://www.washingtonpost.com/technology/2026/09/30/ftc-launches-broad-investigation-into-anthropic-openai/",
  "urlStatus": "resolved",
  "googleNewsUrl": "https://news.google.com/rss/articles/CBMirAFBVV95cUxPNERSOFU3M09XYWNrVTdSdHhkcVl4NkxXeUU2dHItLW41QnJ5TjhOX1VhaUh0Wmc1Y3ZFVm9qeXhfd0gxRVNNclo3UURDbGFrb19KS2RhSWlrbFl1RTZ5V2dlbEN4WXZ0SkwyTy1mRFc4M0lDYVRCZ0lBQnJzZ2xmenA1cDNaX294MzJYVmhydXlBQ1ZQbG40LW9lY1UtQ2MzRmZsdDJ2MWplNVAx?oc=5",
  "articleId": "CBMirAFBVV95cUxPNERSOFU3M09XYWNrVTdSdHhkcVl4NkxXeUU2dHItLW41QnJ5TjhOX1VhaUh0Wmc1Y3ZFVm9qeXhfd0gxRVNNclo3UURDbGFrb19KS2RhSWlrbFl1RTZ5V2dlbEN4WXZ0SkwyTy1mRFc4M0lDYVRCZ0lBQnJzZ2xmenA1cDNaX294MzJYVmhydXlBQ1ZQbG40LW9lY1UtQ2MzRmZsdDJ2MWplNVAx",
  "snippet": "The probe reflects a focus by Trump administration officials on using existing laws to police AI.",
  "language": "en",
  "country": "US",
  "matchedEditions": [
    "US:en",
    "GB:en"
  ],
  "fullText": "The Federal Trade Commission has opened a broad investigation into the safety of artificial intelligence systems made by Anthropic and OpenAI...",
  "fullTextStatus": "ok",
  "author": "Ian Duncan",
  "imageUrl": "https://www.washingtonpost.com/wp-apps/imrs.php?src=https://arc-anglerfish-washpost-prod-washpost.s3.amazonaws.com/public/example.jpg",
  "found": true,
  "scrapedAt": "2026-09-30T18:20:00.000Z"
}
```

## Call it from code

Runnable examples are in [`examples/`](examples). Replace `YOUR_APIFY_TOKEN` with the token from your Apify account settings.

```bash
curl -X POST "https://api.apify.com/v2/acts/datagrit~google-news-rss-monitor/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"queries":["openai","\"electric vehicles\""],"editions":["US:en"],"timeRange":"1d","maxItems":20}'
```


## More from datagrit

- [TED Contract Expiry Radar - Recompete Leads](https://github.com/getdatagrit/ted-contract-expiry-radar) - Find EU public contracts approaching expiry from TED award notices: incumbent, buyer, value, end date and renewal options.
- [UK Contract Expiry Radar - Recompete Leads](https://github.com/getdatagrit/uk-contract-expiry-radar) - UK public contracts ending soon with incumbent supplier, buyer, value and contact - recompete leads from Contracts Finder award notices.
- [French Company Finder - Sirene Financials](https://github.com/getdatagrit/french-company-finder) - French company lead lists from Sirene screened by net result and revenue, with net margin, size, matching establishment and optional directors.
- [GLEIF LEI Lookup - Parents And Subsidiaries](https://github.com/getdatagrit/gleif-lei-ownership-tree) - GLEIF legal entity records with direct and ultimate parents, reporting exceptions and direct subsidiaries.
- [IRS 990 Nonprofit Officers and Compensation](https://github.com/getdatagrit/irs-990-officer-compensation) - Named officers, directors and key employees with pay, hours and titles from IRS e-filed 990, 990-EZ and 990-PF returns.

All Actors: [https://getdatagrit.github.io/](https://getdatagrit.github.io/) · [Apify Store](https://apify.com/datagrit)

---

This repository holds documentation and usage examples. Questions, bug reports and feature requests: use the **Issues** tab of the Actor page on [Apify Store](https://apify.com/datagrit/google-news-rss-monitor). Examples are MIT licensed.
