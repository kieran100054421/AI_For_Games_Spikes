# Three state machine example ... bad code included.

# variables
if __name__ == '__main__':
	int_energy = 0
	distance_travelled = 0
	distance_left = 150
	max_distance = 150

	states = ['running', 'resting', 'finished']
	current_state = 'resting'

	running = True
	finished = False
	max_limit = 100
	game_time = 0

	while running:
	    game_time += 1

	    # resting: racer stopped, increasing energy
	    if current_state is 'resting':
	        # Do things for this state
	        print("Racer has no energy. Racer is resting.")
	        int_energy += 1
	        # Check for change state
	        if int_energy >= 10:
	            current_state = 'running'

	    # Running: racer is running, energy decreases, distance travelled increased
	    elif current_state is 'running':
	        # Do things for this state
	        print("The racer is running")
	        int_energy -= 2
	        distance_travelled += 10;
	        distance_left = max_distance - distance_travelled
	        # Check for change state
	        if int_energy < 1:
	            current_state = 'resting'
	        if distance_left < 0:
	            current_state = 'finished'
	            
	    # Eating: reduces hunger, still gets tired
	    elif current_state is 'finished':
	        # Do things for this state
	        print("The race is over, the racer has finished the end")
	        running = False
	            
	    # check for broken ... :(
	    else:
	        print("AH! BROKEN .... how did you get here?")
	        die() # not a real function - just breaks things! :)
	        
	    # Check for end of game time
	    if game_time > max_limit:
	        running = False

	print('-- The End --')