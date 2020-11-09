#!/user/bin/env python3

import itertools


def printb(b): print(f'{b:b}')


def fn(x):
    # get rid of useless zeros
    x = x >> 24

    l = x >> 32
    r = x ^ (l << 32)

    return (l + r)


def count_collisions(keys, fn):
    return len(keys) - len({fn(key) for key in keys})

print(count_collisions(table.keys(), fn))







# out = {}
# for k, v in table.items():
#     out[v] = out.get(v, 0) + 1

# for i in itertools.count(8634610):
#     out = {}
#     for k, v in table.items():
#         new_k = k % i
#         if new_k not in out:
#             out[new_k] = v
#         elif out[new_k] != v:
#             print(i, 'fail')
#             break
#     else:
#         print(i, 'success')
#         exit()

# size = len(table)

# primes = (int(i) for line in open('primes1.txt') for i in line.split())

# for prime in primes:
#     if prime < size:
#         continue

#     out = {}
#     for k in table.keys():
#         to = k % prime
#         out[to] = out.get(to, 0) + 1

#     collisions = {k: v for k, v in out.items() if v > 1}

#     print(prime, 'collisions:', len(collisions))
