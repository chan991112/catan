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


class Agent:
    def search_for_longest_route(self, board: GameBoard) -> List[Action]:
        """
        Searches for the longest trading route using depth-first search.

        :param board: Game board to manipulate
        :return: List of actions that lead to the longest route
        """
        frontier = LifoQueue()
        initial_state = board.get_initial_state()
        frontier.put(initial_state)
        reached = set([initial_state['state_id']])

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
            num+=1
            #print('\n')
            #print('loop {} 시작'.format(num))
            # Read a state to search further
            state = frontier.get()
            #print(state['state_id'])
            board.set_to_state(state)
            

            if board.is_game_end():
                return _make_action_sequence(state)

            for action in self.get_possible_actions(board):
                next_state = board.simulate_action(state, action)
                if next_state['state_id'] not in reached:
                    next_state['parent'] = (state, action)
                    frontier.put(next_state)
                    reached.add(next_state['state_id'])

        return []

    def get_possible_actions(self, board: GameBoard) -> List[Action]:
        """
        Generate a list of possible actions from the current state of the board.

        :param board: The current game board
        :return: A list of viable actions
        """
        possible_actions = []
        resources = board.get_resource_cards()
        if resources['Lumber'] > 0:  # Example resource check
            for road_location in board.get_applicable_roads():
                possible_actions.append(ROAD(road_location))
        return possible_actions