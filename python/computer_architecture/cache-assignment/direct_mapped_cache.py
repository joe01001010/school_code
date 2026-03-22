from dataclasses import dataclass


class DirectMappedCache:
  def __init__(self, cache_size_bytes=4096, block_size_bytes=64):
    """
    This is the constructor for the DirectMappedCache class
    This constructor takes two optional argument
    cache_size_bytes is the simulated byte size of the cache as an int. Will default to 4096
    block_size_bytes is the simulated block size of the cache as an in. Will default to 64
    This will returnb the DirectMappedCache object
    """
    self.cache_size = cache_size_bytes
    self.block_size = block_size_bytes
    self.num_lines = cache_size_bytes // block_size_bytes
    self.lines = [CacheLine() for _ in range(self.num_lines)]

    self.hits = 0
    self.misses = 0

  def access(self, address):
    """
    This method will take one argument
    address is the address to check in the block and for index and tag
    This function will check it the address is a hit and return true or it will return false
    This function returns a boolean value
    """
    block_number = address // self.block_size
    index = block_number % self.num_lines
    tag = block_number // self.num_lines

    line = self.lines[index]

    if line.valid and line.tag == tag:
      self.hits += 1
      return True
    else:
      self.misses += 1
      line.valid = True
      line.tag = tag
      return False

  def miss_rate(self):
    """
    This function takes no arguments
    This function will calculate the total number of attempts
    Then this function will return a float of the miss rate
    """
    total = self.hits + self.misses
    return self.misses / total if total else 0.0

  def reset(self):
    """
    This function takes no arguments
    This function will reset the class's lines
    This function doesnt return anything
    """
    self.lines = [CacheLine() for _ in range(self.num_lines)]
    self.hits = 0
    self.misses = 0


@dataclass
class CacheLine:
  """
  This class has no contructor, it will simulate a datatype as the cacheline
  """
  valid: bool = False
  tag: int = -1
