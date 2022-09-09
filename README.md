# Context-Aware Native Gate-Level Optimization of the Toffoli Gate

This repository contains software and reports pertaining to context-aware native gate-level optimization of the Toffoli gate. Please see
the associated arXiv paper [here](https://arxiv.org/abs/2209.02669).
While the focus of this work is the Toffoli gate, the techniques explored are generalizable
to any quantum circuit.

A C++ version of this code supporting a subset of the features of this repository is available [here](https://github.com/maxaksel/QuOpt).
This code was used for numerical discovery 6-layer Toffoli gate structures over the {single qubit operations, FANOUT, CNOT} gate set.

Example parameters (in degrees) corresponding to Fig. 10 in paper: [ 60.  60. 185. 300. 300. 100. 300. 120. 225.  85. 185. 150. 240. 270., 180.  85. 120.  60. 135.  60. 225. 225.  45. 190. 265. 270. 270. 275., 135.  60.  80. 135. 355.   0. 135.  45. 135. 150.  45. 120. 225. 150., 280. 150. 120. 315. 135. 240.  75. 330. 300. 100. 210. 210.  90. 240., 165. 135. 300. 300.  60. 270. 270.]. Parameters are specified as (theta, phi, lambda) down and to the right.
