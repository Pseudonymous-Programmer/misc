require 'gosu'

WINDOW_W = 200
WINDOW_H = 400

TILE_SIZE = 20
TILE_W = WINDOW_W / TILE_SIZE
TILE_H = WINDOW_H / TILE_SIZE

BLOCK_I = [
  [:empty,:cyan,:empty,:empty],
  [:empty,:cyan,:empty,:empty],
  [:empty,:cyan,:empty,:empty],
  [:empty,:cyan,:empty,:empty]
]

BLOCK_T = [
  [:purple,:purple,:purple],
  [:empty,:purple,:empty],
  [:empty,:empty,:empty]
]

BLOCK_O = [
  [:yellow,:yellow],
  [:yellow,:yellow]
]

BLOCK_L = [
  [:empty,:orange,:empty],
  [:empty,:orange,:empty],
  [:empty,:orange,:orange]
]

BLOCK_J = BLOCK_L.map {|row| row.reverse.map {|tile| tile == :empty ? :empty : :blue}}

BLOCK_S = [
  [:green,:green,:empty],
  [:empty,:green,:green],
  [:empty,:empty,:empty]
]

BLOCK_Z = BLOCK_S.map {|row| row.reverse.map {|tile| tile == :empty ? :empty : :red}}

BLOCKS = [BLOCK_I,BLOCK_T,BLOCK_O,BLOCK_L,BLOCK_J,BLOCK_S,BLOCK_Z]

$to_color = {empty: Gosu::Color::NONE,
            cyan: Gosu::Color::CYAN,
            red: Gosu::Color::RED,
            green: Gosu::Color::GREEN,
            purple: Gosu::Color.new(128,0,128),
            yellow: Gosu::Color::YELLOW,
            orange: Gosu::Color.new(255,165,0),
            blue: Gosu::Color::BLUE}

class Vec2
  attr_accessor :x,:y
  def initialize(x,y)
    @x = x
    @y = y
  end
  def +(other)
    Vec2.new(@x+other.x,@y+other.y)
  end
  def dup
    Vec2.new(@x,@y)
  end
  def to_str
    "(#{@x},#{@y})"
   end
end

class Block
  attr_accessor :location
  def initialize(structure,location)
    @structure = structure
    @location = location
  end

  def rotate!
    result = []
    @structure.transpose.each do |col|
      result << col.reverse
    end
    @structure = result
    return self
  end

  def display(tetris)
    @structure.each_with_index do |row,y|
      row.each_with_index do |tile,x|
        tetris.render_tile(x + @location.x,y + @location.y,tile)
      end
    end
  end

  def display_next(tetris)
    4.times do |y|
      4.times do |x|
        tetris.render_next(x,y,:empty)
      end
    end
    @structure.each_with_index do |row,y|
      row.each_with_index do |tile,x|
        tetris.render_next(x,y,tile)
      end
    end
   end

  def to_locations
    result = []
    @structure.each_with_index do |row,y|
      row.each_with_index do |tile,x|
        result << Vec2.new(x,y) + @location if tile != :empty
      end
    end
    result.compact
  end

  def to_locations_with_tiles
    result = []
    @structure.each_with_index do |row,y|
      row.each_with_index do |tile,x|
        result << [Vec2.new(x,y) + @location,tile] if tile != :empty
      end
    end
    result
  end

  def dup
    Block.new(@structure.dup,@location.dup)
  end
end



class Tetris < Gosu::Window
  def initialize
    @tiles = []
    TILE_H.times do
      @tiles << Array.new(TILE_W,:empty)
    end
    @next_block = get_new_block
    get_next_block
    @ticks = 0
    @tick_frequency = 1.0/20
    @rotate_cooldown = 0
    @score = 0
    @level = 1
    @cleared_rows = 0
    @clear_rows_recursion = 0
    @block_click = Gosu::Sample.new("click_x.wav")
    super WINDOW_W + 200,WINDOW_H
    Gosu::Song.new("tetris.wav").play(true)
  end

  def get_new_block
    Block.new(BLOCKS.sample.dup,Vec2.new(TILE_W/2,0))
  end

  def get_next_block
    @current_block = @next_block.dup
    @next_block = get_new_block
  end

  def update
    @ticks += 1
    if @ticks == (1/@tick_frequency).round
      @ticks = 0
      @current_block.location.y += 1
      if test_collision
        @current_block.location.y -= 1
        place @current_block
      end
    end
  end

  def button_down(id)
    backup = @current_block.dup
    if id == Gosu::KB_SPACE
      @current_block.rotate!
    elsif id == Gosu::KB_LEFT
      @current_block.location.x -= 1
    elsif id == Gosu::KB_RIGHT
      @current_block.location.x += 1
    elsif id == Gosu::KB_DOWN
      while !test_collision
        @current_block.location.y += 1
      end
      @current_block.location.y -= 1
      place @current_block
    end


    if test_collision
      @current_block = backup
    end
  end

  def test_collision
    @current_block.to_locations.each do |location|
      return true if location.x < 0 || location.x >= TILE_W
      return true if location.y < 0 || location.y >= TILE_H
      return true if @tiles[location.y][location.x] != :empty
    end
    false
  end

  def place(block)
    @current_block.to_locations_with_tiles.each do |location,tile|
      @tiles[location.y][location.x] = tile
    end
    clear_full_rows
    get_next_block
    quit if @tiles[0].any? {|tile| tile != :empty}
    @block_click.play
  end

  def clear_full_rows
    new_tiles = @tiles.dup
    @tiles.length.times do |i|
      if @tiles[i].all? {|tile| tile != :empty}
        new_tiles.delete_at(i)
        @score += 100
        @cleared_rows += 1
        if @cleared_rows == 5
          @tick_frequency *= 1.2
          @cleared_rows = 0
          @level += 1
          @ticks = 0
        end
      end
    end
    while(new_tiles.length != @tiles.length)
      new_tiles.unshift(Array.new(TILE_W,:empty))
    end
    @tiles = new_tiles
    @clear_rows_recursion += 1
    clear_full_rows if @clear_rows_recursion < 5
    @clear_rows_recursion = 0
  end

  def draw
    Gosu.draw_rect(0,0,WINDOW_W,WINDOW_H,Gosu::Color.new(50,50,50))
    Gosu.draw_rect(WINDOW_W + 50 - 2,75 - 2,89,89,Gosu::Color::WHITE)
    Gosu::Image.from_text("TETRIS",40).draw(WINDOW_W + 50,10,0)
    Gosu::Image.from_text("NEXT BLOCK",20).draw(WINDOW_W + 50,50,0)
    Gosu::Image.from_text("SCORE: #{@score}",30).draw(WINDOW_W + 50,200,0)
    Gosu::Image.from_text("LEVEL: #{@level}",30).draw(WINDOW_W + 50,300,0)
    @tiles.each_with_index do |row,y|
      row.each_with_index do |tile,x|
        render_tile(x,y,tile) if tile != :empty
      end
    end
    @current_block.display(self)
    @next_block.display_next(self)
  end

  def render_tile(x,y,tile)
    Gosu.draw_rect(x*TILE_SIZE,y*TILE_SIZE,TILE_SIZE,TILE_SIZE,$to_color[tile])
  end

  def render_next(x,y,tile)
    Gosu.draw_rect(WINDOW_W + 50 + x*22, 75 + y*22,19,19,tile == :empty ? Gosu::Color::BLACK : $to_color[tile])
  end

  def quit
    close
  end
end

tetris = Tetris.new.show
