/**********************************
 * FILE NAME: MP1Node.cpp
 *
 * DESCRIPTION: Membership protocol run by this Node.
 * 				Definition of MP1Node class functions. (Revised 2020)
 *
 *  Starter code template
 **********************************/

#include "MP1Node.h"

/*
 * Note: You can change/add any functions in MP1Node.{h,cpp}
 */

/**
 * Overloaded Constructor of the MP1Node class
 * You can add new members to the class if you think it
 * is necessary for your logic to work
 */
MP1Node::MP1Node( Params *params, EmulNet *emul, Log *log, Address *address) {
	for( int i = 0; i < 6; i++ ) {
		NULLADDR[i] = 0;
	}
	this->memberNode = new Member;
    this->shouldDeleteMember = true;
	memberNode->inited = false;
	this->emulNet = emul;
	this->log = log;
	this->par = params;
	this->memberNode->addr = *address;
}

/**
 * Overloaded Constructor of the MP1Node class
 * You can add new members to the class if you think it
 * is necessary for your logic to work
 */
MP1Node::MP1Node(Member* member, Params *params, EmulNet *emul, Log *log, Address *address) {
    for( int i = 0; i < 6; i++ ) {
        NULLADDR[i] = 0;
    }
    this->memberNode = member;
    this->shouldDeleteMember = false;
    this->emulNet = emul;
    this->log = log;
    this->par = params;
    this->memberNode->addr = *address;
}

/**
 * Destructor of the MP1Node class
 */
MP1Node::~MP1Node() {
    if (shouldDeleteMember) {
        delete this->memberNode;
    }
}

/**
* FUNCTION NAME: recvLoop
*
* DESCRIPTION: This function receives message from the network and pushes into the queue
*                 This function is called by a node to receive messages currently waiting for it
*/
int MP1Node::recvLoop() {
    if ( memberNode->bFailed ) {
    	return false;
    }
    else {
    	return emulNet->ENrecv(&(memberNode->addr), enqueueWrapper, NULL, 1, &(memberNode->mp1q));
    }
}

/**
 * FUNCTION NAME: enqueueWrapper
 *
 * DESCRIPTION: Enqueue the message from Emulnet into the queue
 */
int MP1Node::enqueueWrapper(void *env, char *buff, int size) {
	Queue q;
	return q.enqueue((queue<q_elt> *)env, (void *)buff, size);
}

/**
* FUNCTION NAME: nodeStart
*
* DESCRIPTION: This function bootstraps the node
*                 All initializations routines for a member.
*                 Called by the application layer.
*/
void MP1Node::nodeStart(char *servaddrstr, short servport) {
    Address joinaddr;
    joinaddr = getJoinAddress();

    // Self booting routines
    if( initThisNode(&joinaddr) == -1 ) {
#ifdef DEBUGLOG
        log->LOG(&memberNode->addr, "init_thisnode failed. Exit.");
#endif
        exit(1);
    }

    if( !introduceSelfToGroup(&joinaddr) ) {
        finishUpThisNode();
#ifdef DEBUGLOG
        log->LOG(&memberNode->addr, "Unable to join self to group. Exiting.");
#endif
        exit(1);
    }

    return;
}

/**
 * FUNCTION NAME: initThisNode
 *
 * DESCRIPTION: Find out who I am and start up
 */
int MP1Node::initThisNode(Address *joinaddr) {
    /*
    * This function is partially implemented and may require changes
    */
   // == the id and port of the node for after they are copied out of its address. initialized to zero == //
	int id = 0;
	short port = 0;

	memberNode->bFailed = false;
	memberNode->inited = true;
	memberNode->inGroup = false;
	// node is up!
	memberNode->nnb = 0;
	memberNode->heartbeat = 0;
	memberNode->pingCounter = TFAIL;
	memberNode->timeOutCounter = -1;
	initMemberListTable(memberNode);
	selfIdPort(id, port);
	upsert(id, port, memberNode->heartbeat);

    return 0;
}

/**
 * FUNCTION NAME: introduceSelfToGroup
 *
 * DESCRIPTION: Join the distributed system
 */
int MP1Node::introduceSelfToGroup(Address *joinaddr) {
	MessageHdr *msg;
#ifdef DEBUGLOG
    static char s[1024];
#endif

    if ( 0 == strcmp((char *)&(memberNode->addr.addr), (char *)&(joinaddr->addr))) {
        // I am the group booter (first process to join the group). Boot up the group
#ifdef DEBUGLOG
        log->LOG(&memberNode->addr, "Starting up group...");
#endif
        memberNode->inGroup = true;
    }
    else {
        size_t msgsize = sizeof(MessageHdr) + sizeof(joinaddr->addr) + sizeof(long) + 1;
        msg = (MessageHdr *) malloc(msgsize * sizeof(char));

        // create JOINREQ message: format of data is {struct Address myaddr}
        msg->msgType = JOINREQ;
        memcpy((char *)(msg+1), &memberNode->addr.addr, sizeof(memberNode->addr.addr));
        memcpy((char *)(msg+1) + 1 + sizeof(memberNode->addr.addr), &memberNode->heartbeat, sizeof(long));

#ifdef DEBUGLOG
        sprintf(s, "Trying to join...");
        log->LOG(&memberNode->addr, s);
#endif

        // send JOINREQ message to introducer member
        emulNet->ENsend(&memberNode->addr, joinaddr, (char *)msg, msgsize);

        free(msg);
    }

    return 1;

}

/**
* FUNCTION NAME: finishUpThisNode
*
* DESCRIPTION: Wind up this node and clean up state
*/
int MP1Node::finishUpThisNode(){
    return 0; // int signature must return a value; Application::run ignores it
}

/**
* FUNCTION NAME: nodeLoop
*
* DESCRIPTION: Executed periodically at each member
*                 Check your messages in queue and perform membership protocol duties
*/
void MP1Node::nodeLoop() {
    if (memberNode->bFailed) {
    	return;
    }

    // Check my messages
    checkMessages();

    // Wait until you're in the group...
    if( !memberNode->inGroup ) {
    	return;
    }

    // ...then jump in and share your responsibilities!
    nodeLoopOps();

    return;
}

/**
 * FUNCTION NAME: checkMessages
 *
 * DESCRIPTION: Check messages in the queue and call the respective message handler
 */
void MP1Node::checkMessages() {
    void *ptr;
    int size;

    // Pop waiting messages from memberNode's mp1q
    while ( !memberNode->mp1q.empty() ) {
    	ptr = memberNode->mp1q.front().elt;
    	size = memberNode->mp1q.front().size;
    	memberNode->mp1q.pop();
    	recvCallBack((void *)memberNode, (char *)ptr, size);
    }
    return;
}

/**
 * FUNCTION NAME: recvCallBack
 *
 * DESCRIPTION: Message handler for different message types
 */
bool MP1Node::recvCallBack(void *env, char *data, int size ) {
	if (data == NULL || size < (int)sizeof(MessageHdr)) {
		free(data);
		return true;
	}

	MessageHdr *msg = (MessageHdr *)data;
	switch (msg->msgType) {
		case JOINREQ:                   // peer asking introducer to add
			handleJoinReq(data, size);
			break;
		case JOINREP:                   // join introducer's list (handler sets 'inGroup')
			handleJoinRep(data, size);
			break;
		case GOSSIP:                    // membership list from node already in group
			handleGossip(data, size);
			break;
		default:
			break;
	}

	free(data);
	return true;
}

/**
* FUNCTION NAME: nodeLoopOps
*
* DESCRIPTION: Check if any node hasn't responded within a timeout period and then delete
*                 the nodes
*                 Propagate your membership list
*/
void MP1Node::nodeLoopOps() {
	int id = 0;
	short port = 0;
	int now = par->getcurrtime();

	memberNode->heartbeat++; // the node's own pulse increment for that round
	selfIdPort(id, port);
	upsert(id, port, memberNode->heartbeat);

	for (vector<MemberListEntry>::iterator it = memberNode->memberList.begin(); it != memberNode->memberList.end(); ) {
		int memberId = it->getid();
		short memberPort = it->getport();
		long age = (long)now - it->gettimestamp(); // how many rounds have passed since a row's last heartbeat

        // run if row is other member and age is greater then 20
		if (!isSelf(memberId, memberPort) && age > TREMOVE) { 
			// Log this pair once. The insert blocks a second removal line.
			if (removed.find(make_pair(memberId, memberPort)) == removed.end()) {
				Address removedAddr = makeAddress(memberId, memberPort);
				log->logNodeRemove(&memberNode->addr, &removedAddr);
				removed.insert(make_pair(memberId, memberPort));
			}
			it = memberNode->memberList.erase(it);
		}
		else {
			++it; // advance to next row
		}
	}

	// Send the remaining list to every other member. Rows older than TFAIL and still
	// within TREMOVE stay included and still receive a copy.
	for (vector<MemberListEntry>::iterator it = memberNode->memberList.begin(); it != memberNode->memberList.end(); ++it) {
		if (isSelf(it->getid(), it->getport())) {
			continue;
		}
		Address dest = makeAddress(it->getid(), it->getport());
		sendList(GOSSIP, &dest);
	}

    return;
}

/**
 * FUNCTION NAME: selfIdPort
 *
 * DESCRIPTION: Read this node's id and port from its address bytes
 */
void MP1Node::selfIdPort(int &id, short &port) {
	memcpy(&id, memberNode->addr.addr, sizeof(int));
	memcpy(&port, memberNode->addr.addr + 4, sizeof(short));
}

/**
 * FUNCTION NAME: makeAddress
 *
 * DESCRIPTION: Build an Address from an id and port
 */
Address MP1Node::makeAddress(int id, short port) {
	Address addr;
	memcpy(&addr.addr[0], &id, sizeof(int));
	memcpy(&addr.addr[4], &port, sizeof(short));
	return addr;
}

/**
 * FUNCTION NAME: isSelf
 *
 * DESCRIPTION: True when id and port name this node
 */
bool MP1Node::isSelf(int id, short port) {
	int selfId = 0;
	short selfPort = 0;
	selfIdPort(selfId, selfPort);
	return id == selfId && port == selfPort;
}

/**
 * FUNCTION NAME: upsert
 *
 * DESCRIPTION: Insert a member, or replace its heartbeat when the new one is strictly greater
 */
void MP1Node::upsert(int id, short port, long heartbeat) {
	// A deleted id stays out. Reinserting it produces a second removal line.
	if (removed.find(make_pair(id, port)) != removed.end()) {
		return;
	}

	for (vector<MemberListEntry>::iterator it = memberNode->memberList.begin(); it != memberNode->memberList.end(); ++it) {
		if (it->getid() == id && it->getport() == port) {
			// An equal heartbeat leaves the timestamp in place, so a dead row can age past TREMOVE.
			if (heartbeat > it->getheartbeat()) {
				it->setheartbeat(heartbeat);
				it->settimestamp(par->getcurrtime());
			}
			return;
		}
	}

	memberNode->memberList.push_back(MemberListEntry(id, port, heartbeat, par->getcurrtime()));
	Address added = makeAddress(id, port);
	log->logNodeAdd(&memberNode->addr, &added);
}

/**
 * FUNCTION NAME: sendList
 *
 * DESCRIPTION: Send this node's current membership list to dest
 */
void MP1Node::sendList(MsgTypes msgType, Address *dest) {
	int count = (int)memberNode->memberList.size();
	int entrySize = (int)(sizeof(int) + sizeof(short) + sizeof(long));
	int msgsize = (int)sizeof(MessageHdr) + (int)sizeof(int) + count * entrySize;
	char *buf = (char *)malloc(msgsize);
	char *cursor;

	if (buf == NULL) {
		return;
	}

	cursor = buf + sizeof(MessageHdr) + sizeof(int);

	((MessageHdr *)buf)->msgType = msgType;
	memcpy(buf + sizeof(MessageHdr), &count, sizeof(int));

	for (vector<MemberListEntry>::iterator it = memberNode->memberList.begin(); it != memberNode->memberList.end(); ++it) {
		int id = it->getid();
		short port = it->getport();
		long heartbeat = it->getheartbeat();
		memcpy(cursor, &id, sizeof(int));
		cursor += sizeof(int);
		memcpy(cursor, &port, sizeof(short));
		cursor += sizeof(short);
		memcpy(cursor, &heartbeat, sizeof(long));
		cursor += sizeof(long);
	}

	emulNet->ENsend(&memberNode->addr, dest, buf, msgsize);
	free(buf);
}

/**
 * FUNCTION NAME: applyMembership
 *
 * DESCRIPTION: Upsert each id, port, and heartbeat packed after the message header
 */
void MP1Node::applyMembership(char *data, int size) {
	int header = (int)sizeof(MessageHdr) + (int)sizeof(int);
	int entrySize = (int)(sizeof(int) + sizeof(short) + sizeof(long));
	int count = 0;
	char *cursor;

	if (size < header || entrySize <= 0) {
		return;
	}

	memcpy(&count, data + sizeof(MessageHdr), sizeof(int));
	if (count < 0 || count > (size - header) / entrySize) {
		return;
	}

	cursor = data + header;
	for (int i = 0; i < count; i++) {
		int id = 0;
		short port = 0;
		long heartbeat = 0;
		memcpy(&id, cursor, sizeof(int));
		cursor += sizeof(int);
		memcpy(&port, cursor, sizeof(short));
		cursor += sizeof(short);
		memcpy(&heartbeat, cursor, sizeof(long));
		cursor += sizeof(long);
		upsert(id, port, heartbeat);
	}
}

/**
 * FUNCTION NAME: handleJoinReq
 *
 * DESCRIPTION: Add the joining member and reply with the current list
 */
void MP1Node::handleJoinReq(char *data, int size) {
	int minSize = (int)sizeof(MessageHdr) + 6 + 1 + (int)sizeof(long);
	int id = 0;
	short port = 0;
	long heartbeat = 0;
	Address dest;

	if (size < minSize) {
		return;
	}

	memcpy(&id, data + sizeof(MessageHdr), sizeof(int));
	memcpy(&port, data + sizeof(MessageHdr) + sizeof(int), sizeof(short));
	// Address is 6 bytes, then one unused byte, then the heartbeat.
	memcpy(&heartbeat, data + sizeof(MessageHdr) + 6 + 1, sizeof(long));
	upsert(id, port, heartbeat);
	dest = makeAddress(id, port);
	sendList(JOINREP, &dest);
}

/**
 * FUNCTION NAME: handleJoinRep
 *
 * DESCRIPTION: Enter the group and merge the introducer's membership list
 */
void MP1Node::handleJoinRep(char *data, int size) {
	memberNode->inGroup = true;
	applyMembership(data, size);
}

/**
 * FUNCTION NAME: handleGossip
 *
 * DESCRIPTION: Merge a gossiped membership list
 */
void MP1Node::handleGossip(char *data, int size) {
	applyMembership(data, size);
}

/**
 * FUNCTION NAME: isNullAddress
 *
 * DESCRIPTION: Function checks if the address is NULL
 */
int MP1Node::isNullAddress(Address *addr) {
	return (memcmp(addr->addr, NULLADDR, 6) == 0 ? 1 : 0);
}

/**
 * FUNCTION NAME: getJoinAddress
 *
 * DESCRIPTION: Returns the Address of the coordinator
 */
Address MP1Node::getJoinAddress() {
    Address joinaddr;

    *(int *)(&joinaddr.addr) = 1;
    *(short *)(&joinaddr.addr[4]) = 0;

    return joinaddr;
}

/**
 * FUNCTION NAME: initMemberListTable
 *
 * DESCRIPTION: Initialize the membership list
 */
void MP1Node::initMemberListTable(Member *memberNode) {
	memberNode->memberList.clear();
}

/**
 * FUNCTION NAME: printAddress
 *
 * DESCRIPTION: Print the Address
 */
void MP1Node::printAddress(Address *addr)
{
    printf("%d.%d.%d.%d:%d \n",  addr->addr[0],addr->addr[1],addr->addr[2],
                                                       addr->addr[3], *(short*)&addr->addr[4]) ;    
}
