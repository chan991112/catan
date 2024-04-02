from pathlib import Path
from typing import List

from action import *
from board import GameBoard, RESOURCES
from queue import LifoQueue
from random import shuffle

def _make_action_sequence(state: dict, board: GameBoard) -> List[Action]:
    # If there is no parent specified in the state, then it is an initial action.
    if 'parent' not in state:
        return []

    # Move back to the parent state, and read the action sequence until that state.
    parental_state, parent_action = state['parent']

    #current_resources = board.get_resource_cards(parental_state)
    #lumber_cards = current_resources['LUMBER']
    #brick_cards = current_resources['BRICK']
    #if lumber_cards < 1 or brick_cards < 1:
    #    return _make_action_sequence(parental_state) + [parent_action]+[PASS()]

    #if RESOURCES['BRICK']>0 and RESOURCES['LUMBER']>0:
     #   return _make_action_sequence(parental_state) + [parent_action]
        
    # Append the required action to reach the current state at the end of the parent's action list.
    return _make_action_sequence(parental_state) + [parent_action]


class Agent:  # Do not change the name of this class!
    """
    An agent class, with DFS
    """
    def search_for_longest_route(self, board: GameBoard) -> List[Action]:
        """
        This algorithm search for an action sequence that makes the longest trading route at the end of the game.
        If there's no solution, then return an empty list.

        :param board: Game board to manipulate
        :return: List of actions
        """
        # Set up frontiers as LIFO Queue
        frontier = LifoQueue()
        # Read initial state
        init_state = board.get_initial_state()
        state = board.simulate_action(init_state,PASS())
        board.set_to_state(state)
        for i in range (3):
                state = board.simulate_action(state,PASS())
                board.set_to_state(state)

        initial_state = state
        frontier.put(initial_state)
        reached = [initial_state['state_id']]

        #ì²ì ì¢í ê°ì ¸ì¤ê¸°
        id=initial_state['player_id']
        s=[]
        
        for coord,info in initial_state['board']['intersections'].items():
            if info['owner'] == id:
                s.append(coord)
        s1,s2=s[0],s[1]

        
        id=initial_state['player_id']
        
       
        a=board.get_applicable_roads()
        

        # Until the frontier is nonempty,
        num=0
        while not frontier.empty():
            num=num+1
            
            
            # Read a state to search further
            state = frontier.get()
            
            board.set_to_state(state)

            if board.is_game_end():
                return _make_action_sequence(state)
            # If it is the game end, then read action sequences by back-tracing the actions.
            

            possible_actions = []
            #ì²« ìí©
            if state == initial_state:
                a=board.get_applicable_roads()
                for i in range(len(a)):
                    for_state=board.simulate_action(initial_state,ROAD(a[i]))
                    board.set_to_state(for_state)
                    
                    b=board.get_applicable_roads()
                    a_set = set(a)
                    b_set = set(b)
                    c = b_set - a_set
                    c=list(c)
                    len(a)
                    if len(c) !=0:
                        
                        possible_actions.append(ROAD(a[i]))
            #ì´íì ìí©            
            
            else:        

                if 'parent' in state:
                    parent=state['parent']
                    
                    parent_state =parent[0]
                    
                else:
                    print("No parent node information available")
                
            
                now_route=board.get_applicable_roads()
                now_longest = board.get_longest_route()

                #s1 s2ê° ì°ê²°ë  ì ìì¼ë©´ ì°ê²°íëë¡ íë ë¶ë¶
                connecting_road=[]
                
                for i in range(len(now_route)):
                    connected_state = board.simulate_action(state, ROAD(now_route[i]))
                  
                    board.set_to_state(connected_state)
                  
                    new_longest = board.get_longest_route()
                    
                    #ì°ê²°ì´ ëìì ë
                    if new_longest-now_longest == 2:
                        connecting_road.append(now_route[i])
                        
                        
                if len(connecting_road) != 0:
                    board.set_to_state(state)
                    possible_actions.append(ROAD(connecting_road[0]))
                    L= board.get_longest_route()
                    

                    for action in possible_actions:
                        child = board.simulate_action(state, action)
                        if child['state_id'] in reached:
                            continue

                        child['parent'] = (state, action)
                        frontier.put(child)
                        reached.append(child['state_id'])


                    state = frontier.get()
                    board.set_to_state(state)
                    a=board.get_applicable_roads()
                    possible_actions=[]
                    L= board.get_longest_route()
                   
                    
                    for i in range(len(a)):
                       
                        for_state=board.simulate_action(state,ROAD(a[i]))
                        board.set_to_state(for_state)
                        
                        b=board.get_applicable_roads()
                        a_set = set(a)
                        b_set = set(b)
                        c = b_set - a_set
                        
                        c=list(c)
                        
                        
                        if len(c) !=0:
                            
                            possible_actions.append(ROAD(a[i]))
                            L=board.get_longest_route()
                            
                        
                else:
                    
                    board.set_to_state(parent_state)
                    parent_L = board.get_longest_route()
                    before_route=board.get_applicable_roads()
                    
                    n_set = set(now_route)
                    b_set = set(before_route)
                    right_path = n_set - b_set
                    right_path=list(right_path)
                    
                    board.set_to_state(state)
                    for i in range(len(right_path)):
                        possible_actions.append(ROAD(right_path[i]))
                    
            
            # Expand next states
            parent_L=board.get_longest_route()
            

            for action in possible_actions:
                child = board.simulate_action(state, action)
                
                # If the next state is already reached, then pass to the next action
                if child['state_id'] in reached:
                    continue

                # Add parent information to the next state
                child['parent'] = (state, action)

                frontier.put(child)

                reached.append(child['state_id'])
                

            
            L = board.get_longest_route()

            if L==9 and parent_L==8:
                state_9 = state
                

            if frontier.empty():
                state= state_9   
                board.set_to_state(state)
                a= board.get_applicable_roads()
                current_resources = board.get_resource_cards(state)
                lumber_cards = current_resources['LUMBER']
                brick_cards = current_resources['BRICK']
                if lumber_cards < 1 or brick_cards < 1:
                    final_00=board.simulate_action(state,PASS())
                    board.set_to_state(final_00)
                    final_00['parent']=(state,PASS())
                    frontier.put(final_00)
                final_0= board.simulate_action(state, ROAD(a[0]))
                board.set_to_state(final_0)
                final_0['parent'] = (state, ROAD(a[0]))
                frontier.put(final_0)
                final_01 = frontier.get()
                final_1=board.simulate_action(final_01, UPGRADE(s1))
                board.set_to_state(final_1)
                L=board.get_longest_route()
                final_1['parent'] = (final_01, UPGRADE(s1))
                frontier.put(final_1)
                final_2=frontier.get()
                final_3=board.simulate_action(final_2,UPGRADE(s2))
                board.set_to_state(final_3)
                final_3['parent'] = (final_2, UPGRADE(s2))
                frontier.put(final_3)
            
            if L ==10:
                state=frontier.get()   
                final_1=board.simulate_action(state, UPGRADE(s1))
                board.set_to_state(final_1)
                L=board.get_longest_route()
                final_1['parent'] = (state, UPGRADE(s1))
                frontier.put(final_1)
                final_2=frontier.get()
                final_3=board.simulate_action(final_2,UPGRADE(s2))
                board.set_to_state(final_3)
                final_3['parent'] = (final_2, UPGRADE(s2))
                frontier.put(final_3)

                
                
                
        # Return empty list if search fails.
        return []
