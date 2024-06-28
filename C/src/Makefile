SRC = wordle_solv
SRC2 = wordle_solv_test
END = solveur

$(END) : $(SRC).o $(SRC2).o
	clang -Wall -Wextra -pedantic -O0 -g3 -fsanitize=address -fno-omit-frame-pointer -fno-optimize-sibling-calls  $(SRC2).o $(SRC).o -o $(END)


$(SRC2).o : $(SRC2).c
	clang -c -Wall -Wextra -pedantic -O0 -g3 -fsanitize=address -fno-omit-frame-pointer -fno-optimize-sibling-calls $(SRC2).c



$(SRC).o : $(SRC).c
	clang -c -Wall -Wextra -pedantic -O0 -g3 -fsanitize=address -fno-omit-frame-pointer -fno-optimize-sibling-calls $(SRC).c
	
	
