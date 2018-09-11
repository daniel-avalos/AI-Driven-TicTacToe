# Daniel P. Avalos
# Detailed breakdown of Dr. Jesper Juul's 'All games of Tic Tac Toe'
# source: jesperjuul.dk/tictactoe/allgamesoftictactoe.zip


key1, key2 = '', ''
totals = {'Noughts 5': 0, 'Crosses 5': 0, 'Draw 5': 0,
          'Noughts 6': 0, 'Crosses 6': 0, 'Draw 6': 0,
          'Noughts 7': 0, 'Crosses 7': 0, 'Draw 7': 0,
          'Noughts 8': 0, 'Crosses 8': 0, 'Draw 8': 0,
          'Noughts 9': 0, 'Crosses 9': 0, 'Draw 9': 0,
          'Noughts ': 0, 'Crosses ': 0, 'Draw ': 0, 'total ': 0, }  # To confirm with Juul Numbers
counting = False
filename = 'All games of Tic Tac Toe.txt'
with open(filename) as fp:
    for num, line in enumerate(fp):
        if 'Noughts' in line:
            key1 = 'Noughts '
            counting = True
        elif 'Crosses' in line:
            key1 = 'Crosses '
            counting = True
        elif 'Draw' in line:
            key1 = 'Draw '
            counting = True
        if counting and ('O' or 'X') in line:
            key2 = str(line.count('    '))
            totals[key1] += 1
            totals[key1 + key2] += 1
            totals['total '] += 1
            counting = False
print(totals)

"""Final Totals:
{'Noughts 5': 1440, 'Crosses 5': 0,     'Draw 5': 0, 
'Noughts 6': 0,     'Crosses 6': 5328,  'Draw 6': 0, 
'Noughts 7': 47952, 'Crosses 7': 0,     'Draw 7': 0, 
'Noughts 8': 0,     'Crosses 8': 72576, 'Draw 8': 0, 
'Noughts 9': 81792, 'Crosses 9': 0,     'Draw 9': 46080, 

'Noughts ': 131184, 'Crosses ': 77904,  'Draw ': 46080, 'total ': 255168}
"""