import board

def get_board_pin(button_number):
  switcher = {
    2: board.D2,
    3: board.D3,
    4: board.D4,
    5: board.D5,
    6: board.D6,
    7: board.D7,
    8: board.D8,
    9: board.D9,
    11: board.D11,
    13: board.D13,
    14: board.D14,
    15: board.D15,
    17: board.D17,
    18: board.D18,
    19: board.D19,
    20: board.D20,
    21: board.D21,
    22: board.D22,
    23: board.D23,
    24: board.D24,
    25: board.D25,
    26: board.D26,
    27: board.D27,
  }
  
  return switcher.get(button_number, 'Invalid Board Pin')
