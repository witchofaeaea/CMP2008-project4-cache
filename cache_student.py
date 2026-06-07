class CacheBlock:
    def __init__(self):
        self.valid = False  # True if this cache line holds valid data
        self.tag = 0  # Tag bits of the address stored in this line
        self.lru_counter = 0  # Optional: track recency for replacement (your choice)


class Cache:
    def __init__(self, capacity, block_size, associativity):
        self.capacity = capacity  # Total cache size in bytes (4096 for submission)
        self.block_size = block_size  # Bytes per cache block (must be power of 2)
        self.associativity = associativity  # Ways per set (blocks per set)

        # --- STUDENT IMPLEMENTATION: constructor setup ---
        #
        # sets: number of cache sets
        #   sets = capacity / (block_size * associativity)
        #
        # offset_bits: bits to index a byte within a block
        #   offset_bits = log2(block_size)
        #
        # index_bits: bits to select which set an address maps to
        #   index_bits = log2(sets)
        #
        # directory: 2D list of cache blocks, one row per set
        #   directory[set_index][way_index] -> CacheBlock
        #   len(directory) == sets
        #   len(directory[i]) == associativity for every set i
        #   footprint = sets * associativity * block_size  (must equal 4096 for submission)
        #
        self.sets = 0
        self.offset_bits = 0
        self.index_bits = 0
        self.directory = []
        # --- END STUDENT IMPLEMENTATION ---

    def access(self, address: int) -> bool:
        # --- STUDENT IMPLEMENTATION: cache access ---
        # Split address into tag | index | offset using offset_bits and index_bits.
        # Return True on hit, False on miss (and update directory on miss).
        return False
        # --- END STUDENT IMPLEMENTATION ---


# Create your 4096-byte submission cache here (required for grading):
# submission_cache = Cache(4096, block_size, associativity)
