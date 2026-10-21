# Architecture

The backend exposes a FastAPI API and stores each adaptation in SQLite. It uses OpenAI when `OPENAI_API_KEY` is set. Without a key, local rules split the source into short clauses and keep each sentence on its own line.

The Spanish INFLESZ implementation scores the source and adapted text. ARASAAC results are looked up for selected content words, cached in memory for 15 minutes, and attached to each sentence. A lookup timeout or API error returns an empty pictogram list.

The React application sends text or uploaded files to the API. It can show the result, readability scores, pictograms, saved history, and print layout. The shared request and response shape is documented in [api-contract.md](api-contract.md).

PDF and text uploads are limited to 5 MB. Extracted text and JSON input are limited to 20,000 characters.
