# Lecture: Sensors and Their Networks (Sensor Networks, Lecture A)

Cloud Computing Concepts, Part 2 (Indranil Gupta). CS425 Week 12. Follows Lecture A on Distributed Shared Memory.

## TLDR

A sensor network is a large collection of tiny, battery-powered, failure-prone nodes that sense the environment and send data to a base station. Energy is the binding constraint, and the radio is what drains it, so protocols are built to send as little as possible. The key technique is in-network aggregation: combine readings inside the network instead of forwarding every one.

**Mote:** a tiny sensor node made of a sensor, a microprocessor, a radio, and a battery. **In-network aggregation:** internal nodes of a tree rooted at the base station compute summaries (sum, count, average) of their children's data and send only the summary upward.

## Key sections and what to retain

### 1. What a sensor node is

A sensor node is a very small computer with a sensor and a radio, built to be cheap and left alone for a long time.

- Four parts: sensor, microprocessor, radio, battery.
- The example mote (MICA) has a 4 MHz CPU, a 40 kbps radio, 4 KB of SRAM, and about 7 days of battery at full activity on two AA cells.
- Nodes are deployed in large numbers, often in places that are hard to reach, so they cannot be serviced or recharged.

**Retain:** nodes are extremely limited in CPU, memory, bandwidth, and above all energy.

### 2. Energy budget: computing is cheaper than transmitting

The surprising fact is that thinking costs less battery than talking, which drives the whole design of the network.

- Transmitting on the radio costs about 12 mA. An active CPU costs about 4.6 mA.
- It is **cheaper to compute than to transmit**, so any work done locally that reduces the bytes sent saves battery.
- The radio, not the CPU, drains the battery.

**Retain:** minimize radio use, even at the price of extra local computation.

### 3. Network structure and in-network aggregation

Instead of every node sending its raw reading to the base station, nodes cooperate so that data is combined on the way.

- Nodes form a **tree rooted at the base station**.
- Leaves send readings to their parents. Each internal node combines its children's data with its own using an aggregate such as sum, count, min, max, or average, and sends one summary upward.
- Fewer and smaller messages cross the network, which saves energy and reduces radio contention near the root.
- Aggregates like sum and count combine easily, so the root gets the result without ever seeing the raw readings.

**Builds on:** the compute-versus-transmit asymmetry from section 2. Aggregation is that idea applied to the whole network.

**Retain:** push computation into the network and send summaries up the tree.

### 4. Failures and self-organization

Nodes die, run out of battery, and lose links often, and no one is there to repair them, so the network must manage itself.

- Protocols must be **self-organizing** (build the tree without manual setup) and **self-healing** (rebuild around failed nodes).
- Protocols must **scale in message count**, since every message costs energy at both ends.

**Retain:** with failures this common, fault handling is part of the normal protocol and not a special case.

## Recap

- A mote is a sensor, microprocessor, radio, and battery, with very little CPU, memory, and bandwidth.
- Energy is the main constraint, and the radio is the main consumer: about 12 mA to transmit versus about 4.6 mA for an active CPU.
- Computing locally is cheaper than transmitting, which motivates in-network aggregation.
- Nodes form a tree rooted at the base station, and internal nodes send summaries instead of raw readings.
- Nodes fail often, so protocols must be self-organizing, self-healing, and scalable in message count.
