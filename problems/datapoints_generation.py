with open('problemC.dat', 'w') as f:
    f.write('1 100 -10 10 60\n')
    for x in range(60):
        y = x**3 + 5*x**2 + 3*x - 4
        f.write(f'{x} {y}\n')

f.close()
