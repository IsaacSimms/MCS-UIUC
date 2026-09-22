# A new generation of storage systems: Key-Value and NoSQL

## Key Value Abstraction
The key-value architecture is a form of abstraction. Assign a key that is easy to work with to some sort fo value
    - key --> value
    - (X) post ID --> information about the post
    - (amazon) item number --> information about that product
    etc.
- Key-Value is a dictionary style data structure (much like a hash table or binary tree) but distributed
    Bc of this, reuses many of the techniques found in distributed hash tables in P2P systems
- Another way to think about this is a relational database management system with (MySQL is a popular option). Data stored in schema-ed tables. 
    Each row has a PK and quired using SQL
    Forign keys are used to reference other tables