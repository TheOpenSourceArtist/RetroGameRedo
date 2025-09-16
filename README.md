--------------------------------------------------------------------------------
	Simple Game Engine
--------------------------------------------------------------------------------

	Contents:
		* base.py
		* renderable.py
		* utils.py
		* SimpleGE.py
				
--------------------------------------------------------------------------------
	Getting Started
--------------------------------------------------------------------------------

	SimpleGE is an extension of Pygame that is intended to make it simple to
	create games that consist of multiple game states and modular. To start a
	SimpleGE project, copy the contents of SimpleGE into a folder and create a
	new python script in the same folder to hold the game code. A very simple 
	script might look like this:
	
________________________________________________________________________________

	from SimpleGE import *
	
	def main() -> None:
		myGame: Game = Game(
			name = 'My SimpleGE Game'
			,displaySize = [800,600]
			,initialState = None
		)
		
		myGame.run()
	
		return
	#end main
	
	if __name__ == '__main__':
		main()
	#end if

________________________________________________________________________________

	This script imports all the contents of SimpleGE.py, creates a Game object,
	and calls the game object's run() function. This game will not do anything,
	because it only has the default GameState. Before we get into GameStates,
	let's look at the contents of the Game class itself.
	
--------------------------------------------------------------------------------
	Game Class
--------------------------------------------------------------------------------

	The Game class will control the flow of the game, switching between states
	and rendering to the display. The Game class hold several important member
	variables and functions:
	
		Member Variables
	
		* fps: int 
			How many frame will be rendred in a second
        * clock: Pygame.time.Clock 
        	The Clock object to sync to the FPS
        * deltaTime: float 
        	The time in milliseconds since the last frame
        * displaySize: list[int] 
        	The size in pixels of the display window
        * display: pg.surface.Surface 
        	The display window
        * renderScale: list[float] 
        	How much the GameState render buffer is scaled
        * keysDown: list[bool] 
        	List of keys that are pressed this frame
        * mouseDown: list[bool] 
        	List of mouse buttons pressed this frame
        * mousePos: list[int] 
        	Position of mouse cursor, scaled to the render scale
        * _state: GameState 
       		The current GameState object
       	* running: bool
       		Is the game running
        
        Member Functions
        
        * handleEvents() -> None 
        	Handles Display events and polls user inputs.
        	The polled inputs (keys, mouse buttons, and mouse position) are
        	then passed to the Game's _state object
        	
        * render() -> None 
        	Call the _state object's render function. Then,
        	scale the _state object's renderBuffer by the renderScale, and
        	blit the scaled renderBuffer to the Game's display.
        	
        * update(self) -> None 
        	Pass the Game's deltaTime to the _state object
        	and call the _state's update function
        	
        * syncFPS(self) -> None
        	Slow down game execution to sync with its frame rate and
        	store the deltaTime value (in ms) between the current frame and
        	the last frame
        
        * switchState(self, otherState: GameState) -> None
        	Set the _state object to a new GameState and refresh the
        	renderScale
        	
        * run() -> None
        	Calls the member functions in order handleEvents(), update(),
        		render(), syncFPS() and loops indefinitely while running
        		is True. Deinitializes Pygame when running is set to False
