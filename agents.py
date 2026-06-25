import math
import random

from mesa.discrete_space import CellAgent, FixedAgent

from params import Params


params = Params()


# Distance between a cell and another cell
def distance_cell(cell_1,cell_2):
    x_1 = cell_1.coordinate[0]
    y_1 = cell_1.coordinate[1]

    x_2 = cell_2.coordinate[0]
    y_2 = cell_2.coordinate[1]

    d_x = abs(x_1-x_2)
    d_y = abs(y_1-y_2)

    return max(d_x, d_y)

# change at constant x rate
def change_at_constant_rate(A, x, t):
    '''
    A: Initial value
    x: annual change rate
    t: step number
    '''
    return A*pow(1+x, t)
    

# T年間でｘだけ減少する場合の年間減少率計算
def calculate_annual_decrease_rate(T, x):
    '''
    T年間で x の割合だけ減少する場合，年間平均減少率を返す
    '''
    return 1 -pow(1-x, 1/T)

def neighbor_fuel_field(h, r=1):
    '''
    h: Human agent
    '''
    fuel_agent_list=[]
    neighbor_cells=h.cell.get_neighborhood(radius=r, include_center=False)

    if h.coal_favor:
        for c in list(neighbor_cells):
            for a in c.agents:
                if isinstance(a, Field):
                    if a.type=='Mine':
                        if a.size>0:
                            fuel_agent_list.append(a)    
        return fuel_agent_list

    else:
        for c in list(neighbor_cells):
            for a in c.agents:
                if isinstance(a, Field):
                    if a.type=='Forest':
                        if a.size>0:
                            fuel_agent_list.append(a)    
        return fuel_agent_list
    

# Underconst.
def neighbor_forest(h, r=1):
    '''
    Return neighbor forest field list
    '''
    forest_list=[]
    neighbor_cells=h.cell.get_neighborhood(radius=r, include_center=False)

    for c in list(neighbor_cells):
        for a in c.agents:
            if isinstance(a, Field):
                if a.type=='Forest':
                    if a.size>0:
                        forest_list.append(a)

    return forest_list            
    

# Underconst.
def neighbor_mine(h, r=1):
    '''
    Return neighbor mine field list
    '''
    mine_list=[]
    neighbor_cells=h.cell.get_neighborhood(radius=r, include_center=False)

    for c in list(neighbor_cells):
        for a in c.agents:
            if isinstance(a, Field):
                if a.type=='Mine':
                    if a.size>0:
                        mine_list.append(a)

    return mine_list
    

# Cost function of coal mining (extraction cost)
def cost_of_mining(x, const=params.a_0, coeff=params.a_1, expo=params.a_2):
    return const + coeff*pow(x, expo)


## for history list
def history_sequence(l:list, r:int, x):
    '''
    リストオブジェクトの後ろからr個連続で要素がxだったらTrueを返す
    '''
    if len(l)>=r:
        for i in range(r):
            z = l[-(i+1)]
            if z==x:
                continue
            else:
                return False

        return True
            
            
    else:
        return False
    

class Human(CellAgent):
    
    def __init__(self,model,cell=None,
                coal_ratio=params.coal_ratio):
        super().__init__(model)
        self.cell=cell
        self.metabo=params.metabo
        self.bmr=params.bmr
        self.eta=params.eta_Human
        self.energy = 0
        self.food =0
        #self.food_needs_pc =1   #Food needs per capita
        self.num = 0  # human number in the cell
        self.fuel_needs = 0
        self.fuel_needs_pc = params.fuel_needs_pc   #Fuel needs per capita
        self.fuel=0
        self.target_cell=None
        self.farm=None

        
        self.coal_ratio=coal_ratio   # If coal_favor =True
        self.wood_needs=0
        self.coal_needs=0
        self.wood=0
        self.coal=0

        # about Coal
        self.coal_favor=False  
        #self.coal_favor=random.choice([True,False])  #石炭を使うか否か              
        #self.capital_cost=0     #capital_costの割当コスト
        self.doll=False

        #self.annual_wood_consumption=0
        #self.annual_coal_consumption=0

        # TODO
        self.tr_EI_coal=0  # energy-invested for transportation of coal
        self.o_EI_coal=0   # energy-invested for other work of coal 
        self.tr_EI_wood=0  # energy-investef for transportatino of wood
        self.o_EI_wood=0   # energy-invested for other work of wood
        self.mileage_coal=0  # mileage for coal 
        self.mileage_wood=0  # mileage for wood        
        
        

    #########################
    # Cultivate my cell into farm
    def cultivate(self):
        if self.cell is None:
            return  
            
        for a in self.cell.agents:
            if isinstance(a, Field):
                if a.type=='Farm':
                    a.whose=self
                    self.farm=a
                    a.update_attribute()
                elif a.type=='Forest' and a.cultivable:                    
                    a.type='Farm'
                    a.whose=self
                    self.farm=a
                    a.update_attribute
                    # UNDERCONST. energy loss for cultivation                                    
                    

    
                    
    ########################
    # Collect foods and eat
    def collect_eat_food(self):
        self.num=0
        self.food=0
        energy_cost=0
        for a in self.cell.agents:
            if isinstance(a,Field):
                if a.type=='Farm' and a.size >0:
                    self.num= a.size/self.metabo
                    #self.food= min(self.metabo, a.size)
                    self.food=a.size
                    energy_cost = a.extraction_cost*self.food
                    a.size -= self.food
                    break

        self.energy=max((self.metabo-self.bmr)*self.food*self.eta - energy_cost,0)
        


    
    #################
    def collect_fuel(self):
        self.update_fuel_demand()
        self.collect_wood()
        if self.coal_favor:
            self.collect_coal()

        self.fuel=self.wood+self.coal

        self.dead_or_alive() 
        


        

    
    ########################
    def update_fuel_demand(self):
        '''
        Run after determine self.num (=population)
        '''
        self.fuel_needs=self.fuel_needs_pc*self.num
        self.fuel=0
        
        if self.coal_favor:
            self.wood_needs=self.fuel_needs*(1-self.coal_ratio)
            self.coal_needs=self.fuel_needs*self.coal_ratio
        else:
            self.wood_needs=self.fuel_needs
            self.coal_needs=0
            
    
        

    
    ####################
    def collect_wood(self):
        '''
        Collect firewood.
        '''
        self.wood=0
        self.tr_EI_wood=0
        self.o_EI_wood=0
        self.mileage_wood=0

        shortage=self.wood_needs
        list_1=neighbor_forest(self, params.neighbor_radius)
        count=0

        while shortage>0 and self.energy>0 and len(list_1)>0 and count<pow(2*params.neighbor_radius+1,2):
            list_2=sorted(list_1, key=lambda f: self.fuel_cost(f))
            f=list_2[0]
            l=self.fuel_production_plan(f)
            self.wood += l[1]
            shortage=max(self.wood_needs-self.wood, 0)
            self.energy -= l[0]
            f.size -= l[2]

            self.tr_EI_wood += l[3]
            self.o_EI_wood += l[4]
            self.mileage_wood += distance_cell(self.cell, f.cell)*l[1]
            
            
            list_1=neighbor_forest(self, params.neighbor_radius)
            
            count +=1

        

    
    ###################
    def collect_coal(self):
        '''
        Collect coal
        '''
        self.coal=0
        self.tr_EI_coal=0
        self.o_EI_coal=0
        self.mileage_coal=0        
        
        shortage=self.coal_needs
        list_1=neighbor_mine(self, params.neighbor_radius)
        count=0

        while shortage>0 and self.energy>0 and len(list_1)>0 and count<pow(2*params.neighbor_radius+1,2):
            list_2=sorted(list_1, key=lambda f: self.fuel_cost(f))
            f=list_2[0]
            l=self.fuel_production_plan(f)
            self.coal += l[1]
            shortage=max(self.coal_needs-self.coal, 0)
            self.energy -= l[0]
            f.size -= l[2]
            if l[2] > 0:
                f.mine_state = 'Mined'


            self.tr_EI_coal += l[3]
            self.o_EI_coal += l[4]
            self.mileage_coal += distance_cell(self.cell, f.cell)*l[1]
            
            
            list_1=neighbor_mine(self, params.neighbor_radius)
            
            count +=1
    
         

        

    
    ######################
    def fuel_cost(self, f):
        l=self.fuel_production_plan(f)
        if l[1]<=0:
            return math.inf
        else:
            return l[0]/l[1]
    

    

    #TODO
    #####################################
    def fuel_production_plan(self, f):
        '''
        return [w,y,z, w_tr, w_o]

        w: 投じたエネルギー
        y: 正味採取量
        z: 全採取量
        w_tr: 輸送に投じたエネルギー
        w_0:  その他の作業（採掘、機械操作等）に投じたエネルギー
        '''
        c_0=f.transportation_cost*distance_cell(self.cell,f.cell)
        c_1=f.extraction_cost
        
        z_1=max(f.size, 0) #fuelのポテンシャル
        if f.type=='Forest':
            y_2=max(self.wood_needs-self.wood,0) #wood shortage
        elif f.type=='Mine':
            y_2=max(self.coal_needs-self.coal, 0)  #coal shortage
        else:
            y_2=0

        if f.type=='Forest':
            y_1=z_1
            y_3=(1/(c_0+c_1))*self.energy
            y=min(y_1, y_2, y_3)
            z=y
            w=(c_0+c_1)*y
            w_tr=c_0*y
            w_o=w-w_tr
            return [w,y,z,w_tr,w_o]
        elif f.type=='Mine':                        
            y_1=z_1
            y_3=(1/(c_0+c_1))*self.energy
            y=min(y_1,y_2,y_3)
            z=y
            w=(c_0+c_1)*y 
            w_tr=c_0*y
            w_o=w-w_tr
            return [w,y,z,w_tr,w_o]
        else:
            return [0,0,0,0,0]  
                 
    

    
    ########################
    # Off-spring
    def off_spring(self):

        self.target_cell=None
        self.energy=max(0, self.energy)
        ofs_prb = self.energy/(self.metabo*self.num)
        if random.random()<ofs_prb:
            self.set_target_cell()

        if self.target_cell is not None:
            self.fight()
            if self.target_cell is not None:
                o = Human(self.model, self.target_cell)
                #o.cell=self.target_cell 
                o.cultivate()
                if random.random()>params.mutant_rate:
                    o.coal_favor=self.coal_favor
                    o.coal_ratio = self.coal_ratio
                else:
                    o.coal_favor=random.choice([True, False])
                    o.coal_ratio = random.uniform(0.01, params.coal_ratio)

            



    def dead_or_alive(self):
        '''
        燃料がニーズに足りないほど，死ぬ確率が高まる
        '''
        if self.fuel_needs>0:        
            z= max(self.fuel_needs -self.fuel,0)/self.fuel_needs
            if z>random.random():
                if self.farm is not None:
                    if self.farm.whose is not None:
                        self.farm.whose = None
                    self.farm = None
                self.remove()
        else:
            if self.farm is not None:
                if self.farm.whose is not None:
                    self.farm.whose = None
                self.farm = None
            self.remove()
            
        
        
    
            

    ########################    
    def set_target_cell(self):
        
        if self.cell is None:
            self.target_cell = None
            return  # セルが未割り当ての場合はターゲット設定をスキップ
        
        #self.target_cell = None
        target_Forest =[]
        target_Farm=[]
        target_Farm_2=[]
        target_Farm_without_Human =[]
        neighbor_cells = self.cell.get_neighborhood(radius=params.target_area, include_center=False)
        for c in list(neighbor_cells):
            for a in c.agents:
                if isinstance(a, Field) and a.type=='Forest' and a.cultivable:
                    target_Forest.append(a)
                elif isinstance(a, Field) and a.type=='Farm':
                    target_Farm.append(a)
                else:
                    pass

        target_Farm_2 = sorted(target_Farm,key=lambda f: self.investigate_energy(f.cell))

        for f in target_Farm:
            if f.whose is None:
                target_Farm_without_Human.append(f)
                
                
        if len(target_Farm_without_Human)>0:
            f=random.choice(target_Farm_without_Human)
            self.target_cell=f.cell        
        elif len(target_Forest)>0:
            f = random.choice(target_Forest)
            self.target_cell = f.cell
        elif len(target_Farm_2)>0:
            f=target_Farm_2[0]
            self.target_cell=f.cell
        else:
            self.target_cell = None


    
    ########################
    def investigate_energy(self, cell):
        z=0
        for a in cell.agents:
            if isinstance(a, Human):
                z += a.energy
        return z


    
    ########################
    def fight(self):
        if self.energy<=0:
            self.target_cell=None
        elif self.investigate_energy(self.target_cell) <=0:
            self.remove_Human_in_the_cell(self.target_cell)
        else:
            z = self.investigate_energy(self.target_cell)
            p = self.energy/(self.energy+z)
            if random.random()<p:
                self.remove_Human_in_the_cell(self.target_cell)
            else:
                self.target_cell=None
                self.energy=0
                self.remove_Human_in_the_cell(self.cell)

        

    ########################
    def remove_Human_in_the_cell(self, cell):
        for a in cell.agents:
            if isinstance(a, Human):
                if a.farm is not None:
                    a.farm.whose = None
                    a.farm = None
                a.remove()
                

   

    # TODO
    ########################
    def update_doll(self):
        pass

    
    
        
    #############
    ### STEPS ###
    #############
    
    def step_01(self):
        #self.cultivate()
        self.collect_eat_food()

    def step_02(self):
        self.collect_fuel()
        
    def step_03(self):
        self.off_spring()

    def step_04(self):
        #self.dead_or_alive()
        pass
        

class Field(FixedAgent):

    def __init__(self,model,cell):
        super().__init__(model)
        
        self._type='Forest'  
        '''
            Forest: 森林，薪採取可能．耕作は可能or不可能
            Farm: 耕地（食料生産兼居住地）
            Mine: 炭鉱．燃料採取可能．耕作は不可能
            Desert: 不毛地．燃料採取不可能，食料生産（及び居住）不可能．
            Waste: 放棄地．しばらくは不毛だが，やがて森林に回復
        '''
        
        self.cell = cell

        self.potential_Wood=params.potential_Wood
        self.extraction_cost_Wood=params.ex_cost_Wood
        self.transportation_cost_Wood=params.tr_cost_Wood

        self.potential_Food=params.potential_Food
        self.extraction_cost_Food=params.ex_cost_Food

        self.initial_stock_Coal=params.init_stock_Coal
        self.transportation_cost_Coal=params.tr_cost_Coal        
        

        
        self.potential = self.potential_Wood
        self.size = self.potential
        self.extraction_cost = self.extraction_cost_Wood
        self.transportation_cost = self.transportation_cost_Wood
        #self.update_attribute()

        self.annual_wood_production=0
        self.annual_food_production=0
                
        self.whose=None
        self.history=[0]

        #for coal mine
        self.mine_initialize(self.initial_stock_Coal)

        # Can be cultivated?
        self.cultivable = False

        # Decrease of Transportation cost
        self.dec_rate = calculate_annual_decrease_rate(params.interval, params.dec_rate)
        self.both = params.both
        

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, t:str) -> None:
        self._type=t



    #####################
    def mine_initialize(self, stock):
        self.initial_stock=stock
        self.current_stock=self.initial_stock
        self.annual_coal_production=0
        self.cumulative_production=0 
        self.coal_history=[0]
        #self.coal_user_num=0   # Number of coal users of this mine, at current step.
        self.latent_coal_users=[]  # latent coal users
        self.coal_users=[]  #a ctual coal users
        self.mine_state='Untapped'   #  'Mined', 'Abandoned'  , 'Exhausted'  
        
        
        

    ##########################
    def update_attribute(self):
        if self._type=='Forest':
            self.potential = self.potential_Wood
            self.extraction_cost=self.extraction_cost_Wood
            self.transportation_cost=self.transportation_cost_Wood
        elif self._type=='Farm':
            self.potential=self.potential_Food
            self.extraction_cost=self.extraction_cost_Food
            self.transportation_cost=0
        elif self._type=='Mine':
            self.mine_state='Untapped'
            self.size = self.current_stock
            self.extraction_cost = cost_of_mining(self.cumulative_production)        
            self.transportation_cost=self.transportation_cost_Coal
        elif self._type=='Desert':
            self.potential=0
            self.size=0
            #self.cultivable=False
        elif self._type=='Waste':
            self.potential=0
            self.size=0
        else:
            pass
        
     
                    
            
        
    ######################
    def update_stock(self):
        self.grow()
        self.update_coal_stock()
        
            
    #######################
    def grow(self):
        self.annual_food_production=0
        if self._type=='Farm':
            self.annual_food_production=max(self.potential-self.size,0)
            self.size = self.potential_Food
        
        self.annual_wood_production=0
        if self._type=='Forest':
            self.annual_wood_production=max(self.potential-self.size,0)
            self.size = self.potential_Wood


    #######################
    def update_coal_stock(self):
        self.annual_coal_production=0
        if self._type=='Mine':
            self.annual_coal_production=max(self.current_stock-self.size,0)
            self.current_stock=self.size
            self.cumulative_production=max(0, self.initial_stock-self.current_stock)

       

    ######################
    def update_history(self):
        if self._type=='Waste':
            self.history.append(2)
        elif self._type=='Farm' and self.whose is None:
            self.history.append(1)
        else:
            self.history.append(0)

        if len(self.history)>params.lead_time_restration+1:
            del self.history[0]
        

    

    #######################
    def update_coal_history(self): 
        
        if self.cumulative_production>0:
            #self.is_mined=True
            self.mine_state='Mined'

        #if self.is_mined:
        if self.mine_state=='Mined':
            self.coal_history.append(self.cumulative_production)
        
        if self.current_stock <=0:
            #self._type='Forest'
            self.mine_state='Exhausted'
            #self._tyep='Forest'
        


    ##########################
    def farm_into_waste(self):
        if history_sequence(self.history, params.lead_time_ignored_farm_into_waste, 1):
            self._type='Waste'


    #########################
    def back_to_forest(self):
        if history_sequence(self.history, params.lead_time_restration,2):
            self._type='Forest'

        
            
    
    #######################
    def check_abandoned(self):
        if self.mine_state !='Exhausted':
            if len(self.coal_history)>10:
                l = self.coal_history[::-1]
                z = l[0]
                for i in range(10):
                    if abs(l[0]-l[i])>0.01:
                        return 
                    else:
                        continue
                        
                #self._type='Forest'
                self.mine_state='Abandoned'
        



    
    #########################
    def update_doll(self):
        if self._type=='Mine':
            neighbor_cells=self.cell.get_neighborhood(radius=1, include_center=False)
            for c in neighbor_cells:
                for a in c.agents:
                    if isinstance(a, Human):
                        a.doll=True
                    


    def update_transportation_cost(self):
        '''
        annual decrease rate: self.dec_rate
        both: True: coal and firewood,  False coal only
        '''
        if self.both:
            self.transportation_cost_Wood *= (1-self.dec_rate)
            self.transportation_cost_Coal *= (1-self.dec_rate)
        else:
            self.transportation_cost_Coal *= (1-self.dec_rate)
            
    


    ###################
    ##### STEPS #######
    ###################

    def step_00(self):
        self.update_transportation_cost()
    
    def step_01(self):
        self.coal_users=[]
        self.update_attribute()

    def step_02(self):
        self.update_stock()

    def step_03(self):
        self.update_history()
        self.update_coal_history()
        self.farm_into_waste()
        self.back_to_forest()
        #self.check_abandoned()
        self.update_doll()
                    
