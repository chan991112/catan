from pathlib import Path
from typing import List

from action import *
from board import GameBoard, RESOURCES
from queue import LifoQueue


def _make_action_sequence(state: dict) -> List[Action]:
    # If there is no parent specified in the state, then it is an initial action.
    if 'parent' not in state:
        return []

    # Move back to the parent state, and read the action sequence until that state.
    parental_state, parent_action = state['parent']
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
        initial_state = board.get_initial_state()
        frontier.put(initial_state)
        reached = [initial_state['state_id']]

        #처음 좌표 가져오기
        id=initial_state['player_id']
        s=[]
        
        for coord,info in initial_state['board']['intersections'].items():
            if info['owner'] == id:
                s.append(coord)
        s1,s2=s[0],s[1]

        
        id=initial_state['player_id']
        print(id)
        # for coord,info in initial_state['board']['intersections'].items():
        #     if info['owner'] == id:
        #         s1,s2=initial_state['board']['intersections']['coord']
        # print(s1,s2)
        a=board.get_applicable_roads()
        print(a)
        # Until the frontier is nonempty,
        num=0
        while not frontier.empty():
            num=num+1
            print('\n')
            print('loop {} 시작'.format(num))
            # Read a state to search further
            state = frontier.get()
            #print(state['state_id'])
            board.set_to_state(state)
            
            # If it is the game end, then read action sequences by back-tracing the actions.
            if board.is_game_end():
                return _make_action_sequence(state)

            possible_actions = []
            #첫 상황
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
                    if len(c) !=0:
                        possible_actions.append(ROAD(a[i]))
            #이후의 상황
            else:
                R=board.get_resource_cards()
                L=R['Lumber']
                                
                if 'parent' in state:
                    parent_state=state['parent_state']
        
                else:
                    print("No parent node information available")
                
                now_route=board.get_applicable_roads()
                
                board.set_to_state(parent_state)
                before_route=board.get_applicable_roads()
                
                n_set = set(now_route)
                b_set = set(before_route)
                right_path = n_set - b_set
                right_path=list(right_path)
                for i in range(len(right_path)):
                    possible_actions.append(ROAD(right_path[i]))
                    possible_actions.append(PASS())

                
                
                
                


            # Expand next states
            for action in possible_actions:
                child = board.simulate_action(state, action)

                # If the next state is already reached, then pass to the next action
                if child['state_id'] in reached:
                    continue

                # Add parent information to the next state
                child['parent'] = (state, action)
                child['parent_state']=state
                child['parent_action']=action
                frontier.put(child)
                reached.append(child['state_id'])
            
            print('frontier: {}'.format(frontier.qsize()))
        
            print('possible_actions: {}'.format(possible_actions))
            L=board.get_longest_route()
            R=board.get_resource_cards()
            print(R)
            print('끝 전에 길이{}'.format(L))
            print('loop 끝')
        # Return empty list if search fails.
        return []