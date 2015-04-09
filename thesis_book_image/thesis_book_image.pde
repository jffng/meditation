PImage img;
int[][] old_board, new_board;
int cellsize = 30;
int cellwidth = 30;
int COLS, ROWS;

void setup() {
size(4800, 4200);
//test size
//size(800, 700);
  background(0);
  ROWS = width/cellwidth;
  COLS = height/cellsize;
  old_board = new int[ROWS][COLS];
  new_board = new int[ROWS][COLS];
  img = loadImage("surprised_3.jpg");
  img.loadPixels();
  // Only need to load the pixels[] array once, because we're only
  // manipulating pixels[] inside draw(), not drawing shapes.
  loadPixels();
  initBoard();
}

void draw(){
  //loop through every spot in our 2D array and check spots neighbors
  for (int x = 0; x<ROWS;x++) {
    for (int y = 0; y<COLS;y++) {
      int nb = 0;
      //Note the use of mod ("%") below to ensure that cells on the edges have "wrap-around" neighbors
      //above row
      if (old_board[(x+ROWS-1) % ROWS ][(y+COLS-1) % COLS ] > 0) { 
        nb++;
      }
      if (old_board[x                 ][(y+COLS-1) % COLS ] > 0) { 
        nb++;
      }
      if (old_board[(x+1)    % COLS   ][(y+COLS-1) % COLS ] > 0) { 
        nb++;
      }
      //middle row
      if (old_board[(x+ROWS-1) % ROWS ][ y ] > 0) { 
        nb++;
      }
      if (old_board[(x+1)    % ROWS   ][ y ] > 0) { 
        nb++;
      }
      //bottom row
      if (old_board[(x+ROWS-1) % ROWS ][(y+1) % COLS ] > 0) { 
        nb++;
      }
      if (old_board[x                 ][(y+1) % COLS ] > 0) { 
        nb++;
      }
      if (old_board[(x+1)      % ROWS ][(y+1) % COLS ] > 0) { 
        nb++;
      }

      //RULES OF "LIFE" HERE
      //if dead
      if      ((old_board[x][y] == 0) && (nb == 3)) { 
        new_board[x][y] = 1;
      }
      //if alive
      else if ((old_board[x][y] > 0) && (nb == 2)) { 
        new_board[x][y] = 2;
      }
      else if ((old_board[x][y] > 0) && (nb == 3)) { 
        new_board[x][y] = 3;
      }
      else { 
        new_board[x][y] = 0;
      }
    }
  }
  float blend = 3;
  //RENDER game of life based on "new_board" values
  for ( int i = 0; i<ROWS;i++) {
    for ( int j = 0; j<COLS;j++) {
      if ((new_board[i][j] > 0 )) {
        int R, G, B;  
        R = G = B = 0;
        if ( new_board[i][j] == 1) {
          R = 80; 
          G = 140; 
          B = 100;
//          R = 94; 
//          G = 124; 
//          B = 136; 
        } 
        else if (new_board[i][j] == 2) {
          R = 100;
          G = 120; 
          B = 150;
//          R =254;
//          G = 180;
//          B = 28; 
        } 
        else if (new_board[i][j] == 3) {
//          R = 62; 
//          G = 96; 
//          B = 111; 
            R = 150;
            G = 150;
            B = 150;
        }
        fill(R, G, B, blend);
        stroke(80,80,80, blend);
//        noStroke();
        rect(i*cellsize, j*cellsize, cellsize, cellsize);
      }
    }
  }
  //swap old and new game of life boards
  int[][] tmp = old_board;
  old_board = new_board;
  new_board = tmp;
  
}

void keyPressed() {
if (key == CODED) {
    if (keyCode == DOWN) {
      save("profile");
    } 
  }
}

void initBoard(){
  for (int x = 0; x < img.width; x++) {
    for (int y = 0; y < img.height; y++){
        int loc = x + y*img.width;
        // Determine the brightness of the pixel
        float pixelBrightness = brightness(img.pixels[loc]);
//        println(pixelBrightness);
        if (pixelBrightness > 100) { 
          old_board[x][y] = 1;
        }
        else { 
          old_board[x][y] = 0;
        }
        float r = red(img.pixels[loc]);
      float g = green(img.pixels[loc]);
      float b = blue(img.pixels[loc]);
//        fill(r,g,b, 200);
        fill(pixelBrightness);
        noStroke();
        rect(x*cellwidth, y*cellsize, cellwidth, cellsize);
    }
  }
}


