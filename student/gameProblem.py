
'''
    Class gameProblem, implements simpleai.search.SearchProblem
'''


from simpleai.search import SearchProblem
# from simpleai.search import breadth_first,depth_first,astar,greedy
import simpleai.search

class GameProblem(SearchProblem):

    # Object attributes, can be accessed in the methods below
    
    MAP=None
    POSITIONS=None
    INITIAL_STATE=None
    GOAL=None
    CONFIG=None
    AGENT_START=None
    SHOPS=None
    CUSTOMERS=None
    MAXBAGS = 0

    MOVES = ('West','North','East','South')

   # --------------- Common functions to a SearchProblem -----------------

    def actions(self, state):
        '''Returns a LIST of the actions that may be executed in this state
        '''

        #  If actions are in the list of movement actions
        # (North, East, etc.), they will generate moves in the map when the path is
        # followed, but you can use additional actions

        # self.CONFIG['map_size'][0] - 1 -> x-coordinate (max) east-most
        # self.CONFIG['map_size'][1] - 1 -> y-coordinate (max) south-most

        actions = list(self.MOVES)

        # print(state[0], state[1])

        #West
        if (state[0] - 1) < 0:
            actions.remove('West')

        elif self.getAttribute((state[0] - 1, state[1]), 'blocked'):
            actions.remove('West')

        #North
        if (state[1] - 1) < 0: 
            actions.remove('North')

        elif self.getAttribute((state[0], state[1] - 1), 'blocked'):
            actions.remove('North')

        #East
        if (state[0] + 1) > (self.CONFIG['map_size'][0] - 1):
            actions.remove('East')

        elif self.getAttribute((state[0] + 1, state[1]), 'blocked'):
            actions.remove('East')

        #South
        if (state[1] + 1) > (self.CONFIG['map_size'][1] - 1):
            actions.remove('South')

        elif self.getAttribute((state[0], state[1] + 1), 'blocked'):
            actions.remove('South')

        # #Load
        # if state[0] == self.POSITIONS['pizza'][0][0] and state[1] == self.POSITIONS['pizza'][0][1] and state[2] < 2 and state[3] > 0: #and self.PIZZA_CNT < 2:
        #     load_list = ['Load']
        #     actions = load_list

        #     #With this implementation there is a probably a bug when state[3] = 1, because it would make you pick up 2 pizzas (even tho u only need one)

        #Load
        if state[0] == self.POSITIONS['pizza'][0][0] and state[1] == self.POSITIONS['pizza'][0][1] and state[2] < 2: #and self.PIZZA_CNT < 2:
            actions.append('Load')

        #Unload
        #if state == self.POSITIONS['customer1'][0] or state == self.POSITIONS['customer1'][1] or state == self.POSITIONS['customer2']:
        #if self.getAttribute(state, 'unload') and self.PIZZA_CNT > 0:

        if self.CUSTOMERS[state[0]][state[1]] > 0 and state[2] > 0:
            actions.append('Unload')
            # unload_list = ['Unload']
            # actions = unload_list

        return actions
    

    def result(self, state, action):
        '''Returns the state reached from this state when the given action is executed
        '''

        next_state = state #Default Val

        if action == 'West':
            next_state = (state[0] - 1, state[1], state[2], state[3], 0)
            customer_cnt = self.getPendingRequests(next_state)
            next_state = (state[0] - 1, state[1], state[2], state[3], customer_cnt)

        elif action == 'North':
           next_state = (state[0], state[1] - 1, state[2], state[3], 0)
           customer_cnt = self.getPendingRequests(next_state)
           next_state = (state[0], state[1] - 1, state[2], state[3], customer_cnt)

        elif action == 'East':
            next_state = (state[0] + 1, state[1], state[2], state[3], 0)
            customer_cnt = self.getPendingRequests(next_state)
            next_state = (state[0] + 1, state[1], state[2], state[3], customer_cnt)

        elif action == 'South':
            next_state = (state[0], state[1] + 1, state[2], state[3], 0)
            customer_cnt = self.getPendingRequests(next_state)
            next_state = (state[0], state[1] + 1, state[2], state[3], customer_cnt)

        elif action == 'Load':
            customer_cnt = self.getPendingRequests(state)
            next_state = (state[0], state[1], state[2] + 1, state[3], customer_cnt)
            #x,y unchanged, but state[2] "pizza_cnt" +1

        elif action == 'Unload':
            self.CUSTOMERS[state[0]][state[1]] -= 1
            customer_cnt = self.getPendingRequests(state)
            next_state = (state[0], state[1], state[2] - 1, state[3] - 1, customer_cnt- 1 if customer_cnt > 1 else None)
            #x,y unchanged, but state[2] "pizza_cnt" -1 and state[3] "overall_orders" -1

        # print(str(state[0]) + ', '+ str(state[1]) + ': ' + str(action))
        
        return next_state

        # The search algorithm will select a node among the expanded ones (fringe)
        # and repeat from step 3

    def is_goal(self, state):
        '''Returns true if state is the final state
        '''
        self.debugPrint(state)
        return state == self.GOAL
        #State == self.goal is to return to Base (should be final state once orders are fullfilled)

    def cost(self, state, action, state2):
        '''Returns the cost of applying `action` from `state` to `state2`.
           The returned value is a number (integer or floating point).
           By default this function returns `1`.
        '''
        return 1

    def heuristic(self, state):
        '''Returns the heuristic for `state`
        '''
        return 0


    def setup (self):
        '''This method must create the initial state, final state (if desired) and specify the algorithm to be used.
           This values are later stored as globals that are used when calling the search algorithm.
           final state is optional because it is only used inside the is_goal() method

           It also must set the values of the object attributes that the methods need, as for example, self.SHOPS or self.MAXBAGS
        '''

        print '\nMAP: ', self.MAP, '\n'
	print 'POSITIONS: ', self.POSITIONS, '\n'
	print 'CONFIG: ', self.CONFIG, '\n'

        #Calculate Order_Cnt
        x_size = self.CONFIG['map_size'][0]
        y_size = self.CONFIG['map_size'][1]

        customers = [[0 for i in range(y_size)] for j in range(x_size)]
        order_num = 0
        total_order_cnt = 0
        for x in range (x_size):
            for y in range (y_size):
                curr_state = (x,y)
                order_num = self.getInitialRequests(curr_state)
                if order_num == None:
                    order_num = 0
                customers[x][y] += order_num
                total_order_cnt += order_num

        print(customers)
        cust_cnt = None

        initial_state = (self.AGENT_START[0], self.AGENT_START[1], 0, total_order_cnt, cust_cnt)
        #state[0] = x-coordinate, state[1] = y-coordinate, state[2] = pizza_cnt, state[3] = total_order_cnt, state[4] = customer_cnt

        final_state = (self.POSITIONS['pizza'][0][0], self.POSITIONS['pizza'][0][1], 0, 0, None)
        #Tuple if state is location NOT list or dict
        
        #algorithm= simpleai.search.astar
        #algorithm= simpleai.search.breadth_first
        algorithm= simpleai.search.depth_first
        #algorithm= simpleai.search.limited_depth_first

        return initial_state,final_state, algorithm, customers
        
    def printState (self,state):
        '''Return a string to pretty-print the state '''
        
        pps= 'Coordinate: ' + str(state[0]) + ', ' + str(state[1]) + '\n' + 'Pizza Count: ' + str(state[2]) + '\n' + 'Customer Order Count: ' + str(self.CUSTOMERS[state[0]][state[1]]) + '\n' + 'Total Order Count: ' + str(state[3])
        return (pps)

    def getPendingRequests (self,state):
        ''' Return the number of pending requests in the given position (0-N). 
            MUST return None if the position is not a customer.
            This information is used to show the proper customer image.
        '''
        #if state == self.MAP['customer1'][0] or state == self.MAP['customer1'][1] or state == self.MAP['customer2']:
        x = state[0]
        y = state[1]

        if self.CUSTOMERS[x][y] != 0:
            return self.CUSTOMERS[x][y]
        else:
            return None

        #This is only being called at the end? How can it update in real time on the map?


    # --------------- Helper Functions ----------------- 

    def getInitialRequests (self,state):
        #if state == self.MAP['customer1'][0] or state == self.MAP['customer1'][1] or state == self.MAP['customer2']:
        if self.getAttribute(state, 'unload'):
            tileAttributes = self.MAP[state[0]][state[1]][2]
            if 'objects' in tileAttributes.keys():
                return tileAttributes['objects']
        else:
            return None

    def debugPrint(self, state):
        # print('Coordinate: ' + str(state[0]) + ', ' + str(state[1]) + '\n' + 'Pizza Count: ' + str(state[2]) + '\n' + 
        #     'Customer Order Count: ' + str(self.CUSTOMERS[state[0]][state[1]]) + '\n' + 'Total Order Count: ' + str(state[3]) + '\n' + '---------------' + '\n')
        print(state)

        #PROBLEM IS THAT BFS is getting to a point where state (9,0,0,2) has already been found so it will not find path through (4,3,0,2)


    # -------------------------------------------------------------- #
    # --------------- DO NOT EDIT BELOW THIS LINE  ----------------- #
    # -------------------------------------------------------------- #

    def getAttribute (self, position, attributeName):
        '''Returns an attribute value for a given position of the map
           position is a tuple (x,y)
           attributeName is a string
           
           Returns:
               None if the attribute does not exist
               Value of the attribute otherwise
        '''
        tileAttributes=self.MAP[position[0]][position[1]][2]
        if attributeName in tileAttributes.keys():
            return tileAttributes[attributeName]
        else:
            return None

    def getStateData (self,state):
        stateData={}
        pendingItems=self.getPendingRequests(state)
        if pendingItems >= 0:
            stateData['newType']='customer{}'.format(pendingItems)
        return stateData
        
    # THIS INITIALIZATION FUNCTION HAS TO BE CALLED BEFORE THE SEARCH
    def initializeProblem(self,map,positions,conf,aiBaseName):
        self.MAP=map
        self.POSITIONS=positions
        self.CONFIG=conf
        self.AGENT_START = tuple(conf['agent']['start'])

        initial_state,final_state, algorithm, customers = self.setup()
        if initial_state == False:
            print ('-- INITIALIZATION FAILED')
            return True
      
        self.INITIAL_STATE=initial_state
        self.GOAL=final_state
        self.ALGORITHM=algorithm
        self.CUSTOMERS=customers
        super(GameProblem,self).__init__(self.INITIAL_STATE)
            
        print ('-- INITIALIZATION OK')
        return True
        
    # END initializeProblem 
