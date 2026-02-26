# 🧦 Sock Chat

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![AsyncIO](https://img.shields.io/badge/concurrency-asyncio-green)
![Sockets](https://img.shields.io/badge/networking-TCP-orange)
![Architecture](https://img.shields.io/badge/architecture-event--driven-red)
![License](https://img.shields.io/badge/license-educational-lightgrey)

A progressive TCP chat server built in Python demonstrating the evolution of concurrency models — from threads to asynchronous event-driven architecture.

This repository showcases backend engineering fundamentals applied to networking systems.

---

# 📌 Overview

`sock_chat` is a multi-version networking project designed to explore:

* Low-level TCP socket programming
* Client-server architecture
* Thread-based concurrency
* I/O multiplexing with `select`
* Broadcast message systems
* Asynchronous programming with `asyncio`
* Event-loop based architecture

Each version improves scalability and architectural maturity.

---

# 🏗 Architecture Evolution

```
Thread-per-client  →  select() multiplexing  →  broadcast system  →  asyncio event loop
```

---

## 🥇 v1 — Thread-Per-Client Model

**Concurrency:** OS threads
**Model:** Blocking I/O

Flow:

```
accept()
  └── spawn thread
        └── recv() loop
```

✔ Simple
❌ Thread overhead
❌ Limited scalability

---

## 🥈 v2 — I/O Multiplexing with `select()`

**Concurrency:** Single-threaded
**Model:** Manual event loop

Core pattern:

```python
select.select(sockets_list, [], sockets_list)
```

✔ Lower memory usage
✔ Better scalability
✔ Event-driven architecture

---

## 🥉 v3 — Broadcast Implementation

Adds real chat-room behavior.

```python
for client_sock in clients:
    if client_sock != sender:
        client_sock.send(...)
```

✔ Multi-client messaging
✔ Shared communication channel
✔ Foundation for real-time systems

---

## 🏆 v4 — Asyncio-Based Server (Modern Backend Model)

**Concurrency:** Coroutine-based
**Event Loop:** Native asyncio
**Architecture:** Fully non-blocking

Core setup:

```python
server = await asyncio.start_server(handle_client, '127.0.0.1', 8080)
```

### Technical Improvements

* Non-blocking socket handling
* Coroutine scheduling
* Line-based message framing (`readline()`)
* Backpressure control (`await writer.drain()`)
* Graceful connection cleanup
* Native event loop management

This mirrors modern backend systems like:

* Async web servers
* High-performance APIs
* Real-time messaging systems

---

# 📊 Concurrency Comparison

| Version | Model                | Threads | Event Loop | Broadcast | Scalability |
| ------- | -------------------- | ------- | ---------- | --------- | ----------- |
| v1      | Thread-per-client    | ✅       | ❌          | ❌         | Medium      |
| v2      | select()             | ❌       | Manual     | ❌         | Higher      |
| v3      | select() + broadcast | ❌       | Manual     | ✅         | Higher      |
| v4      | asyncio              | ❌       | Native     | ✅         | Very High   |

---

# ▶️ Running the Project

## Requirements

* Python 3.8+

---

## Run v4 (Recommended)

```bash
cd v4
python server.py
```

Expected output:

```
Servidor asyncio iniciado en ('127.0.0.1', 8080)
```

---

## Connect Clients

Using telnet:

```bash
telnet 127.0.0.1 8080
```

Or:

```bash
python client.py
```

Open multiple terminals to simulate concurrent users.

---

# 📡 Example Behavior

Client A sends:

```
Hello
```

Client B receives:

```
('127.0.0.1', 52344) dice: Hello
```

The sender does not receive its own message.

---

# 🧠 Engineering Concepts Demonstrated

* TCP stream communication
* Socket lifecycle management
* Blocking vs non-blocking I/O
* Thread scheduling vs event loop scheduling
* I/O multiplexing
* Async/await patterns
* Broadcast messaging systems
* Resource cleanup & error handling
* Backpressure management

---

# ⚠️ Current Limitations

* No authentication
* No nickname system
* No TLS encryption
* No command parsing
* No persistent storage
* No rate limiting

---

# 🚀 Roadmap (Next Iterations)

* [ ] Nickname handshake system
* [ ] Command parsing (`/quit`, `/list`, `/pm`)
* [ ] TLS support
* [ ] Logging & chat history
* [ ] Benchmark comparison between versions
* [ ] Docker containerization
* [ ] Load testing
* [ ] WebSocket gateway
* [ ] Selector/epoll implementation

---

# 📈 Why This Project Matters

This repository demonstrates progressive backend engineering maturity:

* Understanding concurrency trade-offs
* Migrating from threads to event-driven architecture
* Managing real-time connections
* Designing scalable network services

It is suitable as:

* Networking learning project
* Backend fundamentals showcase
* Systems programming portfolio piece
* Concurrency model comparison study

---

# 📄 License

Educational project. Free to use and modify.
