
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

        #Load
        load_state = (state[0], state[1])
        if load_state in self.POSITIONS['pizza'] and state[2] < 2:
            actions.append('Load')

        #Unload

        #if (state in self.POSITIONS['customer1'] or state in self.POSITIONS['customer2']) and state[2] > 0:
        unload_state = (state[0], state[1])
        unload_dict = dict(state[4])
        if unload_state in unload_dict:
            if unload_state in self.CUSTOMERS and state[2] > 0 and state[3] > 0 and unload_dict[unload_state] > 0:
           	    actions.append('Unload')

        return actions


    def result(self, state, action):
        '''Returns the state reached from this state when the given action is executed
        '''

        next_state = state #Default Val

        if action == 'West':
            next_state = (state[0] - 1, state[1], state[2], state[3], state[4])

        elif action == 'North':
           next_state = (state[0], state[1] - 1, state[2], state[3], state[4])

        elif action == 'East':
            next_state = (state[0] + 1, state[1], state[2], state[3], state[4])

        elif action == 'South':
            next_state = (state[0], state[1] + 1, state[2], state[3], state[4])

        elif action == 'Load':
            next_state = (state[0], state[1], state[2] + 1, state[3], state[4])
            #x,y unchanged, but state[2] "pizza_cnt" +1

        elif action == 'Unload':
            unload_state = (state[0], state[1])
            unload_dict = dict(state[4])
            unload_dict[unload_state] -= 1
            items = unload_dict.items()
            new_state = tuple(items)

            next_state = (state[0], state[1], state[2] - 1, state[3] - 1, new_state)
            #x,y unchanged, but state[2] "pizza_cnt" -1 and state[3] "overall_orders" -1

        return next_state

        # The search algorithm will select a node among the expanded ones (fringe)
        # and repeat from step 3

    def is_goal(self, state):
        '''Returns true if state is the final state
        '''
        #self.debugPrint(state)
        return state == self.GOAL

    def cost(self, state, action, state2):
        '''Returns the cost of applying `action` from `state` to `state2`.
           The returned value is a number (integer or floating point).
           By default this function returns `1`.
        '''

        #Implementation for Costs / Load
        # if(state[2] == 1):
        #     return 2
        # if(state[2] == 2):
        #     return 10
        # else:
        #     return 1

        return self.getAttribute(state, 'cost')

    def heuristic(self, state):
        '''Returns the heuristic for `state`
        '''

# #----H1 - Admissible ------------------------------------------------------
#         if state[2] < state[3]:
#             customer_distance = []
#             customer_dictionary = dict(state[4])

#             farthest_customer = 0
#             cust_calc = 0
#             cust_coord = [0 for x in range(2)]

#             for cust_state in customer_dictionary:
#                 if customer_dictionary[cust_state] != 0:
#                     cust_calc = abs(cust_state[0] - state[0]) + abs(cust_state[1] - state[1])
#                     customer_distance.append(cust_calc)
#                 if cust_calc > farthest_customer:
#                     farthest_customer = cust_calc
#                     cust_coord[0] = cust_state[0]
#                     cust_coord[1] = cust_state[1]

#             pizza_shops = []
#             pizza_calc = 0
#             closest_pizza = 0
#             pizza_coord = [0 for x in range(2)]

#             for pizzaState in self.POSITIONS['pizza']:
#                 pizza_calc = abs(pizzaState[0] - state[0]) + abs(pizzaState[1] - state[1])
#                 pizza_shops.append(pizza_calc)
#                 if pizza_calc < closest_pizza:
#                     closest_pizza = pizza_calc
#                     pizza_coord[0] = pizzaState[0]
#                     pizza_coord[1] = pizzaState[1]


#             pizza_to_base = abs(pizza_coord[0] - self.AGENT_START[0]) + abs(pizza_coord[1] - self.AGENT_START[1])
#             cust_to_base = abs(cust_coord[0] - self.AGENT_START[0]) + abs(cust_coord[1] - self.AGENT_START[1])

#             base_distance = min(pizza_to_base, cust_to_base)


#             return max(closest_pizza, farthest_customer) + base_distance

#         elif state[3] > 0:
#             customer_distance = []
#             customer_dictionary = dict(state[4])

#             farthest_customer = 0
#             cust_calc = 0
#             cust_coord = [0 for x in range(2)]

#             for cust_state in customer_dictionary:
#                 if customer_dictionary[cust_state] != 0:
#                     cust_calc = abs(cust_state[0] - state[0]) + abs(cust_state[1] - state[1])
#                     customer_distance.append(cust_calc)
#                 if cust_calc > farthest_customer:
#                     farthest_customer = cust_calc
#                     cust_coord[0] = cust_state[0]
#                     cust_coord[1] = cust_state[1]

#             base_distance = abs(cust_coord[0] - self.AGENT_START[0]) + abs(cust_coord[1] - self.AGENT_START[1])

#             return farthest_customer + base_distance

#         else:
#             return 0



# #----H2 - Admissible ------------------------------------------------------
#         if state[2] < state[3]:
#             customer_distance = []
#             customer_dictionary = dict(state[4])

#             for cust_state in customer_dictionary:
#                  if customer_dictionary[cust_state] != 0:
#                      customer_distance.append(abs(cust_state[0] - state[0]) + abs(cust_state[1] - state[1]))
#             farthest_customer = max(customer_distance)

#             pizza_shops = []
#             for pizzaState in self.POSITIONS['pizza']:
#                 pizza_shops.append(abs(pizzaState[0] - state[0]) + abs(pizzaState[1] - state[1]))
#             closest_pizza = min(pizza_shops)

#             return max(closest_pizza, farthest_customer)

#         elif state[3] > 0:
#             customer_distance = []
#             customer_dictionary = dict(state[4])

#             for cust_state in customer_dictionary:
#                  if customer_dictionary[cust_state] != 0:
#                      customer_distance.append(abs(cust_state[0] - state[0]) + abs(cust_state[1] - state[1]))
#             return max(customer_distance)

#         else:
#             return 0



# #----H3 - Admissible ------------------------------------------------------
#         return abs(state[0] - self.AGENT_START[0]) + abs(state[1] - self.AGENT_START[1])



#----H4 - NOT Admissible ------------------------------------------------------
        customer_distance = 0
        customer_dictionary = dict(state[4])

        for cust_state in customer_dictionary:
            if customer_dictionary[cust_state] != 0:
                customer_distance += abs(cust_state[0] - state[0]) + abs(cust_state[1] - state[1])

        return customer_distance


    def setup (self):
        '''This method must create the initial state, final state (if desired) and specify the algorithm to be used.
           This values are later stored as globals that are used when calling the search algorithm.
           final state is optional because it is only used inside the is_goal() method

           It also must set the values of the object attributes that the methods need, as for example, self.SHOPS or self.MAXBAGS
        '''

        print '\nMAP: ', self.MAP, '\n'
	print 'POSITIONS: ', self.POSITIONS, '\n'
	print 'CONFIG: ', self.CONFIG, '\n'

        #Calculate Total_Order_Cnt
        x_size = self.CONFIG['map_size'][0]
        y_size = self.CONFIG['map_size'][1]

        order_num = 0
        total_order_cnt = 0
        for x in range (x_size):
            for y in range (y_size):
                curr_state = (x,y)
                order_num = self.getInitialRequests(curr_state)
                if order_num != None:
                    total_order_cnt += order_num

        customers_list = [ ]
        if 'customer1' in self.POSITIONS:
            for state in self.POSITIONS['customer1']:
                customers_list.append(state)
        if 'customer2' in self.POSITIONS:
            for state in self.POSITIONS['customer2']:
                customers_list.append(state)
        if 'customer3' in self.POSITIONS:
            for state in self.POSITIONS['customer3']:
                customers_list.append(state)

        customers = tuple(customers_list)
        self.CUSTOMERS = customers

        customers_dict = { }
        if 'customer1' in self.POSITIONS:
            for state in self.POSITIONS['customer1']:
                customers_dict[state] = 1
        if 'customer2' in self.POSITIONS:
            for state in self.POSITIONS['customer2']:
                customers_dict[state]  = 2
        if 'customer3' in self.POSITIONS:
            for state in self.POSITIONS['customer3']:
                customers_dict[state]  = 3

        items = customers_dict.items()
        customer_cnt = tuple(items)

        initial_state = (self.AGENT_START[0], self.AGENT_START[1], 0, total_order_cnt, customer_cnt)
        #state[0] = x-coordinate, state[1] = y-coordinate, state[2] = pizza_cnt, state[3] = total_order_cnt, state[4] = tuple list of customers and quantities (((4,3),2), ((9,1),1) ... )

        final_dict = { }
        if 'customer1' in self.POSITIONS:
            for state in self.POSITIONS['customer1']:
                final_dict[state] = 0
        if 'customer2' in self.POSITIONS:
            for state in self.POSITIONS['customer2']:
                final_dict[state]  = 0
        if 'customer3' in self.POSITIONS:
            for state in self.POSITIONS['customer3']:
                final_dict[state]  = 0

        final_items = final_dict.items()
        final_customer_cnt = tuple(final_items)

        final_state = (self.AGENT_START[0], self.AGENT_START[1], 0, 0, final_customer_cnt)

        #algorithm= simpleai.search.astar
        algorithm= simpleai.search.breadth_first
        #algorithm= simpleai.search.depth_first

        return initial_state,final_state, algorithm

    def printState (self,state):
        '''Return a string to pretty-print the state '''

        pps= 'Coordinate: ' + str(state[0]) + ', ' + str(state[1]) + '\n' + 'Pizza Count: ' + str(state[2]) + '\n' + 'Total Order Count: ' + str(state[3])
        return (pps)

    def getPendingRequests (self,state):
        ''' Return the number of pending requests in the given position (0-N).
            MUST return None if the position is not a customer.
            This information is used to show the proper customer image.
        '''

        check_state = (state[0], state[1])
        if check_state in self.CUSTOMERS:
            check_dict = dict(state[4])
            return check_dict[check_state]
        else:
            return None

    # --------------- Helper Functions -----------------

    def getInitialRequests (self,state):
        #if state == self.MAP['customer1'][0] or state == self.MAP['customer1'][1] or state == self.MAP['customer2']:
        if self.getAttribute(state, 'unload'):
            tileAttributes = self.MAP[state[0]][state[1]][2]
            if 'objects' in tileAttributes.keys():
                return tileAttributes['objects']
        else:
            return None

    #def debugPrint(self, state):
        # print('Coordinate: ' + str(state[0]) + ', ' + str(state[1]) + '\n' + 'Pizza Count: ' + str(state[2]) + '\n' +
        #     'Customer Order Count: ' + str(self.CUSTOMERS[state[0]][state[1]]) + '\n' + 'Total Order Count: ' + str(state[3]) + '\n' + '---------------' + '\n')
        #print(state)
        #PROBLEM IS THAT BFS is getting to a point where state (9,0,0,2) has already been found so it will not find path through (4,3,0,2)

        #Still a problem because a state with no cust_count may be necessary to traverse on the path


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

        initial_state,final_state, algorithm = self.setup()
        if initial_state == False:
            print ('-- INITIALIZATION FAILED')
            return True

        self.INITIAL_STATE=initial_state
        self.GOAL=final_state
        self.ALGORITHM=algorithm
        super(GameProblem,self).__init__(self.INITIAL_STATE)

        print ('-- INITIALIZATION OK')
        return True

    # END initializeProblem