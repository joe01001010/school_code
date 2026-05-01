#!/usr/bin/env python


import asyncio
import time


async def make_coffee():
  print("Starting coffee...")
  await asyncio.sleep(3)
  print("Coffee is ready")


async def make_toast():
  print("Starting toast...")
  await asyncio.sleep(2)
  print("Toast is ready")


async def asynced_main():
  start = time.perf_counter()

  await asyncio.gather(make_coffee(), make_toast())

  end = time.perf_counter()

  print(f"Finished getting ready in {time.perf_counter() - start:.2f} seconds")


def make_coffee_normal():
  print("Starting coffee...")
  time.sleep(3)
  print("Coffee is ready")


def make_toast_normal():
  print("Starting toast...")
  time.sleep(2)
  print("Toast is ready")


def main():
  start = time.perf_counter()
  make_coffee_normal()
  make_toast_normal()
  end = time.perf_counter()

  print(f"Finished getting ready in {time.perf_counter() - start:.2f} seconds")


if __name__ == '__main__':
  asyncio.run(asynced_main())

if __name__ == '__main__':
  main()
