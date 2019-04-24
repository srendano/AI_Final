
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
        
        #Series of If statements? Like if you can move West, then add that to list of actions

        #I assume this is imposed by a constraint (i.e. you can / can't move this way because of this)

        #USE getAttribute(<position>,<key>) to check vals in attribute section of map
        #and decide type of terrain, num or orders


        # self.CONFIG['map_size'][0] -> x-coordinate (max) east-most
        # self.CONFIG['map_size'][1] -> y-coordinate (max) south-most


        #actions is a list []
        actions = list(MOVES);

        #West
        if (state[0] - 1) < 0 or getAttribute(state[0] -1 , state[1]) == 'building':
            actions.remove('West')

        #North
        if (state[1] - 1) < 0 or getAttribute(state[0] , state[1] - 1) == 'building':
            actions.remove('North')

        #East
        if (state[1] - 1) > self.CONFIG['map_size'][0] or getAttribute(state[0] + 1, state[1]) == 'building':
            actions.remove('East')

        #South
        if(state[1] + 1) > self.CONFIG['map_size'][1] or getAttribute(state[0] , state[1] + 1) == 'building':
            actions.remove('South')
        
        return actions
    

    def result(self, state, action):
        '''Returns the state reached from this state when the given action is executed
        '''


        #Expands curr node; return new state reached executing specified action in curr state

        #How is the action parameter picked? Presumably an output of the algorithm, but how does that work?

        if action == 'West':
            next_state = (state[0]-1, state[1])

        elif action == 'North':
           next_state = (state[0], state[1] - 1)

        elif action == 'East':
            next_state = (state[0]+1, state[1])

        elif action == 'South':
            next_state = (state[0], state[1] + 1)

        # next_state = 0 #MODIFY 

        return next_state

        # The search algorithm will select a node among the expanded ones (fringe)
        # and repeat from step 3

        #Need to define Load, Unload, could probably do this in is_goal?

    def is_goal(self, state):
        '''Returns true if state is the final state
        '''
        #Compare state to self.goal
        return state == self.goal; 

        #MAYBE return to base after?

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


        initial_state = self.AGENT_START
        final_state= (0,1) 

        #Tuple if state is location NOT list or dict
        
        # initial_state = None
        # final_state= None
        algorithm= simpleai.search.astar
        #algorithm= simpleai.search.breadth_first
        #algorithm= simpleai.search.depth_first
        #algorithm= simpleai.search.limited_depth_first

        return initial_state,final_state,algorithm
        
    def printState (self,state):
        '''Return a string to pretty-print the state '''
        
        pps=''
        return (pps)

    def getPendingRequests (self,state):
        ''' Return the number of pending requests in the given position (0-N). 
            MUST return None if the position is not a customer.
            This information is used to show the proper customer image.
        '''
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

        initial_state,final_state,algorithm = self.setup()
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

