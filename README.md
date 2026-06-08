[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/eUGdPF-i)
[![Work in MakeCode](https://classroom.github.com/assets/work-in-make-code-8824cc13a1a3f34ffcd245c82f0ae96fdae6b7d554b6539aec3a03a70825519c.svg)](https://classroom.github.com/online_ide?assignment_repo_id=24099118&assignment_repo_type=AssignmentRepo)
# Project 4: Cache Performance Simulator

## Overview

Implement a set-associative cache simulator in `cache_student.py` and tune your cache design under a fixed 4096-byte hardware budget. Submit only `cache_student.py`. Do not modify `config.py`.

Run the autograder to see your score:

```bash
python3 autograder.py
```

### Testing your work

| Command | When to use |
|---------|-------------|
| `python3 autograder.py` | Primary — validation, latency banner, score |
| `python3 -m unittest test_cache.py -v` | After `submission_cache` exists — constructor + benchmark checks |
| `python3 trace_reader.py traces/benchmark.txt` | Quick stats without a score |

The starter template has no `submission_cache`, so the autograder reports **0/100** and unit tests skip submission checks until you add one. The constructor unit test also fails until you implement `__init__`.

### Repository layout

```
cache_student.py      ← your implementation (only file you submit)
config.py             ← fixed hardware constants (do not modify)
autograder.py         ← grading script
trace_reader.py       ← local simulator
test_cache.py         ← optional unit tests
traces/benchmark.txt  ← practice trace
```

---

## Your submission design

Do **not** declare `BLOCK_SIZE` or `ASSOCIATIVITY` as module-level constants. Your design lives in the **built cache**:

- `self.block_size` and `self.associativity` are member variables set in your constructor
- `self.directory` must be a 2D list sized to your design
- At the bottom of `cache_student.py`, create your 4096-byte submission instance:

```python
submission_cache = Cache(4096, block_size, associativity)
```

The autograder **imports** `submission_cache` and reads your design from the built object:

```
block_size    = submission_cache.block_size
associativity = len(submission_cache.directory[0])
sets          = len(submission_cache.directory)
footprint     = sets × associativity × block_size   # must equal 4096
```

`cache.associativity`, `cache.sets`, and the directory structure must all be **consistent**. Any mismatch or invalid footprint scores **0**.

The starter template does not include `submission_cache` and scores **0/100** until you add a working implementation.

---

## Address bit fields

The simulator treats each trace address as a **32-bit** value and splits it into three fields:

```
|        tag        |   index   |  offset  |
```

| Field | Size | How to compute |
|-------|------|----------------|
| **offset** | `offset_bits = log2(block_size)` | Selects the byte within a cache block |
| **index** | `index_bits = log2(sets)` | Selects the cache set |
| **tag** | remaining high bits | Identifies which memory block is stored |

Where:

```
sets = CACHE_CAPACITY / (block_size × associativity)
```

**Example** with `block_size = 16` and `associativity = 1`:

| Field | Bits | Calculation |
|-------|------|-------------|
| offset | 4 | log2(16) |
| index | 8 | log2(256 sets) |
| tag | 20 | 32 − 4 − 8 |

Address `0x1000` with that configuration:

- offset = `0x1000 & 0xF` = `0x0`
- index = `(0x1000 >> 4) & 0xFF` = `0x100`
- tag = `0x1000 >> 12` = `0x1`

Your `offset_bits` and `index_bits` must be computed from the constructor parameters passed in. The unit test `test_constructor_calculations` checks this with `Cache(8192, 64, 4)` — independent of your `submission_cache` design.

---

## Latency model

The autograder and `trace_reader.py` print a prominent **HIT LATENCY** banner before performance results.

Costs are derived from your **built cache**, not from declared constants:

| Cost | Formula | Meaning |
|------|---------|---------|
| **Hit latency** | `1 + (associativity − 1)` | 1 base cycle plus 1 cycle per serial tag comparison in the set |
| **Miss latency** | `200` | Main memory access (`MISS_PENALTY` in `config.py`) |

**Example:** a 2-way set-associative cache has hit latency **2 cycles** (1 base + 1 tag compare).

| Metric | Formula |
|--------|---------|
| Hit Rate | `(hits / total_accesses) × 100` |
| Total Cycles | `hits × hit_latency + misses × 200` |
| AMAT | `total_cycles / total_accesses` |

**Main-memory baseline:** if every access misses, total cycles = `accesses × 200`. Your cache must beat this baseline to earn any points.

---

## Benchmark trace (`traces/benchmark.txt`)

The trace is a text file of **32-bit memory addresses**, one per line, written as **8-digit hexadecimal** (e.g. `10000010` = `0x10000010`). The simulator reads each line, calls `submission_cache.access(address)`, and records a hit or miss.

The benchmark contains **112 accesses** modelling a short program run:

| Phase | Address region | Behaviour |
|-------|----------------|-----------|
| Data init | `0x10000000` | Sequential 16-byte stride — array setup |
| Hot loop | `0x10000000` | Same 4 lines revisited — temporal locality |
| Stack frame | `0x7FFFFC00` | Local variables — stack access |
| Heap walk | `0x20000000` | Pointer chase with large gaps — poor spatial locality |
| Matrix row | `0x30000000` | 4-byte stride along a row |
| Matrix column | `0x30000000` | 256-byte stride down a column — conflict pressure |
| Ping-pong | `0x40000000` / `0x40010000` | Alternating distant arrays — set conflicts |
| Code hot spot | `0x00401200` | Repeated instruction fetch |
| Library call | `0x7F000800` | Jump to shared library region |

Any replacement policy (LRU, FIFO, etc.) is acceptable.

---

## Scoring (100 points)

Your score is based entirely on **benchmark performance tiers**. There is no partial credit for an empty template or invalid footprint.

### Entry requirement (20 points)

Earn **20 points** when **all** of the following hold:

1. `submission_cache` exists with a valid 4096-byte footprint
2. `cache.associativity`, `cache.sets`, and `directory` are consistent
3. Benchmark `total_cycles` is **strictly below** `accesses × 200`

### Higher tiers (+10 points each)

Better performance earns higher scores. You receive the **highest tier** you qualify for (not a cumulative sum).

| Score | Tier | Max Total Cycles |
|-------|------|------------------|
| 20 | Base | < 22400 (beats main-memory baseline) |
| 30 | Tier 1 | ≤ 11000 |
| 40 | Tier 2 | ≤ 9500 |
| 50 | Tier 3 | ≤ 8500 |
| 60 | Tier 4 | ≤ 7500 |
| 70 | Tier 5 | ≤ 6500 |
| 80 | Tier 6 | ≤ 5500 |
| 90 | Tier 7 | ≤ 4500 |
| 100 | Tier 8 | ≤ 3400 |

A working cache with a weak design can earn **20–30/100**. Tuning `block_size` and `associativity` in your `submission_cache` for stronger locality can bring the total to **100/100**.

---

## Submission

Submit **only** `cache_student.py` with a working `submission_cache` instance. Do not modify any other project files.
