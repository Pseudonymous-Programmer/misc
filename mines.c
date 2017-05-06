/* Includes */
#include <time.h>
#include <stdio.h>
#include <stdlib.h>


/* Defines, global variables */
#define bool char
#define TRUE 1
#define FALSE 0
#define is_mine(x,y) minefield[y][x].isMine
#define fail(error) {failmsg = error;goto FAIL;}

typedef struct tile {
	bool isMine,revealed,flagged;
	int neighbors;
} tile;

tile **minefield;

struct {
	enum {STOP, CONTINUE} status;
	int unflaggedMines;
	bool zeroCoords;
	int mines;
	int size;
} state;

/* Utility */
long random_at_most(long max) {
  unsigned long
    num_bins = (unsigned long) max + 1,
    num_rand = (unsigned long) RAND_MAX + 1,
    bin_size = num_rand / num_bins,
    defect   = num_rand % num_bins;
  long x;
  do {
   x = random();
  } while (num_rand - defect <= (unsigned long)x);
  return x/bin_size;
}


/* Logic */

void inc_location(int x,int y) {
	if((x < 0) || (y < 0) || (x > state.size - 1) || (y > state.size - 1)) return;
	if(is_mine(x,y)) return;
	minefield[y][x].neighbors++;
}

void print_board();

void place_mines() {
	int remaining_mines = state.mines;
	while(remaining_mines) {
		int x = random_at_most(state.size-1), y = random_at_most(state.size-1);
		if(is_mine(x,y)) continue;
		minefield[y][x].isMine = TRUE;
		minefield[y][x].neighbors = -1;
		inc_location(x-1,y-1);
		inc_location(x  ,y-1);
		inc_location(x+1,y-1);
		inc_location(x+1,y  );
		inc_location(x+1,y+1);
		inc_location(x  ,y+1);
		inc_location(x-1,y+1);
		inc_location(x-1,y  );
		remaining_mines--;
	}
}

void reset() {
	state.status = CONTINUE;
	state.unflaggedMines = state.mines;
	for(int y = 0;y < state.size;y++) {
		for(int x = 0;x < state.size;x++) {
			minefield[y][x].isMine = FALSE;
			minefield[y][x].revealed = FALSE;
			minefield[y][x].flagged = FALSE;
			minefield[y][x].neighbors = 0;
		}
	}
}

void output(tile t) {
	if(t.flagged) {
		putchar('!');
		return;
	}
	if(!t.revealed) {
		putchar('.');
		return;
	}
	if(t.isMine) {
		putchar('X');
		return;
	}
	if(!t.neighbors) {
		putchar('_');
		return;
	}
	putchar(t.neighbors + '0');
	return;
}

void print_board() {
	for(int y = 0;y < state.size;y++) {
		for(int x = 0; x < state.size; x++) {
			output(minefield[y][x]);
			putchar(' ');
		}
	putchar('\n');
	}
}

void reveal(int x,int y) {
	if((x < 0) || (x > state.size - 1) || (y < 0) || (y > state.size - 1) || minefield[y][x].revealed) return;
	minefield[y][x].revealed = TRUE;
	if(minefield[y][x].isMine) {
		printf("You dug up a mine at (%d,%d). Boom!\n",x+!state.zeroCoords,y+!state.zeroCoords);
		state.status = STOP;
		return;
	}
	if(minefield[y][x].neighbors == 0) { //flood-fill
		reveal(x-1,y-1);
		reveal(x  ,y-1);
		reveal(x+1,y-1);
		reveal(x+1,y  );
		reveal(x+1,y+1);
		reveal(x  ,y+1);
		reveal(x-1,y+1);
		reveal(x-1,y  );
	}
}
void update_board() {
	char c;
	char *failmsg = "Failed to read action";
	printf("Input action (f:toggle flag,r:reveal): ");
	c = getchar();
	if(c == 'f') {
		int x,y;
		printf("X: ");
		if(!scanf("%d",&x)) fail("Failed to read int for x-coordinate");
		printf("Y: ");
		if(!scanf("%d",&y)) fail("Failed to read int for y-coordinate");
		if(!state.zeroCoords) {y--;x--;}
		if((y < 0) || (y > state.size-1) || (x < 0) || (x > state.size-1)) fail("X or Y out of bounds");
		minefield[y][x].flagged = !minefield[y][x].flagged;
		printf("You %s the tile at (%d,%d)!\n",minefield[y][x].flagged ? "flagged" : "deflagged",x+!state.zeroCoords,y+!state.zeroCoords);
		if(minefield[y][x].isMine) state.unflaggedMines--;
		if(!state.unflaggedMines) {
			printf("You flagged all of the mines! You win!\n");
			state.status = STOP;
		}
		while ((c = getchar()) != '\n' && c != EOF); //Flush stdin.
		return;
	}
	if(c == 'r') {
		int x,y;
		printf("X: ");
		if(!scanf("%d",&x)) fail("Failed to read int for x-coordinate");
		printf("Y: ");
		if(!scanf("%d",&y)) fail("Failed to read int for y-coordinate");
		if(!state.zeroCoords) {y--;x--;}
		if((y < 0) || (y > state.size-1) || (x < 0) || (x > state.size-1)) fail("X or Y out of bounds");
		if(minefield[y][x].revealed) fail("You already revealed this tile");
		if(minefield[y][x].flagged) fail("You flagged this tile earlier");
		reveal(x,y);
		while ((c = getchar()) != '\n' && c != EOF); //Flush stdin.
		return;
	}
	FAIL: //Handles user input errors
	printf("You did something wrong: %s\nTry again\n",failmsg);
	while ((c = getchar()) != '\n' && c != EOF); //Flush stdin.
	update_board();
}

void play() {
	reset();
	place_mines();
	while(state.status == CONTINUE) {
		print_board();
		update_board();
	}
}

/*Dynamic memory management*/
void alloc_mines() {
	minefield = (tile**)malloc(sizeof(tile*) * state.size);
	for(int i = 0; i < state.size; i++)
		minefield[i] = (tile*)malloc(sizeof(tile) * state.size);
}

void free_mines() {
	for(int i = 0; i < state.size-1; i++)
		free(minefield[i]);
	free(minefield);
}

/* Main */
int main() {
	printf("Size of board: ");
	scanf("%d",&state.size);
	printf("Number of mines: ");
	scanf("%d",&state.mines);
	alloc_mines();
	state.zeroCoords = TRUE;
	srand(time(NULL));
	char c;
	while ((c = getchar()) != '\n' && c != EOF); //Flush stdin.
	play();
	free_mines();
	return 0;
}
