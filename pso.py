import numpy as np;
import math 

# Particle Swarm Optimization
def PSO(problem, MaxIter = 100, PopSize = 100, c1 = 1.4962, c2 = 1.4962, w = 0.7298, wdamp = 1.0):

    # Empty Particle Template
    empty_particle = {
        'position': [None, None],
        'velocity': None,
        'cost': None,
        'best_position': None,
        'best_cost': None,
    };

    # Extract Problem Info
    # CostFunction = problem['CostFunction'];
    VarMin1 = problem['VarMin1'];
    VarMax1 = problem['VarMax1'];
    nVar1 = problem['nVar1'];
    VarMin2 = problem['VarMin2'];
    VarMax2 = problem['VarMax2'];
    nVar2 = problem['nVar2'];
    # print(VarMin2)
    # Initialize Global Best
    gbest = {'position': [None, None], 'cost': np.inf};

    # Create Initial Population
    pop = [];
    for i in range(0, PopSize):
        pop.append(empty_particle.copy());
        # print(VarMin1)
        pop[i]['position'][0] = np.random.uniform(VarMin1, VarMax1, nVar1);
        pop[i]['position'][1] = np.random.uniform(VarMin2, VarMax2, nVar2);
        pop[i]['velocity'] = np.zeros(nVar1);
        # print(i)
        # print(pop[i]['position'])
        pop[i]['cost'] = CostFunction(pop[i]['position'][0], pop[i]['position'][1]);
        
        
        pop[i]['best_position'] = pop[i]['position'].copy();
        pop[i]['best_cost'] = pop[i]['cost'];
        
        #print(gbest['cost'])
        
        if pop[i]['best_cost'] < gbest['cost']:
            gbest['position'] = pop[i]['best_position'].copy();
            gbest['cost'] = pop[i]['best_cost'];
    
    #print(gbest['cost'])
    #print(gbest['position'])
    #print(pop)
    # PSO Loop
    #print(gbest)
    
    for it in range(0, MaxIter):
        for i in range(0, PopSize):

            
            ####################### check for updation of velocity
            pop[i]['velocity'] = w*pop[i]['velocity'] \
                + c1*np.random.rand(nVar1)*(pop[i]['best_position'][0] - pop[i]['position'][0]) \
                + c2*np.random.rand(nVar2)*(gbest['position'][0] - pop[i]['position'][0]) \
                + c1*np.random.rand(nVar1)*(pop[i]['best_position'][1] - pop[i]['position'][1]) \
                + c2*np.random.rand(nVar2)*(gbest['position'][1] - pop[i]['position'][1]);
            
         
            
            pop[i]['position'][0] = pop[i]['position'][0]+pop[i]['velocity'];
            pop[i]['position'][0] = np.maximum(pop[i]['position'][0], VarMin1);
            pop[i]['position'][0] = np.minimum(pop[i]['position'][0], VarMax1);
            
            pop[i]['position'][1] = pop[i]['position'][1]+pop[i]['velocity'];
            pop[i]['position'][1] = np.maximum(pop[i]['position'][1], VarMin2);
            pop[i]['position'][1] = np.minimum(pop[i]['position'][1], VarMax2);
            
            
            pop[i]['cost'] = CostFunction(pop[i]['position'][0], pop[i]['position'][1]);
            
            
            if pop[i]['cost'] < pop[i]['best_cost']:
                pop[i]['best_position'] = pop[i]['position'].copy();
                pop[i]['best_cost'] = pop[i]['cost'];

                if pop[i]['best_cost'] < gbest['cost']:
                    gbest['position'] = pop[i]['best_position'].copy();
                    gbest['cost'] = pop[i]['best_cost'];
                    
        print('Cost {}:Best Cost = {}:global Position= {}'.format(pop[i]['cost'], pop[i]['best_cost'], gbest['position']));
            
        w *= wdamp;
        #print('Iteration {}:Best Cost = {}:Best Position= {}'.format(it, gbest['cost'],gbest['position']));

    return gbest, pop;
# longitude = [2807.7718960252473, -25424.346848140533, 2623.1196524951783, -7221.012642824979, 1442.8748878171918, 3794.2450033991713, -8258.702609365839, -10967.699538703342, -94356.14852337386, -94287.91323523699, 33274.28123818452, -344108.57514588634]
# latitude = [18948.345410799782, 23336.516000885502, 2137.7659436818576, 3867.7248011471575, -401.3975469222055, -14078.411400037792, 1699.452933026549, 14389.953025955212, -68867.6217840994, -82696.28271079031, -39967.898010066776, 151947.33059280113]
 
def CostFunction(x, y):
    y2 = []
    y_res = 0
    y3 = [0.065, 0.045, -0.098, -0.092, -0.078, 0.032, 0.102, -0.044, 0.088, 0.097, 0.034, 0.077]
    for i in range(12):
        y2.append(latitude[i] * x + longitude[i] * y)
        
        y_res = y_res + y2[i] * y2[i] * y3[i]
    return y_res
# p = CostFunction(-7989, 987896)
# print(p)
#for it in range(100):
 #   print('Iteration {}: Best Cost = {}:  Latitude = {}: Longitude = {}'.format(it, np.random.uniform(4951.465, 5010.6554), np.random.uniform(18.81555, 18.99021), np.random.uniform(75.758888, 75.8023)));

#longitude = [28.7718960252473, -25.346848140533, 26.1196524951783, -72.012642824979, 14.8748878171918, 37.2450033991713, -82.702609365839, -10.699538703342, -94.14852337386, -94.91323523699, 33.28123818452, -34.57514588634]
#latitude = [18.345410799782, 23.516000885502, 21.7659436818576, 38.7248011471575, -40.3975469222055, -14.411400037792, 16.452933026549, 14.953025955212, -68.6217840994, -82.28271079031, -39.898010066776, 15.33059280113]

longitude = [2807.7718960252473, -25424.346848140533, 2623.1196524951783, -7221.012642824979, 1442.8748878171918, 3794.2450033991713, -8258.702609365839, -10967.699538703342, -94356.14852337386, -94287.91323523699, 33274.28123818452, -344108.57514588634]
latitude = [18948.345410799782, 23336.516000885502, 2137.7659436818576, 3867.7248011471575, -401.3975469222055, -14078.411400037792, 1699.452933026549, 14389.953025955212, -68867.6217840994, -82696.28271079031, -39967.898010066776, 151947.33059280113]

'''
problem = {
        'VarMin1': 18.10,
        'VarMax1': 19.79,
        'nVar1': 1,
        'VarMin2': 75.10,
        'VarMax2': 77.40,
        'nVar2': 1
    };
'''
        
problem = {
        'VarMin1': 19.84,
        'VarMax1': 19.86,
        'nVar1': 1,
        'VarMin2': 75.19,
        'VarMax2': 75.45,
        'nVar2': 1
    };        
        
PSO(problem)