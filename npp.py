# Copyright 2020 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

## ------- import packages -------
from dwave.system import DWaveSampler, EmbeddingComposite
from collections import defaultdict

# TODO:  Add code here to define your QUBO dictionary
def get_qubo(S):
    """Returns a dictionary representing a QUBO.

    Args:
        S(list of integers): represents the numbers being partitioned
    """
    Q = defaultdict(int)
    C = sum(S)
    # Add QUBO construction here
    for i in range(len(S)):
        Q[(i,i)] = -4*C*S[i] + 4*S[i]**2
        for j in range(i+1, len(S)):
            Q[(i,j)] = 8*S[i]*S[j]

    '''Q = {(0,0):-14100, (0,1):1400, (0,2): 2600, (0,3): 6200, (0,4): 8400, (0,5): 3400, (0,6):4200, (0,7):2000, \
                       (1,1):-4452, (1,2):728, (1,3):1736, (1,4):2352, (1,5):952, (1,6):1176, (1,7):560, \
                                    (2,2):-7956, (2,3):3224, (2,4):4368, (2,5):1768, (2,6):2184, (2,7):1040, \
                                                 (3,3):-16740, (3,4):10416, (3,5):4216, (3,6):5208, (3,7):2480, \
                                                               (4,4):-20832, (4,5):5712, (4,6):7056, (4,7):3360, \
                                                                             (5,5):-10132, (5,6):2856, (5,7):1360, \
                                                                                           (6,6):-12180, (6,7):1680, \
                                                                                                         (7,7):-6240}'''
    print(Q)
    return Q

# TODO:  Choose QPU parameters in the following function
def run_on_qpu(Q, sampler):
    """Runs the QUBO problem Q on the sampler provided.

    Args:
        Q(dict): a representation of a QUBO
        sampler(dimod.Sampler): a sampler that uses the QPU
    """

    chainstrength = 20000 # update
    # chain_strength=chainstrength
    numruns = 1000 # update

    sample_set = sampler.sample_qubo(Q, num_reads=numruns, chain_strength=chainstrength, label='Training - Number Partitioning')
    
    return sample_set


## ------- Main program -------
if __name__ == "__main__":

    ## ------- Set up our list of numbers -------
    S = [25, 7, 13, 31, 42, 17, 21, 10]

    ## ------- Set up our QUBO dictionary -------

    Q = get_qubo(S)

    ## ------- Run our QUBO on the QPU -------

    sampler = EmbeddingComposite(DWaveSampler())

    sample_set = run_on_qpu(Q, sampler)

    ## ------- Return results to user -------
    for sample in sample_set:
        S1 = [S[i] for i in sample if sample[i] == 1]
        S0 = [S[i] for i in sample if sample[i] == 0]
        print("S0 Sum: ", sum(S0), "\tS1 Sum: ", sum(S1), "\t", S0)
