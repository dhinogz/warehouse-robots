
Algoritmo

1. Init
    Goal: place agents

    - place agents, goals, obstacles
    - assign goals to agents based on position
2. Agent step
    Goal: calc and/or get agent's current path and next move

    - Check if current_path is empty
    - if empty
        - agent calculates a* path to goal
        - adds path to current_path (list of tuples)
    - Add next move value to dictionary of agent_id key
3. Agent advance
    Goal: avoid collision between agents and move agents

    - Init occupied set
    - Iterate over dict with next moves
    - check if next move in occupied set
        - if already exists, don't move

    - if does not exist
        - add to set

    - if new_pos a goal
        - remove current path
        - remove goal
        - announce found goal
    
