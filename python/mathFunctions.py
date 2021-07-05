def clamp(n, smallest, largest):
  return max(smallest, min(n, largest))

def inverse_lerp(a, b, value):
    if a != b:
        return clamp((value - a) / (b - a), 0, 1)
    return 0

def lerp(a, b, t):
  return a + (b - a) * clamp(t, 0, 1)
