
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


        #actions is a list []
        actions = list(self.MOVES)

        print(state[0], state[1])

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
        if state == self.POSITIONS['pizza'][0]: #and self.PIZZA_CNT < 2:
            actions.append('Load')

        #Unload
        #if state == self.POSITIONS['customer1'][0] or state == self.POSITIONS['customer1'][1] or state == self.POSITIONS['customer2']:
        #if self.getAttribute(state, 'unload') and self.PIZZA_CNT > 0:

        if self.getAttribute(state, 'unload'): #and self.PIZZA_CNT > 0:
            actions.append('Unload')
            #Check if building needs pizza (Get pending Requests)
            #Prob use"unload": True,

        
        return actions
    

    def result(self, state, action):
        '''Returns the state reached from this state when the given action is executed
        '''

        print(str(action))

        if action == 'West':
            next_state = (state[0]-1, state[1])

        elif action == 'North':
           next_state = (state[0], state[1] - 1)

        elif action == 'East':
            next_state = (state[0]+1, state[1])

        elif action == 'South':
            next_state = (state[0], state[1] + 1)

        elif action == 'Load':
            next_state = state
            self.PIZZA_CNT += 1

        elif action == 'Unload':
            # print(self.MAP[state[0]][state[1]][2])
            # print('original pizza count: ' + str(self.PIZZA_CNT))
            # print('original order count: ' + str(self.ORDER_CNT))
            
            next_state = state
            self.PIZZA_CNT -= 1
            tileAttributes = self.MAP[state[0]][state[1]][2]
            if 'objects' in tileAttributes.keys():
                tileAttributes['objects'] -= 1
            if tileAttributes['objects'] == 0:
                tileAttributes['unload'] = False
            self.ORDER_CNT -= 1

            # print(self.MAP[state[0]][state[1]][2])
            # print('new pizza count: ' + str(self.PIZZA_CNT))
            # print('new order count: ' + str(self.ORDER_CNT))

        else:
            next_state = state #default val

        return next_state

        # The search algorithm will select a node among the expanded ones (fringe)
        # and repeat from step 3

        #Need to define Load, Unload, could probably do this in is_goal?

    def is_goal(self, state):
        '''Returns true if state is the final state
        '''

        return self.ORDER_CNT == 0 #(state == self.GOAL and self.ORDER_CNT == 0)
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


        initial_state = (self.AGENT_START)
        #initial_state[0] = coordinates, #initial_state[1] = pizza_cnt, #initial_state[2] = pizza_cnt, 
        final_state = self.POSITIONS['pizza'][0]
        pizza_cnt = 0
        order_cnt = 0
        for x in range (self.CONFIG['map_size'][0] ):
            for y in range (self.CONFIG['map_size'][1] ):
                curr_state = (x,y)
                order_num = self.getPendingRequests(curr_state)
                if order_num == None:
                    order_num = 0
                order_cnt += order_num
                #print(str(x) + ' ,' + str(y) + 'order count: ' + str(order_cnt)) #FOR TESTING PURPORSES


        #Tuple if state is location NOT list or dict
        
        #algorithm= simpleai.search.astar
        algorithm= simpleai.search.breadth_first
        #algorithm= simpleai.search.depth_first
        #algorithm= simpleai.search.limited_depth_first

        return initial_state,final_state, pizza_cnt, order_cnt, algorithm
        
    def printState (self,state):
        '''Return a string to pretty-print the state '''
        
        pps= '\n' + 'Pizza Count: ' + str(self.PIZZA_CNT) + '\n' + 'Order Count: ' + str(self.ORDER_CNT)
        return (pps)

    def getPendingRequests (self,state):
        ''' Return the number of pending requests in the given position (0-N). 
            MUST return None if the position is not a customer.
            This information is used to show the proper customer image.
        '''
        #if state == self.MAP['customer1'][0] or state == self.MAP['customer1'][1] or state == self.MAP['customer2']:
        if self.getAttribute(state, 'unload'):
            tileAttributes = self.MAP[state[0]][state[1]][2]
            if 'objects' in tileAttributes.keys():
                return tileAttributes['objects']
        else:
            return None

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

        initial_state,final_state,pizza_cnt, order_cnt, algorithm = self.setup()
        if initial_state == False:
            print ('-- INITIALIZATION FAILED')
            return True
      
        self.INITIAL_STATE=initial_state
        self.GOAL=final_state
        self.PIZZA_CNT = pizza_cnt
        self.ORDER_CNT = order_cnt
        self.ALGORITHM=algorithm
        super(GameProblem,self).__init__(self.INITIAL_STATE)
            
        print ('-- INITIALIZATION OK')
        return True
        
    # END initializeProblem 
