
import numpy as np
import math



class MDP():

	def __init__(self):
		pass

	def reward(self, state, action, drone):
		drone_state, target_state = state
		next_drone_state = drone.evaluate_next_state(action)
		# print next_drone_state
		return -np.linalg.norm([target_state[0] - next_drone_state[0], target_state[1] - next_drone_state[1]])

	def get_state(self, drone, target):
		return (drone.get_state(), target.get_state())

	def best_action(self, drone, target, world):
		state = self.get_state(drone, target)

		rewards = sorted([(self.reward(state, action, drone), action) for action in drone.get_actions()], key=lambda x: x[0], reverse=True)
		print rewards
		best_reward, best_action = rewards[0]
		for i in xrange(1, len(rewards)):
			curr_reward, curr_action = rewards[i]
			if curr_reward != best_reward:
				break
			elif abs(curr_action) < abs(best_action):
				best_action = curr_action
		# return -3

		print ' BEST:', best_action, best_reward

		return best_action






