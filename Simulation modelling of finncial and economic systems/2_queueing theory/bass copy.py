"""
Python model 'bass.py'
Translated using PySD
"""

from pathlib import Path

from pysd.py_backend.statefuls import Integ
from pysd import Component

__pysd_version__ = "3.9.0"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 0,
    "final_time": lambda: 1000,
    "time_step": lambda: 0.01,
    "saveper": lambda: 10*time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="FINAL TIME", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    """
    The frequency with which output is stored.
    """
    return __data["time"].saveper()


@component.add(
    name="TIME STEP", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################

@component.add(
    name="total market",
    units="person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"customers": 1, "potential_customers": 1, "enemy_customers":1},
)
def total_market():
    return customers() + potential_customers() + enemy_customers()


@component.add(
    name="direct market",
    units="person/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"mark_eff": 1, "potential_customers":1},
)
def direct_market():
    return mark_eff() * potential_customers()


@component.add(
    name="fruitfulness",
    units="person/contact",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fruitfulness():
    return 0.015


@component.add(
    name="mark eff",
    units="person/contact",
    comp_type="Constant",
    comp_subtype="Normal",
)
def mark_eff():
    return 0.011


@component.add(
    name="sociability",
    units="contact/person/Month",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sociability():
    return 100


@component.add(
    name="p11",
    units="probability",
    comp_type="Constant",
    comp_subtype="Normal",
)
def p11():
    return 0.3


@component.add(
    name="p21",
    units="probability",
    comp_type="Constant",
    comp_subtype="Normal",
)
def p21():
    return 0.5


@component.add(
    name="p13",
    units="probability",
    comp_type="Constant",
    comp_subtype="Normal",
)
def p13():
    return 0.4


@component.add(
    name="p23",
    units="probability",
    comp_type="Constant",
    comp_subtype="Normal",
)
def p23():
    return 0.5


@component.add(
    name="Potential Customers",
    units="person",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_potential_customers": 1},
    other_deps={
        "_integ_potential_customers": {"initial": {}, "step": {"new_customers": 1,
                                                               "left_me":1,
                                                               "new_enemy_customers":1,
                                                               "left_enemy()":1}}
    },
)
def potential_customers():
    return _integ_potential_customers()

_integ_potential_customers = Integ(
    lambda: -new_customers() + left_me() - new_enemy_customers() + left_enemy(), lambda: 100000.0, "_integ_potential_customers"
) #left_enemy - те, кто ушли от конкурентов в рынок, new_enemy_customers - ушел от меня


@component.add(
    name="leave rate",
    units="",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"mark_eff": 1, "fruitfulness": 1},
)
def leave_rate():
    return mark_eff()*2/(mark_eff()*2+fruitfulness()*2)


@component.add(
    name="change rate",
    units="",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"mark_eff": 1, "fruitfulness": 1},
)
def change_rate():
    return fruitfulness()*2/(mark_eff()*2+fruitfulness()*2)

# tr1 b tr2 -шанс что клиент захочет уйти от мена change rate

@component.add(
    name="Customers",
    units="person",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_customers": 1},
    other_deps={"_integ_customers": {"initial": {}, "step": {"new_customers": 1,
                                                             "left_me": 1,
                                                             "change_leftme":1,
                                                             "change_tome": 1}}},
)
def customers():
    return _integ_customers()
#от чего зависит подумать #left_me - те кто покинул в рынок, change_leftme - те кто из моей компании ушел к конкурентам #change_tome - те, кто ушел от конкурентов ко мне

_integ_customers = Integ(lambda:
                         new_customers() - left_me() - change_to_enemy() + change_to_me(),
                         lambda: 0, "_integ_customers")


@component.add(
    name="Enemy customers",
    units="person",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_enemy_customers": 1},
    other_deps={"_integ_enemy_customers": {"initial": {}, "step": {"new_enemy_customers": 1,
                                                                   "left_enemy": 1,
                                                                   "change_left_enemy":1,
                                                                   "change_to_enemy": 1}}},
)
def enemy_customers():
    return _integ_enemy_customers()

_integ_enemy_customers = Integ(lambda:
                               new_enemy_customers() - left_enemy() - change_to_me() + change_to_enemy(),
                               lambda: 0, "_integ_enemy_customers")


@component.add(
    name="my share",
    units="",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"customers": 1, "total market": 1},
)
def my_share():
    return customers()/total_market()


@component.add(
    name="enemy share",
    units="",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"enemy_customers": 1, "total market": 1},
)
def comp_share():
    return enemy_customers()/total_market()


@component.add(
    name="new customers",
    units="person/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"word_of_mouth_demand": 1, "direct_market":1},
)
def new_customers():
    return word_of_mouth_demand() + direct_market()


@component.add(
    name="new enemy customers",
    units="person/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"word_of_enemy_mouth_demand": 1, "direct_market":1},
)
def new_enemy_customers():
    return word_of_enemy_mouth_demand() + direct_market()


@component.add(
    name="contacts with customers",
    units="contact/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"customers": 1, "sociability": 1},
)
def contacts_with_customers():
    return customers() * sociability()


@component.add(
    name="contacts with enemy customers",
    units="contact/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"enemy_customers": 1, "sociability": 1},
)
def contacts_with_enemy_customers():
    return enemy_customers() * sociability()


@component.add(
    name="contacts of noncustomers with customers",
    units="contact/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"contacts_with_customers": 1, "potential_customer_concentration": 1, "p11":1},
)
def contacts_of_noncustomers_with_customers():
    return contacts_with_customers() * potential_customer_concentration() * p11() #p11 - процент кастомеров которые довольны товарами в нашей фирме


@component.add(
    name="contacts of noncustomers with enemy customers",
    units="contact/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"contacts_with_enemy_customers": 1, "potential_customer_concentration": 1, "p11":1},
)
def contacts_of_noncustomers_with_enemy_customers():
    return contacts_with_enemy_customers() * potential_customer_concentration() * p21()


@component.add(
    name="potential customer concentration",
    units="dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"potential_customers": 1, "total_market": 1},
)
def potential_customer_concentration():
    return potential_customers() / total_market()


@component.add(
    name="word of mouth demand",
    units="person/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"contacts_of_noncustomers_with_customers": 1, "fruitfulness": 1},
)
def word_of_mouth_demand():
    return contacts_of_noncustomers_with_customers() * fruitfulness()


@component.add(
    name="word of enemy mouth demand",
    units="person/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"contacts_of_noncustomers_with_enemy_customers": 1, "fruitfulness": 1},
)
def word_of_enemy_mouth_demand():
    return contacts_of_noncustomers_with_enemy_customers() * fruitfulness()


@component.add(
    name="left me",
    units="person/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"customers": 1, "p13": 1, "leave_rate": 1},
)
def left_me():
    return customers()*p13()*leave_rate()


@component.add(
    name="left enemy",
    units="person/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"enemy_customers": 1, "p23": 1, "leave_rate": 1},
)
def left_enemy():
    return enemy_customers()*p23()*leave_rate()


@component.add(
    name="change to me",
    units="person/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"change_rate": 1,
                "leave_rate": 1,
                "fruitfulness": 1,
                "sociability": 1,
                "enemy_customers": 1,
                "customers": 1,
                "p11": 1,
                "p21": 1,
                "p13": 1,
                "total_market": 1},
)
def change_to_me():
    return change_rate() * fruitfulness() * sociability() * enemy_customers() * p21() * customers() * (
                1 - p11() - leave_rate() * p13()) \
           / total_market()


@component.add(
    name="change to enemy",
    units="person/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"change_rate":1,
                "leave_rate": 1,
                "fruitfulness": 1,
                "sociability": 1,
                "enemy_customers": 1,
                "customers": 1,
                "p11": 1,
                "p21": 1,
                "p23": 1,
                "total_market": 1},
)
def change_to_enemy():
    return change_rate()*fruitfulness()*sociability()*enemy_customers()*p11()*customers()*(1-p21()-leave_rate()*p23())\
           /total_market()


