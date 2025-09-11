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

	
