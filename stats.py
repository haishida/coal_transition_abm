"""Statistics functions for Mesa DataCollector."""

from agents import Field, Human


### for DataCollector ###

def stat_population(model):
    if Human in model.agents_by_type:
        human_list = model.agents_by_type[Human]
    else:
        human_list = []

    human_list_2=[]
    for h in human_list:
        if not h.doll:
            human_list_2.append(h)

    z=0
    for h in human_list_2:
        z += h.num

    return z

def stat_mine_in_use(model):
    if Field in model.agents_by_type:
        f_list=model.agents_by_type[Field]
        l=[]
        for f in f_list:
            if f.mine_state=='Mined':
                l.append(f)
    else:
        l=[]

    return len(l)
   

def stat_cumulative_production(model):
    '''
    Total cumulative coal production
    '''
    z=0
    if Field in model.agents_by_type:
        for f in model.agents_by_type[Field]:
            z += f.cumulative_production
    else:
        z=0

    return z       

def stat_annual_coal_production(model):
    '''
    Sum of annual coal production EXCEPT dolls
    '''
    z=0
    if Human in model.agents_by_type:
        for h in model.agents_by_type[Human]:
            if not h.doll:
                z += h.coal
    else:
        z=0

    return z

        
def stat_annual_wood_production(model):
    '''
    Sum of annual wood production EXCEPT dolls
    '''
    if Human in model.agents_by_type:
        z=0
        for h in model.agents_by_type[Human]:
            if not h.doll:
                z += h.wood
        return z
    else:
        return 0    


def stat_coal_share(model):
    '''
    return coal share, except dolls
    '''
    wood=0
    coal=0
    if Human in model.agents_by_type:
        for h in model.agents_by_type[Human]:
            if not h.doll:
                wood += h.wood
                coal += h.coal
                
        total = wood+coal
        if total>0:
            return  coal/total
        else:
            return 0
    else:
        return 0



def stat_coal_favor_share(model):
    '''
    Coal favor の割合を返す
    '''
    count = 0
    pop = 0
    if Human in model.agents_by_type:
        for h in model.agents_by_type[Human]:
            if not h.doll:
                pop +=1
                if h.coal_favor:
                    count += 1

    if pop >0:
        return count/pop
    else:
        return 0
        



def stat_average_coal_ratio(model):
    '''
    coal_ratio の平均値を返す（coal favor のみ対象）
    '''
    count =0
    z=0
    if Human in model.agents_by_type:
        for h in model.agents_by_type[Human]:
            if not h.doll and h.coal_favor:
                count +=1
                z += h.coal_ratio

    if count ==0:
        return 0
    else:
        return z/count
        
    

def stat_average_cost_coal(model):
    '''
    Average energy-invested on coal production per MJ, except dolls
    '''
    if Human in model.agents_by_type:
        z=0
        for h in model.agents_by_type[Human]:
            if not h.doll:
                z += h.tr_EI_coal+ h.o_EI_coal

        q=stat_annual_coal_production(model) #except dolls
        if q>0:
            return z/q
        else:
            return 0
    else:
        return 0


def stat_average_cost_wood(model):
    '''
    Average energy-invested on wood production per MJ, exept dolls
    '''
    if Human in model.agents_by_type:
        z=0
        for h in model.agents_by_type[Human]:
            if not h.doll:
                z += h.tr_EI_wood +h.o_EI_wood

        q=stat_annual_wood_production(model)  #except dolls
        if q>0:
            return z/q
        else:
            return 0
    else:
        return 0


def stat_average_mileage_coal(model):
    '''
    Average mileage of coal search, except dolls
    '''
    if Human in model.agents_by_type:
        z=0
        for h in model.agents_by_type[Human]:
            if not h.doll:
                z += h.mileage_coal

        q=stat_annual_coal_production(model)
        if q>0:
            return z/q
        else:
            return 0
    else:
        return 0


def stat_average_mileage_wood(model):
    '''
    Average mileage of wood search, except dolls
    '''
    if Human in model.agents_by_type:
        z=0
        for h in model.agents_by_type[Human]:
            if not h.doll:
                z += h.mileage_wood

        q=stat_annual_wood_production(model)
        if q>0:
            return z/q
        else:
            return 0
    else:
        return 0

def stat_coal_extraction_cost(model):
    '''
    return average coal extraction cost
    '''
    num=0
    if Field in model.agents_by_type:
        z=0        
        for f in model.agents_by_type[Field]:
            if f.type=='Mine':                
                z += f.extraction_cost
                num +=1

    if num>0:
        avr = z/num
    else:
        avr =0

    return avr 


#DEAL

def stat_coal_price(model):
    l= model.coal_deal
    if len(l)>0:
        sort_l = sorted(l, key=lambda x: x[1], reverse=True)
        return sort_l[0][1]
    else:
        return 0



def stat_wood_price(model):
    l=model.wood_deal
    if len(l)>0:
        sort_l = sorted(l, key=lambda x: x[1], reverse=True)
        return sort_l[0][1]
    else:
        return 0
