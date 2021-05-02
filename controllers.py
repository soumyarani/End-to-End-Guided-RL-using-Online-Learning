import numpy as np
from cost_functions import trajectory_cost_fn
import time

class RandomController():
	def __init__(self, env):
		self.env = env

	def get_action(self, state):
		return self.env.action_space.sample()

class DMDMPCcontroller():
	""" Controller built using the MPC method outlined in Online Learning Approach to MPC """
	def __init__(self, 
				 env, 
				 dyn_model, 
				 horizon=20, 
				 cost_fn=None, 
				 num_simulated_paths=1000,
				 ):
		self.env = env
		self.dyn_model = dyn_model
		self.horizon = horizon
		self.cost_fn = cost_fn
		self.num_simulated_paths = num_simulated_paths
		self.gamma = 0.9
		self.mean = np.full((horizon,6),0)
		self.std = 0.4*np.identity((6))
		self.elite = 10

	def get_action(self, state):
		obs, obs_list, obs_next_list, act_list = [], [], [], []
		[obs.append(state) for _ in range(self.num_simulated_paths)]
	
		for step in range(self.horizon):
			obs_list.append(obs)

			actions = []
			
			for _ in range(self.num_simulated_paths):
				action = np.random.multivariate_normal(self.mean[step],self.std)
				action = np.clip(action, 0.99*self.env.action_space.low, 0.99*self.env.action_space.high)	
				actions.append(action)
			act_list.append(actions)
			obs = self.dyn_model.predict(np.array(obs), np.array(actions))
			obs_next_list.append(obs)

		trajectory_cost_list = trajectory_cost_fn(self.cost_fn, np.array(obs_list), np.array(act_list), np.array(obs_next_list)) 

		elite_inds = trajectory_cost_list.argsort()[0:self.elite]
		act_list=np.array(act_list)
		trajectory_actions=np.array([act_list[:,i,:]*trajectory_cost_list[i] for i in elite_inds])

		grad_m=np.sum(trajectory_actions, axis=0)
		total_cost=np.sum(trajectory_cost_list[elite_inds])
		grad_m=grad_m/total_cost

		self.mean=(1-self.gamma)*self.mean+self.gamma*grad_m

		#shift means, std
		last_mean = self.mean[self.horizon-1].copy()
		self.mean=np.vstack((self.mean[1:],last_mean))
		
		#first control to real model
		action = self.mean[0].copy()
		action=np.clip(action, self.env.action_space.low, self.env.action_space.high)

		return action
