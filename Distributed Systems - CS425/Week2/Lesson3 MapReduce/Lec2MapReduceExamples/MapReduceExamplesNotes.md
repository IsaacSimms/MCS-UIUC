# Some examples of MapReduce in Action

## Distributed Grep
Grep: A unix tool that searches a text based set of data looking for lines matching a pattern (typically an expression). Prints those lines to a defined location.

    Input:  Large det of text files
    Output: Lines that match the defined pattern

    Map:    emits a line if it matches the provided pattern in a key/value intermediate. The line of text is the key.
    Reduce: Copies the intermediate data to output file/location using the key/value

Let's say you where doing that wordCount example, or looking for a specific error message in a set of logs.
If you are processing 100s of GBs of data, running each task concurrently in a distributed fashion would be much faster then running them sequentially on a single machine.

## Reverse Web-Link Graph
A "web graph" is a directed graph of the web. Nodes = URLs. Edges = hyperlinks. a --> b means a contains a hyperlink to b.
Reverse web-link graph: In a reverse web-link graph, nodes are still URLs. However, the graph has been inverted so that it fans inward instead of outward.
Each node is listed with the nodes that point to it, not the nodes it points to. a --> b means that b contains a hyperlink to a

    Input: A web graph. tubles (a,b).
    Output. A graph. Each page lists pages that link *to* it. 

    Map: processes the web logs provided and creates <key,value>. <source,target> outputs <target,source>
        Note: "target" is the key. Each target is going to end up at the same reduce task.
    Reduce: Outputs <target,list(source)>

## Count URL access frequency
Calculate the percentage that each URL is accessed in a set of logs.
    Input:  Logs of accessed URLs within your domain... likely from proxy server
    Output: For each URL listed, % of total accesses for that URL.

    Map:    Proccess the raw log and output <key,value>... <URL,1> (sorta like wordcount)
    Reduce: Emit <URL, URL_Count>

    Note: So far this is exactly like WordCount. However, you will then **chain together another MapReduce to get %**

    Map:    Proccesses <URL, URL_Count> and output <1, (<URL, URL_COUNT>)>
    Reduce: Sums up the URL_Counts for each URL and calculates overall_count
        The "1" key from the map of this phase causes that URL_COUNT to feed into 1 reducer to calculate the sum, which is what you want, to produce a single value.
            The total is a global is a global number so it must go to the one reducer.

## Sorting
Just by the nature of both the  MapReduce and Hadoop engines, some sorting is already completed. 
Map output is sorted via quicksort
Reduce output is sorted via mergesort

    Map: <key,value> --> <value,_>
    Reduce: <key,value> --> <key,value> (Identity)
    Partioning function: partion the keys across reducers based on ranges.