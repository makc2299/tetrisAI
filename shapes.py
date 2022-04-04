# SHAPE FORMATS
 
S = [(['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'], [(1,1),(0,0),(1,-1),(0,-2)], 'S_key_1'),
     (['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....'], [(1,1),(2,0),(-1,1),(0,0)], 'S_key_2')]
 
Z = [(['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'], [(2,0),(0,0),(1,-1),(-1,-1)], 'Z_key_1'),
     (['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....'], [(0,2),(1,1),(0,0),(1,-1)], 'Z_key_2')]
 
I = [(['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'], [(-1,1),(0,0),(1,-1),(2,-2)], 'I_key_1'),
     (['.....',
      '0000.',
      '.....',
      '.....',
      '.....'], [(2,2),(1,1),(0,0),(-1,-1)], 'I_key_2')]
 
O = [(['.....',
      '.....',
      '.00..',
      '.00..',
      '.....'], [(0,0),(0,0),(0,0),(0,0)], 'O_key_1')]
 
J = [(['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'], [(1,1),(0,0),(-2,0),(-1,-1)], 'J_key_1'),
     (['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'], [(0,2),(-1,1),(0,0),(1,-1)], 'J_key_2'),
     (['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'], [(1,1),(2,0),(0,0),(-1,-1)], 'J_key_3'),
     (['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....'], [(0,1),(1,0),(2,-1),(1,-2)], 'J_key_4')]
 
L = [(['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'], [(0,2),(1,1),(0,0),(-1,-1)], 'L_key_1'),
     (['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'], [(2,0),(-1,1),(0,0),(1,-1)], 'L_key_2'),
     (['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'], [(1,1),(0,0),(-1,-1),(0,-2)], 'L_key_3'),
     (['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....'], [(0,1),(1,0),(2,-1),(-1,0)], 'L_key_4')]
 
T = [(['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'], [(1,1),(-1,1),(0,0),(-1,-1)], 'T_key_1'),
     (['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'], [(1,1),(-1,1),(0,0),(1,-1)], 'T_key_2'),
     (['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'], [(1,1),(0,0),(1,-1),(-1,-1)], 'T_key_3'),
     (['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....'], [(0,1),(1,0),(2,-1),(0,-1)], 'T_key_4')]
 
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
