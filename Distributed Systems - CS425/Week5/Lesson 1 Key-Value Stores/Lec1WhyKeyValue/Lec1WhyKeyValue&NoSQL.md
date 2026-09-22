# A new generation of storage systems: Key-Value and NoSQL

## Key Value Abstraction
The key-value architecture is a form of abstraction. Assign a key that is easy to work with to some sort fo value
    - key --> value
    - (X) post ID --> information about the post
    - (amazon) item number --> information about that product
    etc.
- Key-Value is a dictionary style data structure (much like a hash table or binary tree) but distributed
    Bc of this, reuses many of the techniques found in distributed hash tables in P2P systems
- Another way to think about this is an off shoot of traditional structural relational database management system with (MySQL is a popular option). Data stored in schema-ed tables. 
    Each row has a PK and quired using SQL.
    Forign keys are used to reference other tables.
    All SQL logic persists here.

### So why not just use a structured relational database?
**Structural relational database schemas are not always the right fit for modern datasets/workloads**
#### reasons:
- datasets can be large and inherently less structured
- workflows require lots of reads and writes (and potentially write heavy)
- foreign keys are rarely needed
- lots of joins
#### what modern workloads need in their databases
- speed
- no single points of failure
- low cost per operation
- less administration
- scalability
##### scale out, not up
- Scale up = growing capacity by replacing your existing machines with more powerful ones (in cloud computing it is common to think about this as adding more compute to a single rack)
- scale out = growing capacity by adding more machines (using components off the shelf) (thought of in cloud computing as adding more racks)
    Scaling out is the main way that companies are achieving scalability. 
    Cheaper. 
    Older machines are generally phased out at EOL
    Easier to manage (especially when comparing to a few highly specialized "scaling up" machines)

### NoSQL = "Not Only SQL"
- Two important API operations: get(key) & put(key, value)
    get returns a value & put updates a value if it already exists. CQL (cassandra query langauge) extends functionality
- Tables
    In cassandra tables are known as "column families" meaning, a group of columns with something in common. In MangoDB, they are called collections, etc. 
    In a NoSQL model, tables are similar to RDBMS tables but start out unstructured and may not have schemas unless that is explicitly set.
        Some columns may be missing, and some may not support joins or have FKs. You can have index tables though.
#### Column-oriented storage
- NoSQL systems store a column together, not a row together like RDBMS systems. 
    Entries in a column are indexed and easy to locate given a key