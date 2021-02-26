## End-to-End-Guided-RL-using-Online-Learning
##### Designed a Novel End to End algorithm with Reinforcement Learning guided by Online Learning to MPC(Model Predictive Control), leading to optimal policies for continuous control tasks. 

Simulation results:
Control Task is to Swingup and Balance the pole:

a)Control of Cartpole with Augmented Random Search(a Model Free RL):
  Pole Fails to stay in the upright position after swingup using ARS alone
<p align="center">
   <img width="300" height="180" src="https://github.com/soumyarani/End-to-End-Guided-RL-using-Online-Learning/blob/main/media/ars.gif"
</p>

b)Control of Cartpole with Augmented Random Search + Online Learning MPC
Pole balances forever, online Learning guides the Augmented Random Search (RL policy)
<p align="center">
   <img width="200" height="180" src="https://github.com/soumyarani/End-to-End-Guided-RL-using-Online-Learning/blob/main/media/ars_ol.gif">
</p>
           
         
         
