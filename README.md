# A Cognitive Model of Hippocampal Replay as Hypothesis Testing for Efficient Generalization
This is a project for COG403: Seminar in Cognitive Science at the University of Toronto. I investigated a particular hypothesis on hippocampal replay in a brick-based game task whose code can be found [here]([https://github.com/schwartenbeckph/Generative-Replay/]).

<p align="center">
<img width="30%" src="https://github.com/mishaalkandapath/clarion_replay/blob/main/figures/agentpic.png">
</p>

## Contributions
This project mainly deals with a first attempt at formalizing a hypothesis presented in this 
[Kurth-Nelson, Zeb, et al. "Replay and compositional computation." Neuron 111.4 (2023): 454-469.]([https://www.cell.com/neuron/fulltext/S0896-6273(22)01125-4?_returnURL=https%3A%2F%2Flinkinghub.elsevier.com%2Fretrieve%2Fpii%2FS0896627322011254%3Fshowall%3Dtrue]) 
based on a task presented in 
[Schwartenbeck, Philipp, et al. "Generative replay underlies compositional inference in the hippocampal-prefrontal circuit." Cell 186.22 (2023): 4885-4897.]([https://www.cell.com/neuron/fulltext/S0896-6273(22)01125-4?_returnURL=https%3A%2F%2Flinkinghub.elsevier.com%2Fretrieve%2Fpii%2FS0896627322011254%3Fshowall%3Dtrue]) 

The code is supplementary to the paper included in the repository (file: paper.pdf).

## Reproducing Results
### Installation
The easiest way to install all necessary packages would be to build a conda/virtualenv environment from the yaml file
#### Conda
```
conda env create -f clarion_env.yml	# create & install
conda activate clarion_env			      # activate
```
###Note: this module requires pyClarion, which needs to be independently downloaded from [here]([https://github.com/cmekik/pyClarion/tree/v2409])
 ### Running
 Simply run simulation.py to reproduce all results in the paper. 
 ```
 python simulation.py
 ```
 rule_defs.py defines all the rules the model uses, knowledge_init.py defines all the basic atoms for organizing knowledge, and base_participant.py defines various model variations with AbstractParticipant being the main model tested in this work.

### Some Results
<p align="center">
 <img width="50%" src="https://github.com/mishaalkandapath/valuedream/blob/main/plots/reward.png"><br>
 Returns over time<br>
 <img width="50%" src="https://github.com/mishaalkandapath/valuedream/blob/main/plots/score.png"><br>
 Scores over time<br>
 <img width="50%" src="https://github.com/mishaalkandapath/valuedream/blob/main/plots/score-big.png"><br>
 Spectrum of achievements at 1M steps<br>
</p>


