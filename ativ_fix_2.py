import matplotlib.pyplot as plt
import pandas as pd
import random as r

"""
No pandas a Series e um tipo de dado unidimensional
que representa uma coluna.

E o DataFrame e um tipo de dados bidimensional que
representa uma tabela, que possui Series como suas colunas
"""

rndchar = lambda : chr( 64 + r.randint( 1, 26 ) )
chrarr = lambda x: [ chr( i+65 ) for i in range( x ) ]
space = "+" + ( "-" * 49 ) + "+"

matriz = [[ r.randint( 0, 100000 ) if i % 2 == 0 else rndchar() 
        for i in range( 10 ) ] 
            for _ in range( 5 ) ]

df = pd.DataFrame( matriz, columns=chrarr(10), index=chrarr(5) )

print(space)
print(df)
print(space)
for i in range( len( df.columns ) ):
    if i % 2 != 0: continue
    df.iloc[ :, i ] += 1

print( df.head( 2 ) )
print(space)
print( df.tail( 4 ) )
print(space)

dc = df.to_dict()

print( dc )
print(space)

df.plot(kind='line', marker='o')
plt.show()