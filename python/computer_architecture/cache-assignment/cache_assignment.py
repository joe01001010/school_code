#!/usr/bin/env python


import random
import statistics

from direct_mapped_cache import DirectMappedCache


def random_addresses(base_address, total_range, element_size, num_accesses):
  """
  This function takes four arguments
  base_address is the starting address in int format
  total_range is the range in Mib expresses as an int
  element_size is the size of the elemnts expressed as an int
  num_accesses is an int that representts the number of times the address was accessed
  This function will yield the start address + when it was accesses times the elemnt size
  """
  half_range = total_range // 2
  start_address = base_address - half_range
  end_address = base_address + half_range

  start_address -= (start_address % half_range)
  end_address -= (base_address % element_size)
  num_elements = (end_address - start_address) // element_size

  for access in range(num_accesses):
    k = random.randrange(num_accesses)
    yield start_address + (k * element_size)


def row_major_addresses(base_addr: int, rows: int, cols: int, elem_size: int):
  for i in range(rows):
    for j in range(cols):
      yield base_addr + ((i * cols) + j) * elem_size


def column_major_addresses(base_addr: int, rows: int, cols: int, elem_size: int):
  for j in range(cols):
    for i in range(rows):
      yield base_addr + ((i * cols) + j) * elem_size


def run_access_pattern(cache, addresses):
  cache.reset()
  for addr in addresses:
    cache.access(addr)
  return {
    "hits": cache.hits,
    "misses": cache.misses,
    "miss_rate": cache.miss_rate()
  }


def run_random_trials(cache, base_address, total_range_bytes, element_size, num_accesses, num_trials):
  """
  This function takes 5 arguments
  cache is the address cache that is being simulated
  base_address is the arbitrary memory address that was created as a string
  total_range_bytes is the simulates range of bytes represented as a string
  element_size is the simulated size of each element represented as an int
  num_accesses is the number of times to access an address, int
  num_trials is the number of trials to simulate as an int
  This function will generate random addresses and output miss statistics
  This function will return a dictionary of the miss statistics
  """
  miss_rates = []
  for trial in range(num_trials):
    cache.reset()
    addresses = random_addresses(base_address, total_range_bytes, element_size, num_accesses)

    for address in addresses:
      cache.access(address)

    miss_rates.append(cache.miss_rate())

  return {
    'avg_miss_rate': statistics.mean(miss_rates),
    'min_miss_rate': min(miss_rates),
    'max_miss_rate': max(miss_rates),
    'stdev_miss_rate': statistics.pstdev(miss_rates),
    'all_miss_rates': miss_rates,
  }


def main():
  results = []
  random_results = []
  base_address = 0x10000000
  cache = DirectMappedCache()
  
  experiments = [
    ('char', 64, 64, 1),
    ('short', 4096, 4096, 2),
    ('int', 32, 32, 4),
    ('long', 2048, 2304, 8),
  ]

  for data_type, rows, columns, element_size, in experiments:
    row_response = run_access_pattern(cache, row_major_addresses(base_address, rows, columns, element_size))
    column_response = run_access_pattern(cache, column_major_addresses(base_address, rows, columns, element_size))

    results.append({
      'type': data_type,
      'rows': rows,
      'columns': columns,
      'element_size': element_size,
      'row_miss_rate': row_response['miss_rate'],
      'column_miss_rate': column_response['miss_rate'],
      'row_hits': row_response['hits'],
      'row_misses': row_response['misses'],
      'columns_hits': column_response['hits'],
      'columns_misses': column_response['misses'],
    })

  print(f"{'Type':<8} {'Rows':>8} {'Cols':>8} {'Row Miss Rate':>15} {'Col Miss Rate':>15}")
  print("-" * 62)
  for r in results:
    print(f"{r['type']:<8} {r['rows']:>8} {r['columns']:>8} "
        f"{r['row_miss_rate']:>15.6f} {r['column_miss_rate']:>15.6f}")

  byte_size = 32 * 1024 * 1024
  num_accesses = 10000
  num_trials = 30
  
  for data_type, rows, columns, element_size in experiments:
    random_experiment = run_random_trials(cache, base_address, byte_size, element_size, num_accesses, num_trials)
    random_results.append({
      'type': data_type,
      'element_size': element_size,
      'avg_miss_rate': random_experiment['avg_miss_rate'],
      'min_miss_rate': random_experiment['min_miss_rate'],
      'max_miss_rate': random_experiment['max_miss_rate'],
      'stdev_miss_rate': random_experiment['stdev_miss_rate'],
    })
  print()
  print('=' * 100)
  print("Random Experiments:")
  print("-" * 100)
  for r in random_results:
    print(f"Type: {r['type']}")
    print(f"Element Size: {r['element_size']}")
    print(f"Average Miss Rate: {r['avg_miss_rate']}")
    print(f"Minimum Miss Rate: {r['min_miss_rate']}")
    print(f"Maximum Miss Rate: {r['max_miss_rate']}")
    print(f"Standard Deviation Miss Rate: {r['stdev_miss_rate']}")
    print("=" * 100)


if __name__ == '__main__':
  main()
