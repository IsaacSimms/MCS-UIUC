# File System Abstraction in distributed systems

## Definitions

**File system:** The layer of a distributed file system which organizes persistent data into files and directories. (Data in some sort of heirarchical architecture)

**File system abstractions:** An layer at the OS level which acts as an interface between the program and the file system. Allows programs (and then users and agents downstream of that) to interact with those files and directories. As apposed to interacting with raw disc blocks or blocks in memory.


## Files and directories

- **A file is a header plus data blocks**

Header holds metadata such as:

* Timestamps: creation, read, write, and header change.
* File type, such as `.c` or `.java`.
* Ownership.
* Access Control List (ACL): who may access the file, and in what mode.
* Reference count: the number of directories that contain the file.

A file can also have a *discrptor:* a ticket a process gets when it opens a file. All later operations use the ticket, not the name.

Data blocks are the raw data stream

- **A directory is a collection of those files**

**Folder:** a file whose contents are other files

### Read-write pointer

**Defintion:** a per-open-file offset, stored with the file descriptor, that marks the current position in the file. `read` and `write` start at that position and automatically advance it by the number of bytes transferred. `lseek` is the only call that sets it directly, with an offset that is either absolute or relative to the current pointer. It is hidden state held by the OS, not part of the file.

**Retain:** directory = file whose data is (name → file metadata and pointer) entries.

### File descriptors & open/close

**Defintion of file descriptor:** a handle the process uses to open a file. When the process opens a file the OS creates an internal structure for that data. 

**Definition of open/close:** the tool calls which bracket a process's use of a file. 

**Retain:** the descriptor is state held by the OS on behalf of the process. This matters later because it makes the Unix API stateful.

### Links and attributes

**Definition of link:** an additional name that refers to an existing file, created with `link(old_link, new_link)`

**Definition of attribute:** the metadata stored in the file's header, separate from its contents. These are timestamps (creation, read, write, header), file type, ownership, the access control list (who may access the file and in what mode), and the reference count.


## Recap

* A file system abstracts disk blocks into files and directories.
* File = header (timestamps, type, owner, ACL, reference count) + data blocks.
* Directory = a file that maps names to other files' metadata and pointers.
* Unix access goes through file descriptors, and each descriptor carries an auto-advancing read-write pointer.
* Hard links raise the reference count and a file is deleted only at 0. Symbolic links are independent files that do not affect it.
* `lseek` moves only the pointer. It does not seek the disk.
