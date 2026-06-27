class CacheBlock:
    def __init__(self):
        self.valid = False  # True if this cache line holds valid data
        self.tag = 0  # Tag bits of the address stored in this line
        self.lru_counter = 0  # track recency for LRU replacement


class Cache:
    def __init__(self, capacity, block_size, associativity):
        self.capacity = capacity  # Total cache size in bytes (4096 for submission)
        self.block_size = block_size  # Bytes per cache block (must be power of 2)
        self.associativity = associativity  # Ways per set (blocks per set)

        # --- STUDENT IMPLEMENTATION: constructor setup ---
        self.sets = capacity // (block_size * associativity)
        
        # .bit_length() - 1 is a clean way to do log2 for powers of 2 in Python
        self.offset_bits = block_size.bit_length() - 1
        self.index_bits = self.sets.bit_length() - 1

        self.directory = []
        for _ in range(self.sets):
            cache_set = [CacheBlock() for _ in range(self.associativity)]
            self.directory.append(cache_set)
            
        self.access_counter = 0
        # --- END STUDENT IMPLEMENTATION ---

    def access(self, address: int) -> bool:
        # --- STUDENT IMPLEMENTATION: cache access ---
        self.access_counter += 1

        # Extract set index (safely handle 0 index bits for fully associative cases)
        if self.index_bits > 0:
            index_mask = (1 << self.index_bits) - 1
            set_index = (address >> self.offset_bits) & index_mask
        else:
            set_index = 0

        # Extract tag
        tag = address >> (self.offset_bits + self.index_bits)

        cache_set = self.directory[set_index]

        # 1. Check for a HIT
        for block in cache_set:
            if block.valid and block.tag == tag:
                block.lru_counter = self.access_counter
                return True

        # 2. MISS - Look for an empty (invalid) block to fill
        for block in cache_set:
            if not block.valid:
                block.valid = True
                block.tag = tag
                block.lru_counter = self.access_counter
                return False

        # 3. MISS - Evict the Least Recently Used (LRU) block
        lru_block = min(cache_set, key=lambda b: b.lru_counter)
        lru_block.tag = tag
        lru_block.lru_counter = self.access_counter

        return False
        # --- END STUDENT IMPLEMENTATION ---


# Create your 4096-byte submission cache here (required for grading):
# 1024-byte blocks with 2-way associativity perfectly mitigates thrashing 
# in the ping-pong phase while maximizing spatial locality for the matrices.
submission_cache = Cache(4096, 1024, 2)
