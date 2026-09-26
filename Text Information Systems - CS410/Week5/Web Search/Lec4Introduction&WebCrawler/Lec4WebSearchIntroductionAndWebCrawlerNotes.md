# Web Search: One of the most important applications of text retrival
## Challenges in TR web search
- Scalability
Difficult to handle the size of the web as a collection and still ensure completeness of coverage
Tough problem to serve users quickly
- Information/Collection *quality* is quite varied
- The web is dynamic
new pages are constantly creates and some pages are updated very quickly

## Opportunities for improvements in TR for web search
- additional heuristics such as hyperlinks and metadata can be used to improve search accuracy (levereged through Link analysis and multi-feature ranking)
- technologies such as parallel indexing and searching (a MapReduce architecture) used to improve scalability
- technologies such as spam detection and ranking functions that are dialed in help account for low quality information and bad actors

## Basic search engine technologies
- Crawler:   takes the corpus of the web, distilles it down into cached pages "Crawls pages"
- Indexer:   takes the pages out of the cached pages and creates inverted index
- Retriever: The bridge between the inverted index and the user's browser. Intakes the query info and Outputs the Results

### Crawler 
Basic structure needs to:
1. Starts with seed pages in a priority queue 
seed pages are the URLs the crawler has before it fetches anything. Required because the crawler only discovers pages by following links. Should be useful entry points.
2. Fetches pages from web by following those URLs
3. parses those pages for hyperlinks
4. adds those hyperlinks to the queue
5. follows more hyperlinks from the queue

You can run into issues here, some of which you get with any distributed system:
- infra needs to be robust (fault tolerant, resistant to crawler traps, etc.)
- need crawling courtesy (respect the world's load balancing, robot exclusion protocols)
- Need to handle different file types (images, pdfs, etc.)
- Ability to discover hidden URLs and URL extensions
- Understand when pages/URLs are redundant
- It can be difficult to find new pages since they are typically not linked to old pages.

#### Crawling strategies
- Breath-first crawling
Common. Leads to a balanced server load
- Parallel crawling
Natural to parallelize crawling due to the inherent ability to have concurrent crawling processes
- Crawling variations such as focused crawling
Here, a specific subset of pages is crawled (say, all pages ranked to likely be about "automobiles")
Typically decided what is focused via a given query
- Incremental/repeated crawling
Can be resource intense, considerations to reduce resource overhead should be in place.
Should be updated periodically to learn from past experience.
If used, should be targeted at frequently updated or frequently accessed pages. (particularly if you have already crawled everything else before)

