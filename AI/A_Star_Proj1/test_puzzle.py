import puzzle

p = puzzle

def test_print_Puzzle():
	x = p.eight_puzzle(0)
	x.puzzle_print()
	print("")
print(""" - Puzzle class printing test -""")
test_print_Puzzle()

def test_puzzle_equal():
	x = p.eight_puzzle(0)
	y = p.eight_puzzle(0)
	print(x==y)
	print("")
print(""" - Puzzle state is equal test -""")
test_puzzle_equal()

def test_calc_mann_dist():
	x = p.eight_puzzle()
	x.data = [[8,1,3],[0,2,4],[7,6,5]]
	x.goal= [[1,2,3],[8,0,4],[7,6,5]]
	print(x.calc_mann_dist(),'\n')

print(""" - Puzzle h1 function calc, showing fval -""")
test_calc_mann_dist()

def test_calc_Nilson():
	x = p.eight_puzzle()
	x.data = [[8,1,3],[0,2,4],[7,6,5]]
	x.goal= [[1,2,3],[8,0,4],[7,6,5]]
	print(x.calc_NSS(),'\n')

print(""" - Puzzle h2 function calc, showing fval -""")
test_calc_Nilson()

def test_calc_avail_moves():
	x = p.eight_puzzle()
	x.data = [[7,1,6],[8,3,5],[2,0,4]]
	print(x.calc_avail_moves(),'\n')

print(""" - Puzzle h2 function calc, showing fval -""")
test_calc_avail_moves()


print(""" - testing main: -""")
def test_main():
	p.main()

test_main()