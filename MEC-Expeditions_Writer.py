# This generates the code for expedition related files

# Python 3.6 or later
from pathlib import Path
import os
import sys
import codecs
import pprint
import re

expedition_duration = 262  # normal 262, change to 3 for testing

menu_event_number = 3  # Called from disasters/pulse_system If this number changes must also change there
expedition_arrival_start_number = 100
expedition_landing_start_number = 200
expedition_success_start_number = 300
expedition_total_failure_start_number = 400
expedition_map_failure_start_number = 500
expedition_trade_failure_start_number = 600
expedition_no_attack_failure_start_number = 700
expedition_decision_events_start_number = 800


class Expedition:
    def __init__(self, name, localized_name, ai_preference, target_type, associated_TN):
        self.name = name
        self.localized_name = localized_name
        self.ai_preference = ai_preference
        self.target_type = target_type
        self.associated_TN = associated_TN
        self.node_tech_reqs = []
        self.target_provinces = []

    def set_node_tech_reqs(self, node_tech_reqs):  # should be list of tuple pairs of node name and tech level
        assert len(self.node_tech_reqs) == 0, "Should only done once, setting to an empty list."
        self.node_tech_reqs = node_tech_reqs


# Balancing notes: 13 for your own area, 15 for directly next to, 16 for if have coast to go along, 17 if need north/south accuracy
expeditions_list = []  # Expeditions must have appropriately named province groups in in map/provincegroup.txt
# the British Isles
expeditions_list.append(Expedition('british_isles', 'the British Isles', 0, 'Jumping Node', [84]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 25), ('East Atlantis Node', 25), ('South Atlantis Node', 25), ('North Atlantis Node', 25), ('Iberia', 25), ('Strait of Gibraltar', 25), ('West Mediterranean', 25), ('France', 33), ('Channel', 33), ('North Sea', 33), ('Barbary Coast', 25), ('Tyrrenean Sea', 25), ('Rhineland', 33), ('Lower Nile', 25), ('Po Valley', 25), ('Adriatic Sea', 25), ('Levant', 25), ('Aegean Sea', 25),
     ('Danube', 25), ('Elbe', 33), ('Baltic Sea', 25), ('Vistula', 25), ('Crimea', 25), ('Western Siberia', 25), ('Dnieper', 25), ('Caspian Sea', 25), ('Zalesye', 25), ('Anatolia', 25), ('Sahara', 25), ('Senegambia', 27), ('Niger River', 27), ('Guinea Coast',
                        28), ('Lake Tchad', 28), ('Kongo', 28),
     ('South Africa', 30), ('Monomotapa', 30), ('Zanj', 30), ('Red Sea', 32), ('Upper Nile', 32), ('Arabia', 32), ('Iran', 32), ('Khorasan', 32), ('Mawarannahr', 32), ('Yettishar', 32),
     ('Punjab', 32), ('Gurjaratra', 32), ('Konkan', 32), ('Deccan Plateau', 32), ('Tamilakam', 32), ('Kalinga', 32), ('Delhi', 32), ('Bihar', 32), ('Bengal', 32), ('Himalayan Plateau', 32), ('Ayeyarwady', 32), ('Chao Phraya', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Moluccas', 33),
     ('Champa Sea', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangnan', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Eastern Siberia', 33), ('Nippon', 33),
     ('Far East', 33), ('Andes', 32), ('Southern Cone', 31), ('Guiana', 30), ('Amazonia', 32), ('Panama', 31), ('Caribbean', 30), ('Mexico', 31), ('Rio Grande', 31), ('Mississippi', 31), ('Plains', 31), ('Eastern Seaboard', 29), ('Canada', 29),
     ('American West Coast', 33), ('Pacific', 33)])
# Northern Europe
expeditions_list.append(Expedition('northern_europe', 'Northern Europe', 0, 'Jumping Node', [88]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 25), ('East Atlantis Node', 25), ('South Atlantis Node', 25), ('North Atlantis Node', 25), ('Iberia', 25), ('Strait of Gibraltar', 25), ('West Mediterranean', 25), ('France', 33), ('Channel', 33), ('North Sea', 33), ('Barbary Coast', 25), ('Tyrrenean Sea', 25), ('Rhineland', 33), ('Lower Nile', 25), ('Po Valley', 25), ('Adriatic Sea', 25), ('Levant', 25), ('Aegean Sea', 25),
     ('Danube', 25), ('Elbe', 33), ('Baltic Sea', 33), ('Vistula', 25), ('Crimea', 25), ('Western Siberia', 25), ('Dnieper', 25), ('Caspian Sea', 25), ('Zalesye', 25), ('Anatolia', 25), ('Sahara', 25), ('Senegambia', 27), ('Niger River', 27), ('Guinea Coast',
                                                                                                                                                                                                                                                    28), ('Lake Tchad', 28), ('Kongo', 28),
     ('South Africa', 30), ('Monomotapa', 30), ('Zanj', 30), ('Red Sea', 32), ('Upper Nile', 32), ('Arabia', 32), ('Iran', 32), ('Khorasan', 32), ('Mawarannahr', 32), ('Yettishar', 32),
     ('Punjab', 32), ('Gurjaratra', 32), ('Konkan', 32), ('Deccan Plateau', 32), ('Tamilakam', 32), ('Kalinga', 32), ('Delhi', 32), ('Bihar', 32), ('Bengal', 32), ('Himalayan Plateau', 32), ('Ayeyarwady', 32), ('Chao Phraya', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Moluccas', 33),
     ('Champa Sea', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangnan', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Eastern Siberia', 33), ('Nippon', 33),
     ('Far East', 33), ('Andes', 32), ('Southern Cone', 31), ('Guiana', 30), ('Amazonia', 32), ('Panama', 31), ('Caribbean', 30), ('Mexico', 31), ('Rio Grande', 31), ('Mississippi', 31), ('Plains', 31), ('Eastern Seaboard', 29), ('Canada', 29),
     ('American West Coast', 33), ('Pacific', 33)])
# France
expeditions_list.append(Expedition('france', 'France', 0, 'Jumping Node', [84]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 25), ('East Atlantis Node', 25), ('South Atlantis Node', 25), ('North Atlantis Node', 25), ('Iberia', 33), ('Strait of Gibraltar', 25), ('West Mediterranean', 25), ('France', 33), ('Channel', 33), ('North Sea', 33), ('Barbary Coast', 25), ('Tyrrenean Sea', 25), ('Rhineland', 33), ('Lower Nile', 25), ('Po Valley', 25), ('Adriatic Sea', 25), ('Levant', 25), ('Aegean Sea', 25),
     ('Danube', 25), ('Elbe', 33), ('Baltic Sea', 25), ('Vistula', 25), ('Crimea', 25), ('Western Siberia', 25), ('Dnieper', 25), ('Caspian Sea', 25), ('Zalesye', 25), ('Anatolia', 25), ('Sahara', 25), ('Senegambia', 27), ('Niger River', 27), ('Guinea Coast',
                                                                                                                                                                                                                                                    28), ('Lake Tchad', 28), ('Kongo', 28),
     ('South Africa', 30), ('Monomotapa', 30), ('Zanj', 30), ('Red Sea', 32), ('Upper Nile', 32), ('Arabia', 32), ('Iran', 32), ('Khorasan', 32), ('Mawarannahr', 32), ('Yettishar', 32),
     ('Punjab', 32), ('Gurjaratra', 32), ('Konkan', 32), ('Deccan Plateau', 32), ('Tamilakam', 32), ('Kalinga', 32), ('Delhi', 32), ('Bihar', 32), ('Bengal', 32), ('Himalayan Plateau', 32), ('Ayeyarwady', 32), ('Chao Phraya', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Moluccas', 33),
     ('Champa Sea', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangnan', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Eastern Siberia', 33), ('Nippon', 33),
     ('Far East', 33), ('Andes', 32), ('Southern Cone', 31), ('Guiana', 30), ('Amazonia', 32), ('Panama', 31), ('Caribbean', 30), ('Mexico', 31), ('Rio Grande', 31), ('Mississippi', 31), ('Plains', 31), ('Eastern Seaboard', 29), ('Canada', 29),
     ('American West Coast', 33), ('Pacific', 33)])
# Iberia
expeditions_list.append(Expedition('iberia', 'Iberia', 0, 'Jumping Node', [74, 78]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33),('West Atlantis Node', 25), ('East Atlantis Node', 25), ('South Atlantis Node', 25), ('North Atlantis Node', 25), ('Iberia', 33), ('Strait of Gibraltar', 33), ('West Mediterranean', 25), ('France', 25), ('Channel', 25), ('North Sea', 25), ('Barbary Coast', 25), ('Tyrrenean Sea', 25), ('Rhineland', 25), ('Lower Nile', 25), ('Po Valley', 25), ('Adriatic Sea', 25), ('Levant', 25), ('Aegean Sea', 25),
     ('Danube', 25), ('Elbe', 25), ('Baltic Sea', 25), ('Vistula', 25), ('Crimea', 25), ('Western Siberia', 25), ('Dnieper', 25), ('Caspian Sea', 25), ('Zalesye', 25), ('Anatolia', 25), ('Sahara', 25), ('Senegambia', 16), ('Niger River', 16),
     ('Guinea Coast', 27), ('Lake Tchad', 27), ('Kongo', 28), ('South Africa', 30), ('Monomotapa', 30), ('Zanj', 30), ('Red Sea', 32), ('Upper Nile', 32), ('Arabia', 32), ('Iran', 32), ('Khorasan', 32), ('Mawarannahr', 32), ('Yettishar', 32),
     ('Punjab', 32), ('Gurjaratra', 32), ('Konkan', 32), ('Deccan Plateau', 32), ('Tamilakam', 32), ('Kalinga', 32), ('Delhi', 32), ('Bihar', 32), ('Bengal', 32), ('Himalayan Plateau', 32), ('Ayeyarwady', 32), ('Chao Phraya', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Moluccas', 33),
     ('Champa Sea', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangnan', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Eastern Siberia', 33), ('Nippon', 33),
     ('Far East', 33), ('Andes', 32), ('Southern Cone', 31), ('Guiana', 30), ('Amazonia', 32), ('Panama', 31), ('Caribbean', 29), ('Mexico', 31), ('Rio Grande', 31), ('Mississippi', 31), ('Plains', 31), ('Eastern Seaboard', 29), ('Canada', 29),
     ('American West Coast', 33), ('Pacific', 33)])
# the Iberian Islands
expeditions_list.append(Expedition('iberian_islands', 'the Iberian Islands', 300, 'Jumping Node', [74, 78]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 25), ('East Atlantis Node', 25), ('South Atlantis Node', 25), ('North Atlantis Node', 25), ('Iberia', 33), ('Strait of Gibraltar', 33), ('West Mediterranean', 25), ('France', 25), ('Channel', 25), ('North Sea', 25), ('Barbary Coast', 25), ('Tyrrenean Sea', 25), ('Rhineland', 25), ('Lower Nile', 25), ('Po Valley', 25), ('Adriatic Sea', 25), ('Levant', 25), ('Aegean Sea', 25),
     ('Danube', 25), ('Elbe', 25), ('Baltic Sea', 25), ('Vistula', 25), ('Crimea', 25), ('Western Siberia', 25), ('Dnieper', 25), ('Caspian Sea', 25), ('Zalesye', 25), ('Anatolia', 25), ('Sahara', 25), ('Senegambia', 16), ('Niger River', 16),
     ('Guinea Coast', 27), ('Lake Tchad', 27), ('Kongo', 28), ('South Africa', 30), ('Monomotapa', 30), ('Zanj', 30), ('Red Sea', 32), ('Upper Nile', 32), ('Arabia', 32), ('Iran', 32), ('Khorasan', 32), ('Mawarannahr', 32), ('Yettishar', 32),
     ('Punjab', 32), ('Gurjaratra', 32), ('Konkan', 32), ('Deccan Plateau', 32), ('Tamilakam', 32), ('Kalinga', 32), ('Delhi', 32), ('Bihar', 32), ('Bengal', 32), ('Himalayan Plateau', 32), ('Ayeyarwady', 32), ('Chao Phraya', 32), ('Malacca Strait', 32), ('Mekong', 32), ('Moluccas', 32),
     ('Champa Sea', 32), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangnan', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Eastern Siberia', 33), ('Nippon', 33),
     ('Far East', 33), ('Andes', 32), ('Southern Cone', 31), ('Guiana', 30), ('Amazonia', 30), ('Panama', 31), ('Caribbean', 29), ('Mexico', 31), ('Rio Grande', 31), ('Mississippi', 31), ('Plains', 31), ('Eastern Seaboard', 29), ('Canada', 29),
     ('American West Coast', 33), ('Pacific', 33)])
# Northwest Africa
expeditions_list.append(Expedition('northwest_africa', 'Northwest Africa', 100, 'Jumping Node', [55]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 25), ('East Atlantis Node', 25), ('South Atlantis Node', 25), ('North Atlantis Node', 25), ('Iberia', 33), ('Strait of Gibraltar', 33), ('West Mediterranean', 25), ('France', 25), ('Channel', 25), ('North Sea', 25), ('Barbary Coast', 25), ('Tyrrenean Sea', 25), ('Rhineland', 25), ('Lower Nile', 25), ('Po Valley', 25), ('Adriatic Sea', 25), ('Levant', 25), ('Aegean Sea', 25),
     ('Danube', 25), ('Elbe', 25), ('Baltic Sea', 25), ('Vistula', 25), ('Crimea', 25), ('Western Siberia', 25), ('Dnieper', 25), ('Caspian Sea', 25), ('Zalesye', 25), ('Anatolia', 25), ('Sahara', 25), ('Senegambia', 16), ('Niger River', 16), ('Guinea Coast',
                                                                                                                                                                                                                                                    27), ('Lake Tchad', 27), ('Kongo', 28),
     ('South Africa', 30), ('Monomotapa', 30), ('Zanj', 30), ('Red Sea', 32), ('Upper Nile', 32), ('Arabia', 32), ('Iran', 32), ('Khorasan', 32), ('Mawarannahr', 32), ('Yettishar', 32),
     ('Punjab', 32), ('Gurjaratra', 32), ('Konkan', 32), ('Deccan Plateau', 32), ('Tamilakam', 32), ('Kalinga', 32), ('Delhi', 32), ('Bihar', 32), ('Bengal', 32), ('Himalayan Plateau', 32), ('Ayeyarwady', 32), ('Chao Phraya', 32), ('Malacca Strait', 32), ('Mekong', 32), ('Moluccas', 32),
     ('Champa Sea', 32), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangnan', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Eastern Siberia', 33), ('Nippon', 33),
     ('Far East', 33), ('Andes', 32), ('Southern Cone', 31), ('Guiana', 30), ('Amazonia', 32), ('Panama', 31), ('Caribbean', 29), ('Mexico', 31), ('Rio Grande', 31), ('Mississippi', 31), ('Plains', 31), ('Eastern Seaboard', 29), ('Canada', 29),
     ('American West Coast', 33), ('Pacific', 33)])
# West Africa
expeditions_list.append(Expedition('west_africa', 'West Africa', 800, 'Jumping Node', [51]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 16), ('East Atlantis Node', 16), ('South Atlantis Node', 16), ('North Atlantis Node', 16), ('Iberia', 16), ('Strait of Gibraltar', 16), ('Sahara', 16), ('West Mediterranean', 27), ('France', 27), ('Channel', 27), ('North Sea', 27), ('Barbary Coast', 27), ('Tyrrenean Sea', 27), ('Rhineland', 27), ('Lower Nile', 27), ('Po Valley', 27), ('Adriatic Sea', 27), ('Levant', 27),
     ('Aegean Sea', 27), ('Danube', 27), ('Elbe', 27), ('Baltic Sea', 27), ('Vistula', 27), ('Crimea', 27), ('Western Siberia', 27), ('Dnieper', 27), ('Caspian Sea', 27), ('Zalesye', 27), ('Anatolia', 27), ('Senegambia', 33), ('Niger River', 33), ('Guinea Coast',
                                                                                                                                                                                                                                                        33), ('Lake Tchad', 33), ('Kongo', 25),
     ('South Africa', 27), ('Monomotapa', 28), ('Zanj', 28), ('Red Sea', 30), ('Upper Nile', 30), ('Arabia', 30), ('Iran', 30), ('Khorasan', 30), ('Mawarannahr', 30), ('Yettishar', 30),
     ('Punjab', 30), ('Gurjaratra', 30), ('Konkan', 30), ('Deccan Plateau', 30), ('Tamilakam', 30), ('Kalinga', 30), ('Delhi', 30), ('Bihar', 32), ('Bengal', 30), ('Himalayan Plateau', 30), ('Ayeyarwady', 30), ('Chao Phraya', 31), ('Malacca Strait', 31), ('Mekong', 31), ('Moluccas', 31),
     ('Champa Sea', 31), ('Australia', 32), ('Liangguang', 32), ('Szechwan', 32), ('Huazhong', 32), ('Jiangnan', 32), ('Huabei', 32), ('Xibei', 32), ('Zhongyuan', 32), ('Eastern Siberia', 32), ('Nippon', 32),
     ('Far East', 32), ('Andes', 31), ('Southern Cone', 30), ('Guiana', 27), ('Amazonia', 31), ('Panama', 31), ('Caribbean', 29), ('Mexico', 31), ('Rio Grande', 31), ('Mississippi', 31), ('Plains', 31), ('Eastern Seaboard', 31), ('Canada', 31),
     ('American West Coast', 32), ('Pacific', 33)])
# the Gulf of Guinea
expeditions_list.append(Expedition('gulf_of_guinea', 'the Gulf of Guinea', 800, 'Jumping Node', [48]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 27), ('East Atlantis Node', 27), ('South Atlantis Node', 27), ('North Atlantis Node', 27), ('Iberia', 27), ('Strait of Gibraltar', 27), ('Sahara', 16), ('West Mediterranean', 28), ('France', 28), ('Channel', 28), ('North Sea', 28), ('Barbary Coast', 28), ('Tyrrenean Sea', 28), ('Rhineland', 28), ('Lower Nile', 28), ('Po Valley', 28), ('Adriatic Sea', 28), ('Levant', 28),
     ('Aegean Sea', 28), ('Danube', 28), ('Elbe', 28), ('Baltic Sea', 28), ('Vistula', 28), ('Crimea', 28), ('Western Siberia', 28), ('Dnieper', 28), ('Caspian Sea', 28), ('Zalesye', 28), ('Anatolia', 28), ('Senegambia', 33), ('Niger River', 33), ('Guinea Coast',
                                                                                                                                                                                                                                                        33), ('Lake Tchad', 33), ('Kongo', 33),
     ('South Africa', 27), ('Monomotapa', 27), ('Zanj', 27), ('Red Sea', 30), ('Upper Nile', 30), ('Arabia', 31), ('Iran', 31), ('Khorasan', 31), ('Mawarannahr', 31), ('Yettishar', 31),
     ('Punjab', 31), ('Gurjaratra', 31), ('Konkan', 31), ('Deccan Plateau', 31), ('Tamilakam', 31), ('Kalinga', 31), ('Delhi', 31), ('Bihar', 31), ('Bengal', 31), ('Himalayan Plateau', 31), ('Ayeyarwady', 31), ('Chao Phraya', 31), ('Malacca Strait', 31), ('Mekong', 31), ('Moluccas', 31),
     ('Champa Sea', 31), ('Australia', 32), ('Liangguang', 32), ('Szechwan', 32), ('Huazhong', 32), ('Jiangnan', 32), ('Huabei', 32), ('Xibei', 32), ('Zhongyuan', 32), ('Eastern Siberia', 32), ('Nippon', 32),
     ('Far East', 32), ('Andes', 31), ('Southern Cone', 30), ('Guiana', 27), ('Amazonia', 31), ('Panama', 31), ('Caribbean', 29), ('Mexico', 31), ('Rio Grande', 31), ('Mississippi', 31), ('Plains', 31), ('Eastern Seaboard', 31), ('Canada', 31),
     ('American West Coast', 32), ('Pacific', 33)])

# Central Africa
expeditions_list.append(Expedition('central_africa', 'Central Africa', 800, 'Jumping Node', [47]))
expeditions_list[-1].set_node_tech_reqs([('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 28), ('East Atlantis Node', 28), ('South Atlantis Node', 28), ('North Atlantis Node', 28), ('Iberia', 28), ('Strait of Gibraltar', 28), ('Sahara', 27), ('West Mediterranean', 29), ('France', 29),
                                         ('Channel', 29), ('North Sea', 29), ('Barbary Coast', 29), ('Tyrrenean Sea', 29), ('Rhineland', 29), ('Lower Nile', 29), ('Po Valley', 29), ('Adriatic Sea', 29), ('Levant', 29), ('Aegean Sea', 29), ('Danube', 29), ('Elbe', 29), ('Baltic Sea', 29),
                                         ('Vistula', 29), ('Crimea', 29), ('Western Siberia', 29), ('Dnieper', 29), ('Caspian Sea', 29), ('Zalesye', 29), ('Anatolia', 29), ('Senegambia', 25), ('Niger River', 33), ('Guinea Coast',
                                                                                                                                                                                                                      33), ('Lake Tchad', 33), ('Kongo', 33), ('South Africa', 25), ('Monomotapa', 27),
                                         ('Zanj', 27), ('Red Sea', 29), ('Upper Nile', 29), ('Arabia', 30), ('Iran', 30), ('Khorasan', 30), ('Mawarannahr', 30), ('Yettishar', 30),
                                         ('Punjab', 30), ('Gurjaratra', 30), ('Konkan', 30), ('Deccan Plateau', 30), ('Tamilakam', 30), ('Kalinga', 30), ('Delhi', 30), ('Bihar', 30), ('Bengal', 30), ('Himalayan Plateau', 30), ('Ayeyarwady', 30), ('Chao Phraya', 30), ('Malacca Strait', 30),
                                         ('Mekong', 30), ('Moluccas', 30),
                                         ('Champa Sea', 30), ('Australia', 31), ('Liangguang', 31), ('Szechwan', 31), ('Huazhong', 31), ('Jiangnan', 31), ('Huabei', 31), ('Xibei', 31), ('Zhongyuan', 31), ('Eastern Siberia', 31), ('Nippon', 31),
                                         ('Far East', 31), ('Andes', 31), ('Southern Cone', 30), ('Guiana', 28), ('Amazonia', 31), ('Panama', 31), ('Caribbean', 29), ('Mexico', 31), ('Rio Grande', 31), ('Mississippi', 31), ('Plains', 31), ('Eastern Seaboard', 31), ('Canada', 31),
                                         ('American West Coast', 32), ('Pacific', 33)])
# South Africa
expeditions_list.append(Expedition('south_africa', 'South Africa', 1300, 'Colonial Node', [44]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 30), ('East Atlantis Node', 30), ('South Atlantis Node', 30), ('North Atlantis Node', 30), ('Iberia', 30), ('Strait of Gibraltar', 30), ('Sahara', 28), ('West Mediterranean', 30), ('France', 30), ('Channel', 30), ('North Sea', 30), ('Barbary Coast', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Lower Nile', 30), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levant', 30),
     ('Aegean Sea', 30), ('Danube', 30), ('Elbe', 30), ('Baltic Sea', 30),
     ('Vistula', 30), ('Crimea', 30), ('Western Siberia', 30), ('Dnieper', 30), ('Caspian Sea', 30), ('Zalesye', 30), ('Anatolia', 30), ('Senegambia', 27), ('Niger River', 27), ('Guinea Coast',
                                                                                                                                                                                  27), ('Lake Tchad', 27), ('Kongo', 25), ('South Africa', 33), ('Monomotapa', 25), ('Zanj', 25), ('Red Sea', 16),
     ('Upper Nile', 16), ('Arabia', 27), ('Iran', 27), ('Khorasan', 27), ('Mawarannahr', 27), ('Yettishar', 27),
     ('Punjab', 27), ('Gurjaratra', 28), ('Konkan', 28), ('Deccan Plateau', 28), ('Tamilakam', 28), ('Kalinga', 28), ('Delhi', 28), ('Bihar', 28), ('Bengal', 28), ('Himalayan Plateau', 28), ('Ayeyarwady', 28), ('Chao Phraya', 30), ('Malacca Strait', 30), ('Mekong', 30), ('Moluccas', 30),
     ('Champa Sea', 30), ('Australia', 31), ('Liangguang', 30), ('Szechwan', 30), ('Huazhong', 30), ('Jiangnan', 30), ('Huabei', 30), ('Xibei', 30), ('Zhongyuan', 31), ('Eastern Siberia', 31), ('Nippon', 31),
     ('Far East', 31), ('Andes', 31), ('Southern Cone', 30), ('Guiana', 29), ('Amazonia', 31), ('Panama', 31), ('Caribbean', 30), ('Mexico', 31), ('Rio Grande', 31), ('Mississippi', 31), ('Plains', 31), ('Eastern Seaboard', 31), ('Canada', 31),
     ('American West Coast', 32), ('Pacific', 33)])
# East Africa
expeditions_list.append(Expedition('east_africa', 'East Africa', 800, 'Jumping Node', [43]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 30), ('East Atlantis Node', 30), ('South Atlantis Node', 30), ('North Atlantis Node', 30), ('Iberia', 30), ('Strait of Gibraltar', 30), ('Sahara', 30), ('West Mediterranean', 30), ('France', 30), ('Channel', 30), ('North Sea', 30), ('Barbary Coast', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Lower Nile', 28), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levant', 30),
     ('Aegean Sea', 30), ('Danube', 30), ('Elbe', 30), ('Baltic Sea', 30),
     ('Vistula', 30), ('Crimea', 30), ('Western Siberia', 30), ('Dnieper', 30), ('Caspian Sea', 30), ('Zalesye', 30), ('Anatolia', 30), ('Senegambia', 28), ('Niger River', 28), ('Guinea Coast',
                                                                                                                                                                                  27), ('Lake Tchad', 28), ('Kongo', 27), ('South Africa', 25), ('Monomotapa', 33), ('Zanj', 33), ('Red Sea', 33),
     ('Upper Nile', 33), ('Arabia', 25), ('Iran', 16), ('Khorasan', 16), ('Mawarannahr', 16), ('Yettishar', 16),
     ('Punjab', 16), ('Gurjaratra', 27), ('Konkan', 27), ('Deccan Plateau', 27), ('Tamilakam', 27), ('Kalinga', 27), ('Delhi', 27), ('Bihar', 27), ('Bengal', 27), ('Himalayan Plateau', 27), ('Ayeyarwady', 27), ('Chao Phraya', 29), ('Malacca Strait', 29), ('Mekong', 30), ('Moluccas', 30),
     ('Champa Sea', 30), ('Australia', 31), ('Liangguang', 30), ('Szechwan', 30), ('Huazhong', 30), ('Jiangnan', 30), ('Huabei', 30), ('Xibei', 30), ('Zhongyuan', 31), ('Eastern Siberia', 31), ('Nippon', 31),
     ('Far East', 31), ('Andes', 32), ('Southern Cone', 31), ('Guiana', 30), ('Amazonia', 32), ('Panama', 32), ('Caribbean', 31), ('Mexico', 32), ('Rio Grande', 32), ('Mississippi', 32), ('Plains', 32), ('Eastern Seaboard', 32), ('Canada', 32),
     ('American West Coast', 33), ('Pacific', 33)])
# the Indian Ocean
expeditions_list.append(Expedition('indian_ocean', 'the Indian Ocean', 800, 'Jumping Node', [43]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 30), ('East Atlantis Node', 30), ('South Atlantis Node', 30), ('North Atlantis Node', 30), ('Iberia', 30), ('Strait of Gibraltar', 30), ('Sahara', 30), ('West Mediterranean', 30), ('France', 30), ('Channel', 30), ('North Sea', 30), ('Barbary Coast', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Lower Nile', 28), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levant', 30),
     ('Aegean Sea', 30), ('Danube', 30), ('Elbe', 30), ('Baltic Sea', 30),
     ('Vistula', 30), ('Crimea', 30), ('Western Siberia', 30), ('Dnieper', 30), ('Caspian Sea', 30), ('Zalesye', 30), ('Anatolia', 30), ('Senegambia', 28), ('Niger River', 28), ('Guinea Coast',
                                                                                                                                                                                  27), ('Lake Tchad', 28), ('Kongo', 27), ('South Africa', 25), ('Monomotapa', 33), ('Zanj', 33), ('Red Sea', 25),
     ('Upper Nile', 25), ('Arabia', 27), ('Iran', 27), ('Khorasan', 27), ('Mawarannahr', 27), ('Yettishar', 27),
     ('Punjab', 27), ('Gurjaratra', 27), ('Konkan', 27), ('Deccan Plateau', 27), ('Tamilakam', 27), ('Kalinga', 27), ('Delhi', 27), ('Bihar', 27), ('Bengal', 27), ('Himalayan Plateau', 27), ('Ayeyarwady', 27), ('Chao Phraya', 29), ('Malacca Strait', 29), ('Mekong', 30), ('Moluccas', 30),
     ('Champa Sea', 30), ('Australia', 31), ('Liangguang', 30), ('Szechwan', 30), ('Huazhong', 30), ('Jiangnan', 30), ('Huabei', 30), ('Xibei', 30), ('Zhongyuan', 31), ('Eastern Siberia', 31), ('Nippon', 31),
     ('Far East', 31), ('Andes', 32), ('Southern Cone', 31), ('Guiana', 30), ('Amazonia', 32), ('Panama', 32), ('Caribbean', 31), ('Mexico', 32), ('Rio Grande', 32), ('Mississippi', 32), ('Plains', 32), ('Eastern Seaboard', 32), ('Canada', 32),
     ('American West Coast', 33), ('Pacific', 33)])
# Arabia
expeditions_list.append(Expedition('arabia', 'Arabia', 400, 'Jumping Node', [41, 54]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 30), ('East Atlantis Node', 30), ('South Atlantis Node', 30), ('North Atlantis Node', 30), ('Iberia', 30), ('Strait of Gibraltar', 30), ('Sahara', 30), ('West Mediterranean', 30), ('France', 30), ('Channel', 30), ('North Sea', 30), ('Barbary Coast', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Lower Nile', 16), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levant', 30),
     ('Aegean Sea', 30), ('Danube', 30), ('Elbe', 30), ('Baltic Sea', 30),
     ('Vistula', 30), ('Crimea', 30), ('Western Siberia', 30), ('Dnieper', 30), ('Caspian Sea', 30), ('Zalesye', 30), ('Anatolia', 30), ('Senegambia', 30), ('Niger River', 30), ('Guinea Coast',
                                                                                                                                                                                  30), ('Lake Tchad', 30), ('Kongo', 30), ('South Africa', 27), ('Monomotapa', 16), ('Zanj', 25), ('Red Sea', 33),
     ('Upper Nile', 33), ('Arabia', 33), ('Iran', 33), ('Khorasan', 33), ('Mawarannahr', 33), ('Yettishar', 33),
     ('Punjab', 33), ('Gurjaratra', 25), ('Konkan', 25), ('Deccan Plateau', 25), ('Tamilakam', 25), ('Kalinga', 25), ('Delhi', 25), ('Bihar', 25), ('Bengal', 25), ('Himalayan Plateau', 25), ('Ayeyarwady', 25), ('Chao Phraya', 27), ('Malacca Strait', 27), ('Mekong', 27), ('Moluccas', 27),
     ('Champa Sea', 27), ('Australia', 29), ('Liangguang', 29), ('Szechwan', 29), ('Huazhong', 29), ('Jiangnan', 29), ('Huabei', 29), ('Xibei', 29), ('Zhongyuan', 30), ('Eastern Siberia', 30), ('Nippon', 30),
     ('Far East', 30), ('Andes', 32), ('Southern Cone', 31), ('Guiana', 30), ('Amazonia', 32), ('Panama', 32), ('Caribbean', 31), ('Mexico', 32), ('Rio Grande', 32), ('Mississippi', 32), ('Plains', 32), ('Eastern Seaboard', 32), ('Canada', 32),
     ('American West Coast', 33), ('Pacific', 33)])
# Western India
expeditions_list.append(Expedition('western_india', 'Western India', 1300, 'Jumping Node', [38, 39]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 30), ('East Atlantis Node', 30), ('South Atlantis Node', 30), ('North Atlantis Node', 30), ('Iberia', 30), ('Strait of Gibraltar', 30), ('Sahara', 30), ('West Mediterranean', 30), ('France', 30), ('Channel', 30), ('North Sea', 30), ('Barbary Coast', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Lower Nile', 28), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levant', 30),
     ('Aegean Sea', 30), ('Danube', 30), ('Elbe', 30), ('Baltic Sea', 30),
     ('Vistula', 30), ('Crimea', 30), ('Western Siberia', 30), ('Dnieper', 30), ('Caspian Sea', 30), ('Zalesye', 30), ('Anatolia', 30), ('Senegambia', 30), ('Niger River', 30), ('Guinea Coast',
                                                                                                                                                                                  30), ('Lake Tchad', 30), ('Kongo', 30), ('South Africa', 28), ('Monomotapa', 27), ('Zanj', 27), ('Red Sea', 25),
     ('Upper Nile', 25), ('Arabia', 33), ('Iran', 25), ('Khorasan', 25), ('Mawarannahr', 33), ('Yettishar', 33),
     ('Punjab', 33), ('Gurjaratra', 33), ('Konkan', 33), ('Deccan Plateau', 33), ('Tamilakam', 33), ('Kalinga', 25), ('Delhi', 33), ('Bihar', 33), ('Bengal', 25), ('Himalayan Plateau', 25), ('Ayeyarwady', 25), ('Chao Phraya', 27), ('Malacca Strait', 27), ('Mekong', 27), ('Moluccas', 27),
     ('Champa Sea', 27), ('Australia', 28), ('Liangguang', 28), ('Szechwan', 28), ('Huazhong', 28), ('Jiangnan', 28), ('Huabei', 28), ('Xibei', 28), ('Zhongyuan', 29), ('Eastern Siberia', 29), ('Nippon', 29),
     ('Far East', 29), ('Andes', 33), ('Southern Cone', 32), ('Guiana', 31), ('Amazonia', 33), ('Panama', 33), ('Caribbean', 32), ('Mexico', 33), ('Rio Grande', 33), ('Mississippi', 33), ('Plains', 33), ('Eastern Seaboard', 33), ('Canada', 33),
     ('American West Coast', 33), ('Pacific', 33)])
# Southern India
expeditions_list.append(Expedition('southern_india', 'Southern India', 1300, 'Jumping Node', [37, 38]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 30), ('East Atlantis Node', 30), ('South Atlantis Node', 30), ('North Atlantis Node', 30), ('Iberia', 30), ('Strait of Gibraltar', 30), ('Sahara', 30), ('West Mediterranean', 30), ('France', 30), ('Channel', 30), ('North Sea', 30), ('Barbary Coast', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Lower Nile', 28), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levant', 30),
     ('Aegean Sea', 30), ('Danube', 30), ('Elbe', 30), ('Baltic Sea', 30),
     ('Vistula', 30), ('Crimea', 30), ('Western Siberia', 30), ('Dnieper', 30), ('Caspian Sea', 30), ('Zalesye', 30), ('Anatolia', 30), ('Senegambia', 30), ('Niger River', 30), ('Guinea Coast',
                                                                                                                                                                                  30), ('Lake Tchad', 30), ('Kongo', 30), ('South Africa', 28), ('Monomotapa', 27), ('Zanj', 27), ('Red Sea', 25),
     ('Upper Nile', 25), ('Arabia', 25), ('Iran', 25), ('Khorasan', 25), ('Mawarannahr', 25), ('Yettishar', 25),
     ('Punjab', 25), ('Gurjaratra', 33), ('Konkan', 33), ('Deccan Plateau', 33), ('Tamilakam', 33), ('Kalinga', 33), ('Delhi', 33), ('Bihar', 33), ('Bengal', 25), ('Himalayan Plateau', 25), ('Ayeyarwady', 25), ('Chao Phraya', 25), ('Malacca Strait', 16), ('Mekong', 16), ('Moluccas', 16),
     ('Champa Sea', 16), ('Australia', 28), ('Liangguang', 28), ('Szechwan', 28), ('Huazhong', 28), ('Jiangnan', 28), ('Huabei', 28), ('Xibei', 28), ('Zhongyuan', 29), ('Eastern Siberia', 29), ('Nippon', 29),
     ('Far East', 29), ('Andes', 33), ('Southern Cone', 32), ('Guiana', 31), ('Amazonia', 33), ('Panama', 33), ('Caribbean', 32), ('Mexico', 33), ('Rio Grande', 33), ('Mississippi', 33), ('Plains', 33), ('Eastern Seaboard', 33), ('Canada', 33),
     ('American West Coast', 33), ('Pacific', 33)])
# Eastern India
expeditions_list.append(Expedition('eastern_india', 'Eastern India', 1300, 'Jumping Node', [36, 37]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 30), ('East Atlantis Node', 30), ('South Atlantis Node', 30), ('North Atlantis Node', 30), ('Iberia', 30), ('Strait of Gibraltar', 30), ('Sahara', 30), ('West Mediterranean', 30), ('France', 30), ('Channel', 30), ('North Sea', 30), ('Barbary Coast', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Lower Nile', 28), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levant', 30),
     ('Aegean Sea', 30), ('Danube', 30), ('Elbe', 30), ('Baltic Sea', 30),
     ('Vistula', 30), ('Crimea', 30), ('Western Siberia', 30), ('Dnieper', 30), ('Caspian Sea', 30), ('Zalesye', 30), ('Anatolia', 30), ('Senegambia', 30), ('Niger River', 30), ('Guinea Coast',
                                                                                                                                                                                  30), ('Lake Tchad', 30), ('Kongo', 30), ('South Africa', 28), ('Monomotapa', 27), ('Zanj', 27), ('Red Sea', 16),
     ('Upper Nile', 16), ('Arabia', 25), ('Iran', 25), ('Khorasan', 25), ('Mawarannahr', 25), ('Yettishar', 25),
     ('Punjab', 25), ('Gurjaratra', 25), ('Konkan', 25), ('Deccan Plateau', 25), ('Tamilakam', 33), ('Kalinga', 33), ('Delhi', 33), ('Bihar', 33), ('Bengal', 33), ('Himalayan Plateau', 33), ('Ayeyarwady', 33), ('Chao Phraya', 25), ('Malacca Strait', 16), ('Mekong', 16), ('Moluccas', 16),
     ('Champa Sea', 16), ('Australia', 27), ('Liangguang', 16), ('Szechwan', 16), ('Huazhong', 27), ('Jiangnan', 27), ('Huabei', 27), ('Xibei', 27), ('Zhongyuan', 27), ('Eastern Siberia', 28), ('Nippon', 28),
     ('Far East', 28), ('Andes', 33), ('Southern Cone', 32), ('Guiana', 31), ('Amazonia', 33), ('Panama', 33), ('Caribbean', 32), ('Mexico', 33), ('Rio Grande', 33), ('Mississippi', 33), ('Plains', 33), ('Eastern Seaboard', 33), ('Canada', 33),
     ('American West Coast', 33), ('Pacific', 33)])
# Malacca
expeditions_list.append(Expedition('malacca', 'Malacca', 800, 'Regular', [36]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 31), ('East Atlantis Node', 31), ('South Atlantis Node', 31), ('North Atlantis Node', 31), ('Iberia', 31), ('Strait of Gibraltar', 31), ('Sahara', 31), ('West Mediterranean', 31), ('France', 31), ('Channel', 31), ('North Sea', 31), ('Barbary Coast', 31), ('Tyrrenean Sea', 31), ('Rhineland', 31), ('Lower Nile', 29), ('Po Valley', 31), ('Adriatic Sea', 31), ('Levant', 31),
     ('Aegean Sea', 31), ('Danube', 31), ('Elbe', 31), ('Baltic Sea', 31),
     ('Vistula', 31), ('Crimea', 31), ('Western Siberia', 31), ('Dnieper', 31), ('Caspian Sea', 31), ('Zalesye', 31), ('Anatolia', 31), ('Senegambia', 31), ('Niger River', 31), ('Guinea Coast',
                                                                                                                                                                                  31), ('Lake Tchad', 31), ('Kongo', 31), ('South Africa', 30), ('Monomotapa', 30), ('Zanj', 30), ('Red Sea', 27),
     ('Upper Nile', 27), ('Arabia', 27), ('Iran', 27), ('Khorasan', 27), ('Mawarannahr', 27), ('Yettishar', 27),
     ('Punjab', 27), ('Gurjaratra', 27), ('Konkan', 27), ('Deccan Plateau', 27), ('Tamilakam', 16), ('Kalinga', 25), ('Delhi', 25), ('Bihar', 25), ('Bengal', 25), ('Himalayan Plateau', 25), ('Ayeyarwady', 25), ('Chao Phraya', 33), ('Malacca Strait', 33), ('Mekong', 25), ('Moluccas', 33),
     ('Champa Sea', 25), ('Australia', 27), ('Liangguang', 25), ('Szechwan', 25), ('Huazhong', 25), ('Jiangnan', 16), ('Huabei', 16), ('Xibei', 16), ('Eastern Siberia', 27), ('Zhongyuan', 16), ('Nippon', 27),
     ('Far East', 27), ('Andes', 33), ('Southern Cone', 32), ('Guiana', 31), ('Amazonia', 33), ('Panama', 33), ('Caribbean', 32), ('Mexico', 33), ('Rio Grande', 33), ('Mississippi', 33), ('Plains', 33), ('Eastern Seaboard', 33), ('Canada', 33),
     ('American West Coast', 33), ('Pacific', 33)])
# Southeast Asia
expeditions_list.append(Expedition('southeast_asia', 'Southeast Asia', 600, 'Regular', [27, 32, 31]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 31), ('East Atlantis Node', 31), ('South Atlantis Node', 31), ('North Atlantis Node', 31), ('Iberia', 31), ('Strait of Gibraltar', 31), ('Sahara', 31), ('West Mediterranean', 31), ('France', 31), ('Channel', 31), ('North Sea', 31), ('Barbary Coast', 31), ('Tyrrenean Sea', 31), ('Rhineland', 31), ('Lower Nile', 29), ('Po Valley', 31), ('Adriatic Sea', 31), ('Levant', 31),
     ('Aegean Sea', 31), ('Danube', 31), ('Elbe', 31), ('Baltic Sea', 31),
     ('Vistula', 31), ('Crimea', 31), ('Western Siberia', 31), ('Dnieper', 31), ('Caspian Sea', 31), ('Zalesye', 31), ('Anatolia', 31), ('Senegambia', 31), ('Niger River', 31), ('Guinea Coast',
                                                                                                                                                                                  31), ('Lake Tchad', 31), ('Kongo', 31), ('South Africa', 30), ('Monomotapa', 30), ('Zanj', 30), ('Red Sea', 27),
     ('Upper Nile', 27), ('Arabia', 27), ('Iran', 27), ('Khorasan', 27), ('Mawarannahr', 27), ('Yettishar', 27),
     ('Punjab', 27), ('Gurjaratra', 27), ('Konkan', 27), ('Deccan Plateau', 27), ('Tamilakam', 16), ('Kalinga', 25), ('Delhi', 25), ('Bihar', 25), ('Bengal', 25), ('Himalayan Plateau', 25), ('Ayeyarwady', 25), ('Chao Phraya', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Moluccas', 25),
     ('Champa Sea', 25), ('Australia', 27), ('Liangguang', 25), ('Szechwan', 25), ('Huazhong', 25), ('Jiangnan', 16), ('Huabei', 16), ('Xibei', 16), ('Eastern Siberia', 27), ('Zhongyuan', 16), ('Nippon', 27),
     ('Far East', 27), ('Andes', 33), ('Southern Cone', 32), ('Guiana', 31), ('Amazonia', 33), ('Panama', 33), ('Caribbean', 32), ('Mexico', 33), ('Rio Grande', 33), ('Mississippi', 33), ('Plains', 33), ('Eastern Seaboard', 33), ('Canada', 33),
     ('American West Coast', 33), ('Pacific', 33)])
# Indonesia
expeditions_list.append(Expedition('indonesia', 'Indonesia', 1300, 'Regular', [35]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 31), ('East Atlantis Node', 31), ('South Atlantis Node', 31), ('North Atlantis Node', 31), ('Iberia', 31), ('Strait of Gibraltar', 31), ('Sahara', 31), ('West Mediterranean', 31), ('France', 31), ('Channel', 31), ('North Sea', 31), ('Barbary Coast', 31), ('Tyrrenean Sea', 31), ('Rhineland', 31), ('Lower Nile', 29), ('Po Valley', 31), ('Adriatic Sea', 31), ('Levant', 31),
     ('Aegean Sea', 31), ('Danube', 31), ('Elbe', 31), ('Baltic Sea', 31),
     ('Vistula', 31), ('Crimea', 31), ('Western Siberia', 31), ('Dnieper', 31), ('Caspian Sea', 31), ('Zalesye', 31), ('Anatolia', 31), ('Senegambia', 31), ('Niger River', 31), ('Guinea Coast',
                                                                                                                                                                                  31), ('Lake Tchad', 31), ('Kongo', 31), ('South Africa', 30), ('Monomotapa', 30), ('Zanj', 30), ('Red Sea', 27),
     ('Upper Nile', 27), ('Arabia', 27), ('Iran', 27), ('Khorasan', 27), ('Mawarannahr', 27), ('Yettishar', 27),
     ('Punjab', 27), ('Gurjaratra', 27), ('Konkan', 27), ('Deccan Plateau', 27), ('Tamilakam', 16), ('Kalinga', 16), ('Delhi', 16), ('Bihar', 16), ('Bengal', 16), ('Himalayan Plateau', 16), ('Ayeyarwady', 16), ('Chao Phraya', 25), ('Malacca Strait', 33), ('Mekong', 25), ('Moluccas', 33),
     ('Champa Sea', 25), ('Australia', 27), ('Liangguang', 25), ('Szechwan', 25), ('Huazhong', 25), ('Jiangnan', 16), ('Huabei', 16), ('Xibei', 16), ('Eastern Siberia', 27), ('Zhongyuan', 16), ('Nippon', 27),
     ('Far East', 27), ('Andes', 33), ('Southern Cone', 32), ('Guiana', 31), ('Amazonia', 33), ('Panama', 33), ('Caribbean', 32), ('Mexico', 33), ('Rio Grande', 33), ('Mississippi', 33), ('Plains', 33), ('Eastern Seaboard', 33), ('Canada', 33),
     ('American West Coast', 33), ('Pacific', 33)])
# the Philippines
expeditions_list.append(Expedition('philippines', 'the Philippines', 800, 'Regular', [32]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 31), ('East Atlantis Node', 31), ('South Atlantis Node', 31), ('North Atlantis Node', 31), ('Iberia', 31), ('Strait of Gibraltar', 31), ('Sahara', 31), ('West Mediterranean', 31), ('France', 31), ('Channel', 31), ('North Sea', 31), ('Barbary Coast', 31), ('Tyrrenean Sea', 31), ('Rhineland', 31), ('Lower Nile', 29), ('Po Valley', 31), ('Adriatic Sea', 31), ('Levant', 31),
     ('Aegean Sea', 31), ('Danube', 31), ('Elbe', 31), ('Baltic Sea', 31),
     ('Vistula', 31), ('Crimea', 31), ('Western Siberia', 31), ('Dnieper', 31), ('Caspian Sea', 31), ('Zalesye', 31), ('Anatolia', 31), ('Senegambia', 31), ('Niger River', 31), ('Guinea Coast',
                                                                                                                                                                                  31), ('Lake Tchad', 31), ('Kongo', 31), ('South Africa', 30), ('Monomotapa', 30), ('Zanj', 30), ('Red Sea', 27),
     ('Upper Nile', 27), ('Arabia', 27), ('Iran', 27), ('Khorasan', 27), ('Mawarannahr', 27), ('Yettishar', 27),
     ('Punjab', 27), ('Gurjaratra', 27), ('Konkan', 27), ('Deccan Plateau', 27), ('Tamilakam', 16), ('Kalinga', 16), ('Delhi', 16), ('Bihar', 16), ('Bengal', 16), ('Himalayan Plateau', 16), ('Ayeyarwady', 16), ('Chao Phraya', 25), ('Malacca Strait', 25), ('Mekong', 25), ('Moluccas', 25),
     ('Champa Sea', 33), ('Australia', 27), ('Liangguang', 25), ('Szechwan', 25), ('Huazhong', 25), ('Jiangnan', 16), ('Huabei', 16), ('Xibei', 16), ('Eastern Siberia', 27), ('Zhongyuan', 16), ('Nippon', 27),
     ('Far East', 27), ('Andes', 33), ('Southern Cone', 32), ('Guiana', 31), ('Amazonia', 33), ('Panama', 33), ('Caribbean', 32), ('Mexico', 33), ('Rio Grande', 33), ('Mississippi', 33), ('Plains', 33), ('Eastern Seaboard', 33), ('Canada', 33),
     ('American West Coast', 33), ('Pacific', 33)])
# Papua New Guinea
expeditions_list.append(Expedition('papua', 'Papua New Guinea', 100, 'Regular', [5]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 49), ('East Atlantis Node', 49), ('South Atlantis Node', 49), ('North Atlantis Node', 49), ('Iberia', 49), ('Strait of Gibraltar', 49), ('Sahara', 49), ('West Mediterranean', 49), ('France', 49), ('Channel', 49), ('North Sea', 49), ('Barbary Coast', 49), ('Tyrrenean Sea', 49), ('Rhineland', 49), ('Lower Nile', 49), ('Po Valley', 49), ('Adriatic Sea', 49), ('Levant', 49),
     ('Aegean Sea', 49), ('Danube', 49), ('Elbe', 49), ('Baltic Sea', 49),
     ('Vistula', 49), ('Crimea', 49), ('Western Siberia', 49), ('Dnieper', 49), ('Caspian Sea', 49), ('Zalesye', 49), ('Anatolia', 49), ('Senegambia', 49), ('Niger River', 49), ('Guinea Coast',
                                                                                                                                                                                  49), ('Lake Tchad', 49), ('Kongo', 49), ('South Africa', 49), ('Monomotapa', 49), ('Zanj', 49), ('Red Sea', 49),
     ('Upper Nile', 49), ('Arabia', 49), ('Iran', 49), ('Khorasan', 49), ('Mawarannahr', 49), ('Yettishar', 49),
     ('Punjab', 49), ('Gurjaratra', 49), ('Konkan', 49), ('Deccan Plateau', 49), ('Tamilakam', 49), ('Kalinga', 49), ('Delhi', 49), ('Bihar', 49), ('Bengal', 49), ('Himalayan Plateau', 49), ('Ayeyarwady', 49), ('Chao Phraya', 49), ('Malacca Strait', 49), ('Mekong', 49), ('Moluccas', 49),
     ('Champa Sea', 49), ('Australia', 49), ('Liangguang', 49), ('Szechwan', 49), ('Huazhong', 49), ('Jiangnan', 49), ('Huabei', 49), ('Xibei', 49), ('Eastern Siberia', 49), ('Zhongyuan', 49), ('Nippon', 49),
     ('Far East', 49), ('Andes', 49), ('Southern Cone', 49), ('Guiana', 49), ('Amazonia', 49), ('Panama', 49), ('Caribbean', 49), ('Mexico', 49), ('Rio Grande', 49), ('Mississippi', 49), ('Plains', 49), ('Eastern Seaboard', 49), ('Canada', 49),
     ('American West Coast', 49), ('Pacific', 49)])
# Australia
expeditions_list.append(Expedition('australia', 'Australia', 100, 'Colonial Node', [5]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 48), ('East Atlantis Node', 48), ('South Atlantis Node', 48), ('North Atlantis Node', 48), ('Iberia', 48), ('Strait of Gibraltar', 48), ('Sahara', 48), ('West Mediterranean', 48), ('France', 48), ('Channel', 48), ('North Sea', 48), ('Barbary Coast', 48), ('Tyrrenean Sea', 48), ('Rhineland', 48), ('Lower Nile', 48), ('Po Valley', 48), ('Adriatic Sea', 48), ('Levant', 48),
     ('Aegean Sea', 48), ('Danube', 48), ('Elbe', 48), ('Baltic Sea', 48),
     ('Vistula', 48), ('Crimea', 48), ('Western Siberia', 48), ('Dnieper', 48), ('Caspian Sea', 48), ('Zalesye', 48), ('Anatolia', 48), ('Senegambia', 48), ('Niger River', 48), ('Guinea Coast',
                                                                                                                                                                                  48), ('Lake Tchad', 48), ('Kongo', 48), ('South Africa', 48), ('Monomotapa', 48), ('Zanj', 48), ('Red Sea', 48),
     ('Upper Nile', 48), ('Arabia', 48), ('Iran', 48), ('Khorasan', 48), ('Mawarannahr', 48), ('Yettishar', 48),
     ('Punjab', 48), ('Gurjaratra', 48), ('Konkan', 48), ('Deccan Plateau', 48), ('Tamilakam', 48), ('Kalinga', 48), ('Delhi', 48), ('Bihar', 48), ('Bengal', 48), ('Himalayan Plateau', 48), ('Ayeyarwady', 48), ('Chao Phraya', 48), ('Malacca Strait', 48), ('Mekong', 48), ('Moluccas', 48),
     ('Champa Sea', 48), ('Australia', 25), ('Liangguang', 48), ('Szechwan', 48), ('Huazhong', 48), ('Jiangnan', 48), ('Huabei', 48), ('Xibei', 48), ('Eastern Siberia', 48), ('Zhongyuan', 48), ('Nippon', 48),
     ('Far East', 48), ('Andes', 48), ('Southern Cone', 48), ('Guiana', 48), ('Amazonia', 48), ('Panama', 48), ('Caribbean', 48), ('Mexico', 48), ('Rio Grande', 48), ('Mississippi', 48), ('Plains', 48), ('Eastern Seaboard', 48), ('Canada', 48),
     ('American West Coast', 48), ('Pacific', 33)])
# the Pacific Islands
expeditions_list.append(Expedition('pacific_islands', 'the Pacific Islands', 400, 'Jumping Node', [1]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 33), ('East Atlantis Node', 33), ('South Atlantis Node', 33), ('North Atlantis Node', 33), ('Iberia', 33), ('Strait of Gibraltar', 33), ('Sahara', 33), ('West Mediterranean', 33), ('France', 33), ('Channel', 33), ('North Sea', 33), ('Barbary Coast', 33), ('Tyrrenean Sea', 33), ('Rhineland', 33), ('Lower Nile', 33), ('Po Valley', 33), ('Adriatic Sea', 33), ('Levant', 33),
     ('Aegean Sea', 33), ('Danube', 33), ('Elbe', 33), ('Baltic Sea', 33),
     ('Vistula', 33), ('Crimea', 33), ('Western Siberia', 33), ('Dnieper', 33), ('Caspian Sea', 33), ('Zalesye', 33), ('Anatolia', 33), ('Senegambia', 33), ('Niger River', 33), ('Guinea Coast',
                                                                                                                                                                                  33), ('Lake Tchad', 33), ('Kongo', 33), ('South Africa', 33), ('Monomotapa', 33), ('Zanj', 33), ('Red Sea', 33),
     ('Upper Nile', 33), ('Arabia', 33), ('Iran', 33), ('Khorasan', 33), ('Mawarannahr', 33), ('Yettishar', 33),
     ('Punjab', 33), ('Gurjaratra', 33), ('Konkan', 33), ('Deccan Plateau', 33), ('Tamilakam', 33), ('Kalinga', 33), ('Delhi', 33), ('Bihar', 33), ('Bengal', 33), ('Himalayan Plateau', 33), ('Ayeyarwady', 33), ('Chao Phraya', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Moluccas', 33),
     ('Champa Sea', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangnan', 33), ('Huabei', 33), ('Xibei', 33), ('Eastern Siberia', 33), ('Zhongyuan', 33), ('Nippon', 33),
     ('Far East', 33), ('Andes', 33), ('Southern Cone', 33), ('Guiana', 33), ('Amazonia', 33), ('Panama', 33), ('Caribbean', 33), ('Mexico', 33), ('Rio Grande', 33), ('Mississippi', 33), ('Plains', 33), ('Eastern Seaboard', 33), ('Canada', 33),
     ('American West Coast', 33), ('Pacific', 33)])
# Southern China
expeditions_list.append(Expedition('southern_china', 'Southern China', 800, 'Chinese Mainland', [6, 30]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 32), ('East Atlantis Node', 32), ('South Atlantis Node', 32), ('North Atlantis Node', 32), ('Iberia', 32), ('Strait of Gibraltar', 32), ('Sahara', 32), ('West Mediterranean', 32), ('France', 32), ('Channel', 32), ('North Sea', 32), ('Barbary Coast', 32), ('Tyrrenean Sea', 32), ('Rhineland', 32), ('Lower Nile', 30), ('Po Valley', 32), ('Adriatic Sea', 32), ('Levant', 32),
     ('Aegean Sea', 32), ('Danube', 32), ('Elbe', 32), ('Baltic Sea', 32),
     ('Vistula', 32), ('Crimea', 32), ('Western Siberia', 32), ('Dnieper', 32), ('Caspian Sea', 32), ('Zalesye', 32), ('Anatolia', 32), ('Senegambia', 32), ('Niger River', 32), ('Guinea Coast',
                                                                                                                                                                                  32), ('Lake Tchad', 32), ('Kongo', 32), ('South Africa', 31), ('Monomotapa', 31), ('Zanj', 31), ('Red Sea', 29),
     ('Upper Nile', 29), ('Arabia', 29), ('Iran', 29), ('Khorasan', 29), ('Mawarannahr', 29), ('Yettishar', 29),
     ('Punjab', 28), ('Gurjaratra', 28), ('Konkan', 28), ('Deccan Plateau', 28), ('Tamilakam', 28), ('Kalinga', 28), ('Delhi', 28), ('Bihar', 28), ('Bengal', 28), ('Himalayan Plateau', 28), ('Ayeyarwady', 28), ('Chao Phraya', 16), ('Malacca Strait', 16), ('Mekong', 16), ('Moluccas', 16),
     ('Champa Sea', 25), ('Australia', 27), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangnan', 33), ('Huabei', 33), ('Xibei', 25), ('Zhongyuan', 25), ('Eastern Siberia', 25), ('Nippon', 25),
     ('Far East', 16), ('Andes', 33), ('Southern Cone', 33), ('Guiana', 32), ('Amazonia', 33), ('Panama', 33), ('Caribbean', 33), ('Mexico', 33), ('Rio Grande', 33), ('Mississippi', 33), ('Plains', 33), ('Eastern Seaboard', 33), ('Canada', 33),
     ('American West Coast', 33), ('Pacific', 33)])
# Northern China
expeditions_list.append(Expedition('northern_china', 'Northern China', 800, 'Chinese Mainland', [6, 9, 7, 14]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 32), ('East Atlantis Node', 32), ('South Atlantis Node', 32), ('North Atlantis Node', 32), ('Iberia', 32), ('Strait of Gibraltar', 32), ('Sahara', 32), ('West Mediterranean', 32), ('France', 32), ('Channel', 32), ('North Sea', 32), ('Barbary Coast', 32), ('Tyrrenean Sea', 32), ('Rhineland', 32), ('Lower Nile', 30), ('Po Valley', 32), ('Adriatic Sea', 32), ('Levant', 32),
     ('Aegean Sea', 32), ('Danube', 32), ('Elbe', 32), ('Baltic Sea', 32),
     ('Vistula', 32), ('Crimea', 32), ('Western Siberia', 32), ('Dnieper', 32), ('Caspian Sea', 32), ('Zalesye', 32), ('Anatolia', 32), ('Senegambia', 32), ('Niger River', 32), ('Guinea Coast',
                                                                                                                                                                                  32), ('Lake Tchad', 32), ('Kongo', 32), ('South Africa', 31), ('Monomotapa', 31), ('Zanj', 31), ('Red Sea', 29),
     ('Upper Nile', 29), ('Arabia', 29), ('Iran', 29), ('Khorasan', 29), ('Mawarannahr', 29), ('Yettishar', 29),
     ('Punjab', 28), ('Gurjaratra', 28), ('Konkan', 28), ('Deccan Plateau', 28), ('Tamilakam', 28), ('Kalinga', 27), ('Delhi', 27), ('Bihar', 27), ('Bengal', 27), ('Himalayan Plateau', 27), ('Ayeyarwady', 27), ('Chao Phraya', 16), ('Malacca Strait', 16), ('Mekong', 16), ('Moluccas', 16),
     ('Champa Sea', 25), ('Australia', 27), ('Liangguang', 25), ('Szechwan', 25), ('Huazhong', 33), ('Jiangnan', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 25), ('Eastern Siberia', 33), ('Nippon', 25),
     ('Far East', 16), ('Andes', 33), ('Southern Cone', 33), ('Guiana', 32), ('Amazonia', 33), ('Panama', 33), ('Caribbean', 33), ('Mexico', 33), ('Rio Grande', 33), ('Mississippi', 33), ('Plains', 33), ('Eastern Seaboard', 33), ('Canada', 33),
     ('American West Coast', 33), ('Pacific', 33)])
# Korea
expeditions_list.append(Expedition('korea', 'Korea', 400, 'Chinese Mainland', [7]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 32), ('East Atlantis Node', 32), ('South Atlantis Node', 32), ('North Atlantis Node', 32), ('Iberia', 32), ('Strait of Gibraltar', 32), ('Sahara', 32), ('West Mediterranean', 32), ('France', 32), ('Channel', 32), ('North Sea', 32), ('Barbary Coast', 32), ('Tyrrenean Sea', 32), ('Rhineland', 32), ('Lower Nile', 30), ('Po Valley', 32), ('Adriatic Sea', 32), ('Levant', 32),
     ('Aegean Sea', 32), ('Danube', 32), ('Elbe', 32), ('Baltic Sea', 32),
     ('Vistula', 32), ('Crimea', 32), ('Western Siberia', 32), ('Dnieper', 32), ('Caspian Sea', 32), ('Zalesye', 32), ('Anatolia', 32), ('Senegambia', 32), ('Niger River', 32), ('Guinea Coast',
                                                                                                                                                                                  32), ('Lake Tchad', 32), ('Kongo', 32), ('South Africa', 31), ('Monomotapa', 31), ('Zanj', 31), ('Red Sea', 30),
     ('Upper Nile', 30), ('Arabia', 30), ('Iran', 30), ('Khorasan', 30), ('Mawarannahr', 30), ('Yettishar', 30),
     ('Punjab', 29), ('Gurjaratra', 29), ('Konkan', 29), ('Deccan Plateau', 29), ('Tamilakam', 29), ('Kalinga', 29), ('Delhi', 29), ('Bihar', 29), ('Bengal', 29), ('Himalayan Plateau', 29), ('Ayeyarwady', 29), ('Chao Phraya', 16), ('Malacca Strait', 16), ('Mekong', 16), ('Moluccas', 16),
     ('Champa Sea', 25), ('Australia', 27), ('Liangguang', 25), ('Szechwan', 25), ('Huazhong', 25), ('Jiangnan', 25), ('Huabei', 25), ('Xibei', 25), ('Zhongyuan', 33), ('Eastern Siberia', 25), ('Nippon', 25),
     ('Far East', 25), ('Andes', 33), ('Southern Cone', 33), ('Guiana', 32), ('Amazonia', 33), ('Panama', 33), ('Caribbean', 33), ('Mexico', 33), ('Rio Grande', 33), ('Mississippi', 33), ('Plains', 33), ('Eastern Seaboard', 33), ('Canada', 33),
     ('American West Coast', 33), ('Pacific', 33)])
# Japan
expeditions_list.append(Expedition('japan', 'Japan', 400, 'Jumping Node', [10]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 32), ('East Atlantis Node', 32), ('South Atlantis Node', 32), ('North Atlantis Node', 32), ('Iberia', 32), ('Strait of Gibraltar', 32), ('Sahara', 32), ('West Mediterranean', 32), ('France', 32), ('Channel', 32), ('North Sea', 32), ('Barbary Coast', 32), ('Tyrrenean Sea', 32), ('Rhineland', 32), ('Lower Nile', 30), ('Po Valley', 32), ('Adriatic Sea', 32), ('Levant', 32),
     ('Aegean Sea', 32), ('Danube', 32), ('Elbe', 32), ('Baltic Sea', 32),
     ('Vistula', 32), ('Crimea', 32), ('Western Siberia', 32), ('Dnieper', 32), ('Caspian Sea', 32), ('Zalesye', 32), ('Anatolia', 32), ('Senegambia', 32), ('Niger River', 32), ('Guinea Coast',
                                                                                                                                                                                  32), ('Lake Tchad', 32), ('Kongo', 32), ('South Africa', 31), ('Monomotapa', 31), ('Zanj', 31), ('Red Sea', 30),
     ('Upper Nile', 30), ('Arabia', 30), ('Iran', 30), ('Khorasan', 30), ('Mawarannahr', 30), ('Yettishar', 30),
     ('Punjab', 29), ('Gurjaratra', 29), ('Konkan', 29), ('Deccan Plateau', 29), ('Tamilakam', 29), ('Kalinga', 29), ('Delhi', 29), ('Bihar', 29), ('Bengal', 29), ('Himalayan Plateau', 29), ('Ayeyarwady', 29), ('Chao Phraya', 16), ('Malacca Strait', 16), ('Mekong', 16), ('Moluccas', 16),
     ('Champa Sea', 25), ('Australia', 27), ('Liangguang', 25), ('Szechwan', 25), ('Huazhong', 25), ('Jiangnan', 25), ('Huabei', 25), ('Xibei', 25), ('Zhongyuan', 25), ('Eastern Siberia', 25), ('Nippon', 33),
     ('Far East', 25), ('Andes', 33), ('Southern Cone', 33), ('Guiana', 32), ('Amazonia', 33), ('Panama', 33), ('Caribbean', 33), ('Mexico', 33), ('Rio Grande', 33), ('Mississippi', 33), ('Plains', 33), ('Eastern Seaboard', 33), ('Canada', 33),
     ('American West Coast', 33), ('Pacific', 33)])

# Cuba
expeditions_list.append(Expedition('cuba', 'Cuba', 800, 'Colonial Node', [68]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 29), ('East Atlantis Node', 29), ('South Atlantis Node', 29), ('North Atlantis Node', 29), ('Iberia', 29), ('Strait of Gibraltar', 29), ('Sahara', 29), ('West Mediterranean', 29), ('France', 29), ('Channel', 29), ('North Sea', 29), ('Barbary Coast', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Lower Nile', 30), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levant', 30),
     ('Aegean Sea', 30), ('Danube', 30), ('Elbe', 30), ('Baltic Sea', 30),
     ('Vistula', 30), ('Crimea', 30), ('Western Siberia', 30), ('Dnieper', 30), ('Caspian Sea', 32), ('Zalesye', 30), ('Anatolia', 30), ('Senegambia', 29), ('Niger River', 29), ('Guinea Coast',
                                                                                                                                                                                  29), ('Lake Tchad', 29), ('Kongo', 29), ('South Africa', 30), ('Monomotapa', 30), ('Zanj', 30), ('Red Sea', 31),
     ('Upper Nile', 31), ('Arabia', 32), ('Iran', 32), ('Khorasan', 32), ('Mawarannahr', 32), ('Yettishar', 32),
     ('Punjab', 32), ('Gurjaratra', 32), ('Konkan', 32), ('Deccan Plateau', 32), ('Tamilakam', 32), ('Kalinga', 32), ('Delhi', 32), ('Bihar', 32), ('Bengal', 32), ('Himalayan Plateau', 32), ('Ayeyarwady', 32), ('Chao Phraya', 32), ('Malacca Strait', 32), ('Mekong', 32), ('Moluccas', 32),
     ('Champa Sea', 32), ('Australia', 32), ('Liangguang', 32), ('Szechwan', 32), ('Huazhong', 32), ('Jiangnan', 32), ('Huabei', 32), ('Xibei', 32), ('Zhongyuan', 32), ('Eastern Siberia', 32), ('Nippon', 32),
     ('Far East', 32), ('Andes', 29), ('Southern Cone', 27), ('Guiana', 16), ('Amazonia', 29), ('Panama', 25), ('Caribbean', 33), ('Mexico', 25), ('Rio Grande', 25), ('Mississippi', 25), ('Plains', 25), ('Eastern Seaboard', 25), ('Canada', 27),
     ('American West Coast', 30), ('Pacific', 33)])
# Hispaniola
expeditions_list.append(Expedition('hispaniola', 'Hispaniola', 800, 'Colonial Node', [68]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 29), ('East Atlantis Node', 29), ('South Atlantis Node', 29), ('North Atlantis Node', 29), ('Iberia', 29), ('Strait of Gibraltar', 29), ('Sahara', 29), ('West Mediterranean', 29), ('France', 29), ('Channel', 29), ('North Sea', 29), ('Barbary Coast', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Lower Nile', 30), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levant', 30),
     ('Aegean Sea', 30), ('Danube', 30), ('Elbe', 30), ('Baltic Sea', 30),
     ('Vistula', 30), ('Crimea', 30), ('Western Siberia', 30), ('Dnieper', 30), ('Caspian Sea', 30), ('Zalesye', 30), ('Anatolia', 30), ('Senegambia', 29), ('Niger River', 29), ('Guinea Coast',
                                                                                                                                                                                  29), ('Lake Tchad', 29), ('Kongo', 29), ('South Africa', 30), ('Monomotapa', 30), ('Zanj', 30), ('Red Sea', 31),
     ('Upper Nile', 31), ('Arabia', 32), ('Iran', 32), ('Khorasan', 32), ('Mawarannahr', 32), ('Yettishar', 32),
     ('Punjab', 32), ('Gurjaratra', 32), ('Konkan', 32), ('Deccan Plateau', 32), ('Tamilakam', 32), ('Kalinga', 32), ('Delhi', 32), ('Bihar', 32), ('Bengal', 32), ('Himalayan Plateau', 32), ('Ayeyarwady', 32), ('Chao Phraya', 32), ('Malacca Strait', 32), ('Mekong', 32), ('Moluccas', 32),
     ('Champa Sea', 32), ('Australia', 32), ('Liangguang', 32), ('Szechwan', 32), ('Huazhong', 32), ('Jiangnan', 32), ('Huabei', 32), ('Xibei', 32), ('Zhongyuan', 32), ('Eastern Siberia', 32), ('Nippon', 32),
     ('Far East', 32), ('Andes', 29), ('Southern Cone', 27), ('Guiana', 16), ('Amazonia', 29), ('Panama', 25), ('Caribbean', 33), ('Mexico', 25), ('Rio Grande', 25), ('Mississippi', 25), ('Plains', 25), ('Eastern Seaboard', 25), ('Canada', 27),
     ('American West Coast', 30), ('Pacific', 33)])
# Caribbean
expeditions_list.append(Expedition('caribbean', 'Caribbean', 800, 'Jumping Node', [68]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 29), ('East Atlantis Node', 29), ('South Atlantis Node', 29), ('North Atlantis Node', 29), ('Iberia', 29), ('Strait of Gibraltar', 29), ('Sahara', 29), ('West Mediterranean', 29), ('France', 29), ('Channel', 29), ('North Sea', 29), ('Barbary Coast', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Lower Nile', 30), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levant', 30),
     ('Aegean Sea', 30), ('Danube', 30), ('Elbe', 30), ('Baltic Sea', 30),
     ('Vistula', 30), ('Crimea', 30), ('Western Siberia', 30), ('Dnieper', 30), ('Caspian Sea', 30), ('Zalesye', 30), ('Anatolia', 30), ('Senegambia', 29), ('Niger River', 29), ('Guinea Coast',
                                                                                                                                                                                  29), ('Lake Tchad', 29), ('Kongo', 29), ('South Africa', 30), ('Monomotapa', 30), ('Zanj', 30), ('Red Sea', 31),
     ('Upper Nile', 31), ('Arabia', 32), ('Iran', 32), ('Khorasan', 32), ('Mawarannahr', 32), ('Yettishar', 32),
     ('Punjab', 32), ('Gurjaratra', 32), ('Konkan', 32), ('Deccan Plateau', 32), ('Tamilakam', 32), ('Kalinga', 32), ('Delhi', 32), ('Bihar', 32), ('Bengal', 32), ('Himalayan Plateau', 32), ('Ayeyarwady', 32), ('Chao Phraya', 32), ('Malacca Strait', 32), ('Mekong', 32), ('Moluccas', 32),
     ('Champa Sea', 32), ('Australia', 32), ('Liangguang', 32), ('Szechwan', 32), ('Huazhong', 32), ('Jiangnan', 32), ('Huabei', 32), ('Xibei', 32), ('Zhongyuan', 32), ('Eastern Siberia', 32), ('Nippon', 32),
     ('Far East', 32), ('Andes', 29), ('Southern Cone', 27), ('Guiana', 16), ('Amazonia', 28), ('Panama', 25), ('Caribbean', 33), ('Mexico', 25), ('Rio Grande', 25), ('Mississippi', 25), ('Plains', 25), ('Eastern Seaboard', 25), ('Canada', 27),
     ('American West Coast', 30), ('Pacific', 33)])
# Atlantic Colombia
expeditions_list.append(Expedition('atlantic_colombia', 'Atlantic Colombia', 300, 'Colonial Node', [46]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 30), ('East Atlantis Node', 30), ('South Atlantis Node', 30), ('North Atlantis Node', 30), ('Iberia', 30), ('Strait of Gibraltar', 30), ('Sahara', 30), ('West Mediterranean', 30), ('France', 30), ('Channel', 30), ('North Sea', 30), ('Barbary Coast', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Lower Nile', 30), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levant', 30),
     ('Aegean Sea', 30), ('Danube', 30), ('Elbe', 30), ('Baltic Sea', 30),
     ('Vistula', 30), ('Crimea', 30), ('Western Siberia', 30), ('Dnieper', 30), ('Caspian Sea', 30), ('Zalesye', 30), ('Anatolia', 30), ('Senegambia', 30), ('Niger River', 30), ('Guinea Coast',
                                                                                                                                                                                  30), ('Lake Tchad', 30), ('Kongo', 30), ('South Africa', 31), ('Monomotapa', 31), ('Zanj', 31), ('Red Sea', 33),
     ('Upper Nile', 33), ('Arabia', 33), ('Iran', 33), ('Khorasan', 33), ('Mawarannahr', 33), ('Yettishar', 33),
     ('Punjab', 33), ('Gurjaratra', 33), ('Konkan', 33), ('Deccan Plateau', 33), ('Tamilakam', 33), ('Kalinga', 33), ('Delhi', 33), ('Bihar', 33), ('Bengal', 33), ('Himalayan Plateau', 33), ('Ayeyarwady', 33), ('Chao Phraya', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Moluccas', 33),
     ('Champa Sea', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangnan', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Eastern Siberia', 33), ('Nippon', 33),
     ('Far East', 33), ('Andes', 29), ('Southern Cone', 16), ('Guiana', 25), ('Amazonia', 29), ('Panama', 33), ('Caribbean', 25), ('Mexico', 16), ('Rio Grande', 16), ('Mississippi', 16), ('Plains', 16), ('Eastern Seaboard', 16), ('Canada', 27),
     ('American West Coast', 30), ('Pacific', 33)])
# Guyana
expeditions_list.append(Expedition('guyana', 'Guyana', 300, 'Colonial Node', [46]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 30), ('East Atlantis Node', 30), ('South Atlantis Node', 30), ('North Atlantis Node', 30), ('Iberia', 30), ('Strait of Gibraltar', 30), ('Sahara', 30), ('West Mediterranean', 30), ('France', 30), ('Channel', 30), ('North Sea', 30), ('Barbary Coast', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Lower Nile', 30), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levant', 30),
     ('Aegean Sea', 30), ('Danube', 30), ('Elbe', 30), ('Baltic Sea', 30),
     ('Vistula', 30), ('Crimea', 30), ('Western Siberia', 30), ('Dnieper', 30), ('Caspian Sea', 30), ('Zalesye', 30), ('Anatolia', 30), ('Senegambia', 30), ('Niger River', 30), ('Guinea Coast',
                                                                                                                                                                                  30), ('Lake Tchad', 30), ('Kongo', 30), ('South Africa', 31), ('Monomotapa', 31), ('Zanj', 31), ('Red Sea', 33),
     ('Upper Nile', 33), ('Arabia', 33), ('Iran', 33), ('Khorasan', 33), ('Mawarannahr', 33), ('Yettishar', 33),
     ('Punjab', 33), ('Gurjaratra', 33), ('Konkan', 33), ('Deccan Plateau', 33), ('Tamilakam', 33), ('Kalinga', 33), ('Delhi', 33), ('Bihar', 33), ('Bengal', 33), ('Himalayan Plateau', 33), ('Ayeyarwady', 33), ('Chao Phraya', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Moluccas', 33),
     ('Champa Sea', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangnan', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Eastern Siberia', 33), ('Nippon', 33),
     ('Far East', 33), ('Andes', 29), ('Southern Cone', 16), ('Guiana', 25), ('Amazonia', 29), ('Panama', 33), ('Caribbean', 25), ('Mexico', 16), ('Rio Grande', 16), ('Mississippi', 16), ('Plains', 16), ('Eastern Seaboard', 16), ('Canada', 27),
     ('American West Coast', 30), ('Pacific', 33)])
# Atlantic Mexico
expeditions_list.append(Expedition('atlantic_mexico', 'Atlantic Mexico', 1600, 'Colonial Node', [45, 12]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 31), ('East Atlantis Node', 31), ('South Atlantis Node', 31), ('North Atlantis Node', 31), ('Iberia', 31), ('Strait of Gibraltar', 31), ('Sahara', 31), ('West Mediterranean', 31), ('France', 31), ('Channel', 31), ('North Sea', 31), ('Barbary Coast', 31), ('Tyrrenean Sea', 31), ('Rhineland', 31), ('Lower Nile', 31), ('Po Valley', 31), ('Adriatic Sea', 31), ('Levant', 31),
     ('Aegean Sea', 31), ('Danube', 31), ('Elbe', 31), ('Baltic Sea', 31),
     ('Vistula', 31), ('Crimea', 31), ('Western Siberia', 31), ('Dnieper', 31), ('Caspian Sea', 31), ('Zalesye', 31), ('Anatolia', 31), ('Senegambia', 31), ('Niger River', 31), ('Guinea Coast',
                                                                                                                                                                                  31), ('Lake Tchad', 31), ('Kongo', 31), ('South Africa', 31), ('Monomotapa', 31), ('Zanj', 31), ('Red Sea', 33),
     ('Upper Nile', 33), ('Arabia', 33), ('Iran', 33), ('Khorasan', 33), ('Mawarannahr', 33), ('Yettishar', 33),
     ('Punjab', 33), ('Gurjaratra', 33), ('Konkan', 33), ('Deccan Plateau', 33), ('Tamilakam', 33), ('Kalinga', 33), ('Delhi', 33), ('Bihar', 33), ('Bengal', 33), ('Himalayan Plateau', 33), ('Ayeyarwady', 33), ('Chao Phraya', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Moluccas', 33),
     ('Champa Sea', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangnan', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Eastern Siberia', 33), ('Nippon', 33),
     ('Far East', 33), ('Andes', 29), ('Southern Cone', 27), ('Guiana', 16), ('Amazonia', 29), ('Panama', 33), ('Caribbean', 25), ('Mexico', 33), ('Rio Grande', 33), ('Mississippi', 25), ('Plains', 25), ('Eastern Seaboard', 16), ('Canada', 27),
     ('American West Coast', 30), ('Pacific', 33)])
# Northern Brazil
expeditions_list.append(Expedition('north_brazil', 'Northern Brazil', 600, 'Colonial Node', [46]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 30), ('East Atlantis Node', 30), ('South Atlantis Node', 30), ('North Atlantis Node', 30), ('Iberia', 30), ('Strait of Gibraltar', 30), ('Sahara', 30), ('West Mediterranean', 30), ('France', 30), ('Channel', 30), ('North Sea', 30), ('Barbary Coast', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Lower Nile', 30), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levant', 30),
     ('Aegean Sea', 30), ('Danube', 30), ('Elbe', 30), ('Baltic Sea', 30),
     ('Vistula', 30), ('Crimea', 30), ('Western Siberia', 30), ('Dnieper', 30), ('Caspian Sea', 30), ('Zalesye', 30), ('Anatolia', 30), ('Senegambia', 27), ('Niger River', 27), ('Guinea Coast',
                                                                                                                                                                                  27), ('Lake Tchad', 27), ('Kongo', 28), ('South Africa', 29), ('Monomotapa', 30), ('Zanj', 30), ('Red Sea', 30),
     ('Upper Nile', 30), ('Arabia', 31), ('Iran', 31), ('Khorasan', 31), ('Mawarannahr', 31), ('Yettishar', 31),
     ('Punjab', 31), ('Gurjaratra', 31), ('Konkan', 31), ('Deccan Plateau', 31), ('Tamilakam', 31), ('Kalinga', 31), ('Delhi', 31), ('Bihar', 31), ('Bengal', 31), ('Himalayan Plateau', 31), ('Ayeyarwady', 31), ('Chao Phraya', 31), ('Malacca Strait', 31), ('Mekong', 31), ('Moluccas', 31),
     ('Champa Sea', 31), ('Australia', 32), ('Liangguang', 32), ('Szechwan', 32), ('Huazhong', 32), ('Jiangnan', 32), ('Huabei', 32), ('Xibei', 32), ('Zhongyuan', 32), ('Eastern Siberia', 32), ('Nippon', 32),
     ('Far East', 32), ('Andes', 27), ('Southern Cone', 33), ('Guiana', 33), ('Amazonia', 27), ('Panama', 16), ('Caribbean', 25), ('Mexico', 16), ('Rio Grande', 16), ('Mississippi', 16), ('Plains', 16), ('Eastern Seaboard', 16), ('Canada', 27),
     ('American West Coast', 29), ('Pacific', 33)])
# Southern Brazil
expeditions_list.append(Expedition('south_brazil', 'Southern Brazil', 600, 'Colonial Node', [19]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 30), ('East Atlantis Node', 30), ('South Atlantis Node', 30), ('North Atlantis Node', 30), ('Iberia', 30), ('Strait of Gibraltar', 30), ('Sahara', 30), ('West Mediterranean', 30), ('France', 30), ('Channel', 30), ('North Sea', 30), ('Barbary Coast', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Lower Nile', 30), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levant', 30),
     ('Aegean Sea', 30), ('Danube', 30), ('Elbe', 30), ('Baltic Sea', 30),
     ('Vistula', 30), ('Crimea', 30), ('Western Siberia', 30), ('Dnieper', 30), ('Caspian Sea', 30), ('Zalesye', 30), ('Anatolia', 30), ('Senegambia', 27), ('Niger River', 27), ('Guinea Coast',
                                                                                                                                                                                  27), ('Lake Tchad', 27), ('Kongo', 28), ('South Africa', 29), ('Monomotapa', 30), ('Zanj', 30), ('Red Sea', 30),
     ('Upper Nile', 30), ('Arabia', 31), ('Iran', 31), ('Khorasan', 31), ('Mawarannahr', 31), ('Yettishar', 31),
     ('Punjab', 31), ('Gurjaratra', 31), ('Konkan', 31), ('Deccan Plateau', 31), ('Tamilakam', 31), ('Kalinga', 31), ('Delhi', 31), ('Bihar', 31), ('Bengal', 31), ('Himalayan Plateau', 31), ('Ayeyarwady', 31), ('Chao Phraya', 31), ('Malacca Strait', 31), ('Mekong', 31), ('Moluccas', 31),
     ('Champa Sea', 31), ('Australia', 32), ('Liangguang', 32), ('Szechwan', 32), ('Huazhong', 32), ('Jiangnan', 32), ('Huabei', 32), ('Xibei', 32), ('Zhongyuan', 32), ('Eastern Siberia', 32), ('Nippon', 32),
     ('Far East', 32), ('Andes', 27), ('Southern Cone', 33), ('Guiana', 33), ('Amazonia', 27), ('Panama', 16), ('Caribbean', 25), ('Mexico', 16), ('Rio Grande', 16), ('Mississippi', 16), ('Plains', 16), ('Eastern Seaboard', 16), ('Canada', 27),
     ('American West Coast', 29), ('Pacific', 33)])
# the Gulf of Mexico
expeditions_list.append(Expedition('gulf_of_mexico', 'the Gulf of Mexico', 300, 'Colonial Node', [65, 66]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 25), ('East Atlantis Node', 25), ('South Atlantis Node', 25), ('North Atlantis Node', 25), ('Iberia', 25), ('Strait of Gibraltar', 25), ('Sahara', 25), ('West Mediterranean', 25), ('France', 25), ('Channel', 25), ('North Sea', 25), ('Barbary Coast', 25), ('Tyrrenean Sea', 25), ('Rhineland', 25), ('Lower Nile', 25), ('Po Valley', 25), ('Adriatic Sea', 25), ('Levant', 25),
     ('Aegean Sea', 25), ('Danube', 25), ('Elbe', 25), ('Baltic Sea', 25),
     ('Vistula', 25), ('Crimea', 25), ('Western Siberia', 25), ('Dnieper', 25), ('Caspian Sea', 25), ('Zalesye', 25), ('Anatolia', 25), ('Senegambia', 25), ('Niger River', 25), ('Guinea Coast',
                                                                                                                                                                                  25), ('Lake Tchad', 25), ('Kongo', 25), ('South Africa', 25), ('Monomotapa', 25), ('Zanj', 25), ('Red Sea', 25),
     ('Upper Nile', 25), ('Arabia', 25), ('Iran', 25), ('Khorasan', 25), ('Mawarannahr', 25), ('Yettishar', 25),
     ('Punjab', 25), ('Gurjaratra', 25), ('Konkan', 25), ('Deccan Plateau', 25), ('Tamilakam', 25), ('Kalinga', 25), ('Delhi', 25), ('Bihar', 25), ('Bengal', 25), ('Himalayan Plateau', 25), ('Ayeyarwady', 25), ('Chao Phraya', 25), ('Malacca Strait', 25), ('Mekong', 25), ('Moluccas', 25),
     ('Champa Sea', 25), ('Australia', 25), ('Liangguang', 25), ('Szechwan', 25), ('Huazhong', 25), ('Jiangnan', 25), ('Huabei', 25), ('Xibei', 25), ('Zhongyuan', 25), ('Eastern Siberia', 25), ('Nippon', 25),
     ('Far East', 25), ('Andes', 29), ('Southern Cone', 27), ('Guiana', 16), ('Amazonia', 29), ('Panama', 25), ('Caribbean', 25), ('Mexico', 25), ('Rio Grande', 33), ('Mississippi', 33), ('Plains', 33), ('Eastern Seaboard', 25), ('Canada', 27),
     ('American West Coast', 30), ('Pacific', 33)])
# Southeastern America
expeditions_list.append(Expedition('southeastern_america', 'Southeastern America', 400, 'Colonial Node', [69, 66]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 33), ('East Atlantis Node', 33), ('South Atlantis Node', 33), ('North Atlantis Node', 33), ('Iberia', 33), ('Strait of Gibraltar', 33), ('Sahara', 33), ('West Mediterranean', 33), ('France', 33), ('Channel', 33), ('North Sea', 33), ('Barbary Coast', 33), ('Tyrrenean Sea', 33), ('Rhineland', 33), ('Lower Nile', 33), ('Po Valley', 33), ('Adriatic Sea', 33), ('Levant', 33),
     ('Aegean Sea', 33), ('Danube', 33), ('Elbe', 33), ('Baltic Sea', 33),
     ('Vistula', 33), ('Crimea', 33), ('Western Siberia', 33), ('Dnieper', 33), ('Caspian Sea', 33), ('Zalesye', 33), ('Anatolia', 33), ('Senegambia', 33), ('Niger River', 33), ('Guinea Coast',
                                                                                                                                                                                  33), ('Lake Tchad', 33), ('Kongo', 33), ('South Africa', 33), ('Monomotapa', 33), ('Zanj', 33), ('Red Sea', 33),
     ('Upper Nile', 33), ('Arabia', 33), ('Iran', 33), ('Khorasan', 33), ('Mawarannahr', 33), ('Yettishar', 33),
     ('Punjab', 33), ('Gurjaratra', 33), ('Konkan', 33), ('Deccan Plateau', 33), ('Tamilakam', 33), ('Kalinga', 33), ('Delhi', 33), ('Bihar', 33), ('Bengal', 33), ('Himalayan Plateau', 33), ('Ayeyarwady', 33), ('Chao Phraya', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Moluccas', 33),
     ('Champa Sea', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangnan', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Eastern Siberia', 33), ('Nippon', 33),
     ('Far East', 33), ('Andes', 29), ('Southern Cone', 27), ('Guiana', 16), ('Amazonia', 29), ('Panama', 16), ('Caribbean', 25), ('Mexico', 25), ('Rio Grande', 25), ('Mississippi', 33), ('Plains', 33), ('Eastern Seaboard', 33), ('Canada', 25),
     ('American West Coast', 30), ('Pacific', 33)])
# Eastern America
expeditions_list.append(Expedition('eastern_america', 'Eastern America', 400, 'Colonial Node', [69]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 25), ('East Atlantis Node', 25), ('South Atlantis Node', 25), ('North Atlantis Node', 25), ('Iberia', 25), ('Strait of Gibraltar', 25), ('Sahara', 25), ('West Mediterranean', 25), ('France', 25), ('Channel', 25), ('North Sea', 25), ('Barbary Coast', 25), ('Tyrrenean Sea', 25), ('Rhineland', 25), ('Lower Nile', 25), ('Po Valley', 25), ('Adriatic Sea', 25), ('Levant', 25),
     ('Aegean Sea', 25), ('Danube', 25), ('Elbe', 25), ('Baltic Sea', 25),
     ('Vistula', 25), ('Crimea', 25), ('Western Siberia', 25), ('Dnieper', 25), ('Caspian Sea', 25), ('Zalesye', 25), ('Anatolia', 25), ('Senegambia', 25), ('Niger River', 25), ('Guinea Coast',
                                                                                                                                                                                  25), ('Lake Tchad', 25), ('Kongo', 25), ('South Africa', 25), ('Monomotapa', 25), ('Zanj', 25), ('Red Sea', 25),
     ('Upper Nile', 25), ('Arabia', 25), ('Iran', 25), ('Khorasan', 25), ('Mawarannahr', 25), ('Yettishar', 25),
     ('Punjab', 25), ('Gurjaratra', 25), ('Konkan', 25), ('Deccan Plateau', 25), ('Tamilakam', 25), ('Kalinga', 25), ('Delhi', 25), ('Bihar', 25), ('Bengal', 25), ('Himalayan Plateau', 25), ('Ayeyarwady', 25), ('Chao Phraya', 25), ('Malacca Strait', 25), ('Mekong', 25), ('Moluccas', 25),
     ('Champa Sea', 25), ('Australia', 25), ('Liangguang', 25), ('Szechwan', 25), ('Huazhong', 25), ('Jiangnan', 25), ('Huabei', 25), ('Xibei', 25), ('Zhongyuan', 25), ('Eastern Siberia', 25), ('Nippon', 25),
     ('Far East', 25), ('Andes', 30), ('Southern Cone', 29), ('Guiana', 29), ('Amazonia', 30), ('Panama', 16), ('Caribbean', 16), ('Mexico', 16), ('Rio Grande', 16), ('Mississippi', 16), ('Plains', 16), ('Eastern Seaboard', 33), ('Canada', 25),
     ('American West Coast', 31), ('Pacific', 33)])
# Canada
expeditions_list.append(Expedition('canada', 'Canada', 300, 'Colonial Node', [67]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 25), ('East Atlantis Node', 25), ('South Atlantis Node', 25), ('North Atlantis Node', 25), ('Iberia', 25), ('Strait of Gibraltar', 25), ('Sahara', 25), ('West Mediterranean', 25), ('France', 25), ('Channel', 25), ('North Sea', 25), ('Barbary Coast', 25), ('Tyrrenean Sea', 25), ('Rhineland', 25), ('Lower Nile', 25), ('Po Valley', 25), ('Adriatic Sea', 25), ('Levant', 25),
     ('Aegean Sea', 25), ('Danube', 25), ('Elbe', 25), ('Baltic Sea', 25),
     ('Vistula', 25), ('Crimea', 25), ('Western Siberia', 25), ('Dnieper', 25), ('Caspian Sea', 25), ('Zalesye', 25), ('Anatolia', 25), ('Senegambia', 25), ('Niger River', 25), ('Guinea Coast',
                                                                                                                                                                                  25), ('Lake Tchad', 25), ('Kongo', 25), ('South Africa', 25), ('Monomotapa', 25), ('Zanj', 25), ('Red Sea', 25),
     ('Upper Nile', 25), ('Arabia', 25), ('Iran', 25), ('Khorasan', 25), ('Mawarannahr', 25), ('Yettishar', 25),
     ('Punjab', 25), ('Gurjaratra', 25), ('Konkan', 25), ('Deccan Plateau', 25), ('Tamilakam', 25), ('Kalinga', 25), ('Delhi', 25), ('Bihar', 25), ('Bengal', 25), ('Himalayan Plateau', 25), ('Ayeyarwady', 25), ('Chao Phraya', 25), ('Malacca Strait', 25), ('Mekong', 25), ('Moluccas', 25),
     ('Champa Sea', 25), ('Australia', 25), ('Liangguang', 25), ('Szechwan', 25), ('Huazhong', 25), ('Jiangnan', 25), ('Huabei', 25), ('Xibei', 25), ('Zhongyuan', 25), ('Eastern Siberia', 25), ('Nippon', 25),
     ('Far East', 25), ('Andes', 25), ('Southern Cone', 25), ('Guiana', 25), ('Amazonia', 25), ('Panama', 25), ('Caribbean', 25), ('Mexico', 25), ('Rio Grande', 25), ('Mississippi', 25), ('Plains', 25), ('Eastern Seaboard', 25), ('Canada', 33),
     ('American West Coast', 25), ('Pacific', 33)])
# the North Atlantic
expeditions_list.append(Expedition('north_atlantic', 'the North Atlantic', 50, 'Jumping Node', [88]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 30), ('East Atlantis Node', 30), ('South Atlantis Node', 30), ('North Atlantis Node', 30), ('Iberia', 30), ('Strait of Gibraltar', 30), ('Sahara', 30), ('West Mediterranean', 30), ('France', 30), ('Channel', 30), ('North Sea', 30), ('Barbary Coast', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Lower Nile', 30), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levant', 30),
     ('Aegean Sea', 30), ('Danube', 30), ('Elbe', 30), ('Baltic Sea', 30),
     ('Vistula', 30), ('Crimea', 30), ('Western Siberia', 30), ('Dnieper', 30), ('Caspian Sea', 30), ('Zalesye', 30), ('Anatolia', 30), ('Senegambia', 30), ('Niger River', 30), ('Guinea Coast',
                                                                                                                                                                                  30), ('Lake Tchad', 30), ('Kongo', 30), ('South Africa', 30), ('Monomotapa', 30), ('Zanj', 30), ('Red Sea', 30),
     ('Upper Nile', 30), ('Arabia', 30), ('Iran', 30), ('Khorasan', 30), ('Mawarannahr', 30), ('Yettishar', 30),
     ('Punjab', 30), ('Gurjaratra', 30), ('Konkan', 30), ('Deccan Plateau', 30), ('Tamilakam', 30), ('Kalinga', 30), ('Delhi', 30), ('Bihar', 30), ('Bengal', 30), ('Himalayan Plateau', 30), ('Ayeyarwady', 30), ('Chao Phraya', 30), ('Malacca Strait', 30), ('Mekong', 30), ('Moluccas', 30),
     ('Champa Sea', 30), ('Australia', 30), ('Liangguang', 30), ('Szechwan', 30), ('Huazhong', 30), ('Jiangnan', 30), ('Huabei', 30), ('Xibei', 30), ('Zhongyuan', 30), ('Eastern Siberia', 30), ('Nippon', 30),
     ('Far East', 30), ('Andes', 30), ('Southern Cone', 30), ('Guiana', 30), ('Amazonia', 30), ('Panama', 30), ('Caribbean', 30), ('Mexico', 30), ('Rio Grande', 30), ('Mississippi', 30), ('Plains', 30), ('Eastern Seaboard', 30), ('Canada', 30),
     ('American West Coast', 30), ('Pacific', 33)])
# Hudson Bay
expeditions_list.append(Expedition('hudson_bay', 'Hudson Bay', 100, 'Colonial Node', [67]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 35), ('East Atlantis Node', 35), ('South Atlantis Node', 35), ('North Atlantis Node', 35), ('Iberia', 35), ('Strait of Gibraltar', 35), ('Sahara', 35), ('West Mediterranean', 35), ('France', 35), ('Channel', 35), ('North Sea', 35), ('Barbary Coast', 35), ('Tyrrenean Sea', 35), ('Rhineland', 35), ('Lower Nile', 35), ('Po Valley', 35), ('Adriatic Sea', 35), ('Levant', 35),
     ('Aegean Sea', 35), ('Danube', 35), ('Elbe', 35), ('Baltic Sea', 35),
     ('Vistula', 35), ('Crimea', 35), ('Western Siberia', 35), ('Dnieper', 35), ('Caspian Sea', 35), ('Zalesye', 35), ('Anatolia', 35), ('Senegambia', 35), ('Niger River', 35), ('Guinea Coast',
                                                                                                                                                                                  35), ('Lake Tchad', 35), ('Kongo', 35), ('South Africa', 35), ('Monomotapa', 35), ('Zanj', 35), ('Red Sea', 35),
     ('Upper Nile', 35), ('Arabia', 35), ('Iran', 35), ('Khorasan', 35), ('Mawarannahr', 35), ('Yettishar', 35),
     ('Punjab', 35), ('Gurjaratra', 35), ('Konkan', 35), ('Deccan Plateau', 35), ('Tamilakam', 35), ('Kalinga', 35), ('Delhi', 35), ('Bihar', 35), ('Bengal', 35), ('Himalayan Plateau', 35), ('Ayeyarwady', 35), ('Chao Phraya', 35), ('Malacca Strait', 35), ('Mekong', 35), ('Moluccas', 35),
     ('Champa Sea', 35), ('Australia', 35), ('Liangguang', 35), ('Szechwan', 35), ('Huazhong', 35), ('Jiangnan', 35), ('Huabei', 35), ('Xibei', 35), ('Zhongyuan', 35), ('Eastern Siberia', 35), ('Nippon', 35),
     ('Far East', 35), ('Andes', 35), ('Southern Cone', 35), ('Guiana', 35), ('Amazonia', 35), ('Panama', 35), ('Caribbean', 35), ('Mexico', 35), ('Rio Grande', 35), ('Mississippi', 35), ('Plains', 35), ('Eastern Seaboard', 35), ('Canada', 33),
     ('American West Coast', 35), ('Pacific', 35)])
# Southern Cone
expeditions_list.append(Expedition('la_plata', 'Southern Cone', 100, 'Colonial Node', [19]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 33), ('East Atlantis Node', 33), ('South Atlantis Node', 33), ('North Atlantis Node', 33), ('Iberia', 33), ('Strait of Gibraltar', 33), ('Sahara', 33), ('West Mediterranean', 33), ('France', 33), ('Channel', 33), ('North Sea', 33), ('Barbary Coast', 33), ('Tyrrenean Sea', 33), ('Rhineland', 33), ('Lower Nile', 33), ('Po Valley', 33), ('Adriatic Sea', 33), ('Levant', 33),
     ('Aegean Sea', 33), ('Danube', 33), ('Elbe', 33), ('Baltic Sea', 33),
     ('Vistula', 33), ('Crimea', 33), ('Western Siberia', 33), ('Dnieper', 33), ('Caspian Sea', 33), ('Zalesye', 33), ('Anatolia', 33), ('Senegambia', 30), ('Niger River', 30), ('Guinea Coast',
                                                                                                                                                                                  30), ('Lake Tchad', 30), ('Kongo', 31), ('South Africa', 33), ('Monomotapa', 33), ('Zanj', 33), ('Red Sea', 33),
     ('Upper Nile', 33), ('Arabia', 33), ('Iran', 33), ('Khorasan', 33), ('Mawarannahr', 33), ('Yettishar', 33),
     ('Punjab', 33), ('Gurjaratra', 33), ('Konkan', 33), ('Deccan Plateau', 33), ('Tamilakam', 33), ('Kalinga', 33), ('Delhi', 33), ('Bihar', 33), ('Bengal', 33), ('Himalayan Plateau', 33), ('Ayeyarwady', 33), ('Chao Phraya', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Moluccas', 33),
     ('Champa Sea', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangnan', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Eastern Siberia', 33), ('Nippon', 33),
     ('Far East', 33), ('Andes', 16), ('Southern Cone', 33), ('Guiana', 25), ('Amazonia', 16), ('Panama', 27), ('Caribbean', 27), ('Mexico', 27), ('Rio Grande', 27), ('Mississippi', 27), ('Plains', 27), ('Eastern Seaboard', 27), ('Canada', 29),
     ('American West Coast', 29), ('Pacific', 33)])
# California
expeditions_list.append(Expedition('california', 'California', 100, 'Colonial Node', [11]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 30), ('East Atlantis Node', 30), ('South Atlantis Node', 30), ('North Atlantis Node', 30), ('Iberia', 30), ('Strait of Gibraltar', 30), ('Sahara', 30), ('West Mediterranean', 30), ('France', 30), ('Channel', 30), ('North Sea', 30), ('Barbary Coast', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Lower Nile', 30), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levant', 30),
     ('Aegean Sea', 30), ('Danube', 30), ('Elbe', 30), ('Baltic Sea', 30),
     ('Vistula', 30), ('Crimea', 30), ('Western Siberia', 30), ('Dnieper', 30), ('Caspian Sea', 30), ('Zalesye', 30), ('Anatolia', 30), ('Senegambia', 30), ('Niger River', 30), ('Guinea Coast',
                                                                                                                                                                                  30), ('Lake Tchad', 30), ('Kongo', 30), ('South Africa', 30), ('Monomotapa', 30), ('Zanj', 30), ('Red Sea', 25),
     ('Upper Nile', 25), ('Arabia', 25), ('Iran', 25), ('Khorasan', 25), ('Mawarannahr', 25), ('Yettishar', 25),
     ('Punjab', 25), ('Gurjaratra', 25), ('Konkan', 25), ('Deccan Plateau', 25), ('Tamilakam', 25), ('Kalinga', 25), ('Delhi', 25), ('Bihar', 25), ('Bengal', 25), ('Himalayan Plateau', 25), ('Ayeyarwady', 25), ('Chao Phraya', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Moluccas', 33),
     ('Champa Sea', 33), ('Australia', 33), ('Liangguang', 31), ('Szechwan', 31), ('Huazhong', 31), ('Jiangnan', 31), ('Huabei', 31), ('Xibei', 31), ('Zhongyuan', 30), ('Eastern Siberia', 30), ('Nippon', 30),
     ('Far East', 30), ('Andes', 27), ('Southern Cone', 29), ('Guiana', 29), ('Amazonia', 27), ('Panama', 16), ('Caribbean', 29), ('Mexico', 25), ('Rio Grande', 25), ('Mississippi', 29), ('Plains', 29), ('Eastern Seaboard', 29), ('Canada', 30),
     ('American West Coast', 33), ('Pacific', 33)])
# Alaska
expeditions_list.append(Expedition('alaska', 'Alaska', 100, 'Colonial Node', [11]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 37), ('East Atlantis Node', 37), ('South Atlantis Node', 37), ('North Atlantis Node', 37), ('Iberia', 37), ('Strait of Gibraltar', 37), ('Sahara', 37), ('West Mediterranean', 37), ('France', 37), ('Channel', 37), ('North Sea', 37), ('Barbary Coast', 37), ('Tyrrenean Sea', 37), ('Rhineland', 37), ('Lower Nile', 37), ('Po Valley', 37), ('Adriatic Sea', 37), ('Levant', 37),
     ('Aegean Sea', 37), ('Danube', 37), ('Elbe', 37), ('Baltic Sea', 37),
     ('Vistula', 37), ('Crimea', 37), ('Western Siberia', 37), ('Dnieper', 37), ('Caspian Sea', 37), ('Zalesye', 37), ('Anatolia', 37), ('Senegambia', 37), ('Niger River', 37), ('Guinea Coast',
                                                                                                                                                                                  37), ('Lake Tchad', 37), ('Kongo', 37), ('South Africa', 37), ('Monomotapa', 37), ('Zanj', 37), ('Red Sea', 37),
     ('Upper Nile', 37), ('Arabia', 37), ('Iran', 37), ('Khorasan', 37), ('Mawarannahr', 37), ('Yettishar', 37),
     ('Punjab', 37), ('Gurjaratra', 37), ('Konkan', 37), ('Deccan Plateau', 37), ('Tamilakam', 37), ('Kalinga', 37), ('Delhi', 37), ('Bihar', 37), ('Bengal', 37), ('Himalayan Plateau', 37), ('Ayeyarwady', 37), ('Chao Phraya', 37), ('Malacca Strait', 37), ('Mekong', 37), ('Moluccas', 37),
     ('Champa Sea', 37), ('Australia', 37), ('Liangguang', 37), ('Szechwan', 37), ('Huazhong', 37), ('Jiangnan', 37), ('Huabei', 37), ('Xibei', 37), ('Zhongyuan', 37), ('Eastern Siberia', 30), ('Nippon', 30),
     ('Far East', 30), ('Andes', 30), ('Southern Cone', 30), ('Guiana', 30), ('Amazonia', 30), ('Panama', 30), ('Caribbean', 30), ('Mexico', 30), ('Rio Grande', 30), ('Mississippi', 30), ('Plains', 30), ('Eastern Seaboard', 30), ('Canada', 25),
     ('American West Coast', 33), ('Pacific', 33)])
# Pacific Mexico
expeditions_list.append(Expedition('pacific_mexico', 'Pacific Mexico', 800, 'Colonial Node', [12, 65]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 33), ('East Atlantis Node', 33), ('South Atlantis Node', 33), ('North Atlantis Node', 33), ('Iberia', 33), ('Strait of Gibraltar', 33), ('Sahara', 33), ('West Mediterranean', 33), ('France', 33), ('Channel', 33), ('North Sea', 33), ('Barbary Coast', 33), ('Tyrrenean Sea', 33), ('Rhineland', 33), ('Lower Nile', 33), ('Po Valley', 33), ('Adriatic Sea', 33), ('Levant', 33),
     ('Aegean Sea', 33), ('Danube', 33), ('Elbe', 33), ('Baltic Sea', 33), ('Vistula', 33), ('Crimea', 33), ('Western Siberia', 33), ('Dnieper', 33), ('Caspian Sea', 33), ('Zalesye', 33), ('Anatolia', 33), ('Senegambia', 33), ('Niger River', 33), ('Guinea Coast',
                                                                                                                                                                                                                                                        33), ('Lake Tchad', 33), ('Kongo', 33),
     ('South Africa', 33), ('Monomotapa', 33), ('Zanj', 33), ('Red Sea', 33), ('Upper Nile', 33), ('Arabia', 33), ('Iran', 33), ('Khorasan', 33), ('Mawarannahr', 33), ('Yettishar', 33),
     ('Punjab', 33), ('Gurjaratra', 33), ('Konkan', 33), ('Deccan Plateau', 33), ('Tamilakam', 33), ('Kalinga', 33), ('Delhi', 33), ('Bihar', 33), ('Bengal', 33), ('Himalayan Plateau', 33), ('Ayeyarwady', 33), ('Chao Phraya', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Moluccas', 33),
     ('Champa Sea', 33), ('Australia', 33), ('Liangguang', 32), ('Szechwan', 32), ('Huazhong', 32), ('Jiangnan', 32), ('Huabei', 32), ('Xibei', 32), ('Zhongyuan', 31), ('Eastern Siberia', 31), ('Nippon', 31),
     ('Far East', 31), ('Andes', 16), ('Southern Cone', 27), ('Guiana', 27), ('Amazonia', 16), ('Panama', 25), ('Caribbean', 29), ('Mexico', 25), ('Rio Grande', 33), ('Mississippi', 29), ('Plains', 29), ('Eastern Seaboard', 29), ('Canada', 30),
     ('American West Coast', 25), ('Pacific', 33)])
# Pacific Central America
expeditions_list.append(Expedition('pacific_central_america', 'Pacific Central America', 1300, 'Colonial Node', [45]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 33), ('East Atlantis Node', 33), ('South Atlantis Node', 33), ('North Atlantis Node', 33), ('Iberia', 33), ('Strait of Gibraltar', 33), ('Sahara', 33), ('West Mediterranean', 33), ('France', 33), ('Channel', 33), ('North Sea', 33), ('Barbary Coast', 33), ('Tyrrenean Sea', 33), ('Rhineland', 33), ('Lower Nile', 33), ('Po Valley', 33), ('Adriatic Sea', 33), ('Levant', 33),
     ('Aegean Sea', 33), ('Danube', 33), ('Elbe', 33), ('Baltic Sea', 33),
     ('Vistula', 33), ('Crimea', 33), ('Western Siberia', 33), ('Dnieper', 33), ('Caspian Sea', 33), ('Zalesye', 33), ('Anatolia', 33), ('Senegambia', 33), ('Niger River', 33), ('Guinea Coast',
                                                                                                                                                                                  33), ('Lake Tchad', 33), ('Kongo', 33), ('South Africa', 33), ('Monomotapa', 33), ('Zanj', 33), ('Red Sea', 33),
     ('Upper Nile', 33), ('Arabia', 33), ('Iran', 33), ('Khorasan', 33), ('Mawarannahr', 33), ('Yettishar', 33),
     ('Punjab', 33), ('Gurjaratra', 33), ('Konkan', 33), ('Deccan Plateau', 33), ('Tamilakam', 33), ('Kalinga', 33), ('Delhi', 33), ('Bihar', 33), ('Bengal', 33), ('Himalayan Plateau', 33), ('Ayeyarwady', 33), ('Chao Phraya', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Moluccas', 33),
     ('Champa Sea', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangnan', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 32), ('Eastern Siberia', 32), ('Nippon', 32),
     ('Far East', 32), ('Andes', 25), ('Southern Cone', 27), ('Guiana', 27), ('Amazonia', 25), ('Panama', 33), ('Caribbean', 29), ('Mexico', 25), ('Rio Grande', 25), ('Mississippi', 29), ('Plains', 29), ('Eastern Seaboard', 29), ('Canada', 30),
     ('American West Coast', 16), ('Pacific', 33)])
# Peru
expeditions_list.append(Expedition('peru', 'Peru', 2400, 'Colonial Node', [18]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 33), ('East Atlantis Node', 33), ('South Atlantis Node', 33), ('North Atlantis Node', 33), ('Iberia', 33), ('Strait of Gibraltar', 33), ('Sahara', 33), ('West Mediterranean', 33), ('France', 33), ('Channel', 33), ('North Sea', 33), ('Barbary Coast', 33), ('Tyrrenean Sea', 33), ('Rhineland', 33), ('Lower Nile', 33), ('Po Valley', 33), ('Adriatic Sea', 33), ('Levant', 33),
     ('Aegean Sea', 33), ('Danube', 33), ('Elbe', 33), ('Baltic Sea', 33),
     ('Vistula', 33), ('Crimea', 33), ('Western Siberia', 33), ('Dnieper', 33), ('Caspian Sea', 33), ('Zalesye', 33), ('Anatolia', 33), ('Senegambia', 33), ('Niger River', 33), ('Guinea Coast',
                                                                                                                                                                                  33), ('Lake Tchad', 33), ('Kongo', 33), ('South Africa', 33), ('Monomotapa', 33), ('Zanj', 33), ('Red Sea', 33),
     ('Upper Nile', 33), ('Arabia', 33), ('Iran', 33), ('Khorasan', 33), ('Mawarannahr', 33), ('Yettishar', 33),
     ('Punjab', 33), ('Gurjaratra', 33), ('Konkan', 33), ('Deccan Plateau', 33), ('Tamilakam', 33), ('Kalinga', 33), ('Delhi', 33), ('Bihar', 33), ('Bengal', 33), ('Himalayan Plateau', 33), ('Ayeyarwady', 33), ('Chao Phraya', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Moluccas', 33),
     ('Champa Sea', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangnan', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Eastern Siberia', 33), ('Nippon', 33),
     ('Far East', 33), ('Andes', 33), ('Southern Cone', 16), ('Guiana', 27), ('Amazonia', 33), ('Panama', 16), ('Caribbean', 29), ('Mexico', 16), ('Rio Grande', 27), ('Mississippi', 29), ('Plains', 29), ('Eastern Seaboard', 29), ('Canada', 30),
     ('American West Coast', 27), ('Pacific', 33)])
# Chile
expeditions_list.append(Expedition('chile', 'Chile', 400, 'Colonial Node', [18]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 33), ('East Atlantis Node', 33), ('South Atlantis Node', 33), ('North Atlantis Node', 33), ('Iberia', 33), ('Strait of Gibraltar', 33), ('Sahara', 33), ('West Mediterranean', 33), ('France', 33), ('Channel', 33), ('North Sea', 33), ('Barbary Coast', 33), ('Tyrrenean Sea', 33), ('Rhineland', 33), ('Lower Nile', 33), ('Po Valley', 33), ('Adriatic Sea', 33), ('Levant', 33),
     ('Aegean Sea', 33), ('Danube', 33), ('Elbe', 33), ('Baltic Sea', 33),
     ('Vistula', 33), ('Crimea', 33), ('Western Siberia', 33), ('Dnieper', 33), ('Caspian Sea', 33), ('Zalesye', 33), ('Anatolia', 33), ('Senegambia', 33), ('Niger River', 33), ('Guinea Coast',
                                                                                                                                                                                  33), ('Lake Tchad', 33), ('Kongo', 33), ('South Africa', 33), ('Monomotapa', 33), ('Zanj', 33), ('Red Sea', 33),
     ('Upper Nile', 33), ('Arabia', 33), ('Iran', 33), ('Khorasan', 33), ('Mawarannahr', 33), ('Yettishar', 33),
     ('Punjab', 33), ('Gurjaratra', 33), ('Konkan', 33), ('Deccan Plateau', 33), ('Tamilakam', 33), ('Kalinga', 33), ('Delhi', 33), ('Bihar', 33), ('Bengal', 33), ('Himalayan Plateau', 33), ('Ayeyarwady', 33), ('Chao Phraya', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Moluccas', 33),
     ('Champa Sea', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangnan', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Eastern Siberia', 33), ('Nippon', 33),
     ('Far East', 33), ('Andes', 33), ('Southern Cone', 16), ('Guiana', 27), ('Amazonia', 33), ('Panama', 16), ('Caribbean', 29), ('Mexico', 16), ('Rio Grande', 27), ('Mississippi', 29), ('Plains', 29), ('Eastern Seaboard', 29), ('Canada', 30),
     ('American West Coast', 27), ('Pacific', 33)])
#South Atlantis Node
expeditions_list.append(Expedition('south_atlantis_node', 'South Atlantis Node', 0, 'Jumping Node', [70]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('South Atlantis Node', 33), ('East Atlantis Node', 25), ('West Atlantis Node', 25), ('North Atlantis Node', 25), ('Iberia', 25), ('Strait of Gibraltar', 25), ('West Mediterranean', 25), ('France', 25), ('Channel', 25), ('North Sea', 25), ('Barbary Coast', 25), ('Tyrrenean Sea', 25), ('Rhineland', 33), ('Lower Nile', 25), ('Po Valley', 25), ('Adriatic Sea', 25), ('Levant', 25), ('Aegean Sea', 25),
     ('Danube', 25), ('Elbe', 33), ('Baltic Sea', 25), ('Vistula', 25), ('Crimea', 25), ('Western Siberia', 25), ('Dnieper', 25), ('Caspian Sea', 25), ('Zalesye', 25), ('Anatolia', 25), ('Sahara', 25), ('Senegambia', 27), ('Niger River', 27), ('Guinea Coast',
                                                                                                                                                                                                                                                    28), ('Lake Tchad', 28), ('Kongo', 28),
     ('South Africa', 30), ('Monomotapa', 30), ('Zanj', 30), ('Red Sea', 32), ('Upper Nile', 32), ('Arabia', 32), ('Iran', 32), ('Khorasan', 32), ('Mawarannahr', 32), ('Yettishar', 32),
     ('Punjab', 32), ('Gurjaratra', 32), ('Konkan', 32), ('Deccan Plateau', 32), ('Tamilakam', 32), ('Kalinga', 32), ('Delhi', 32), ('Bihar', 32), ('Bengal', 32), ('Himalayan Plateau', 32), ('Ayeyarwady', 32), ('Chao Phraya', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Moluccas', 33),
     ('Champa Sea', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangnan', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Eastern Siberia', 33), ('Nippon', 33),
     ('Far East', 33), ('Andes', 32), ('Southern Cone', 31), ('Guiana', 30), ('Amazonia', 32), ('Panama', 31), ('Caribbean', 30), ('Mexico', 31), ('Rio Grande', 31), ('Mississippi', 31), ('Plains', 31), ('Eastern Seaboard', 29), ('Canada', 29),
     ('American West Coast', 33), ('Pacific', 33)])
#North Atlantis Node
expeditions_list.append(Expedition('north_atlantis_node', 'North Atlantis Node', 0, 'Jumping Node', [82]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('North Atlantis Node', 33), ('East Atlantis Node', 25), ('West Atlantis Node', 25), ('South Atlantis Node', 25), ('Iberia', 25), ('Strait of Gibraltar', 25), ('West Mediterranean', 25), ('France', 25), ('Channel', 25), ('North Sea', 25), ('Barbary Coast', 25), ('Tyrrenean Sea', 25), ('Rhineland', 33), ('Lower Nile', 25), ('Po Valley', 25), ('Adriatic Sea', 25), ('Levant', 25), ('Aegean Sea', 25),
     ('Danube', 25), ('Elbe', 33), ('Baltic Sea', 25), ('Vistula', 25), ('Crimea', 25), ('Western Siberia', 25), ('Dnieper', 25), ('Caspian Sea', 25), ('Zalesye', 25), ('Anatolia', 25), ('Sahara', 25), ('Senegambia', 27), ('Niger River', 27), ('Guinea Coast',
                                                                                                                                                                                                                                                    28), ('Lake Tchad', 28), ('Kongo', 28),
     ('South Africa', 30), ('Monomotapa', 30), ('Zanj', 30), ('Red Sea', 32), ('Upper Nile', 32), ('Arabia', 32), ('Iran', 32), ('Khorasan', 32), ('Mawarannahr', 32), ('Yettishar', 32),
     ('Punjab', 32), ('Gurjaratra', 32), ('Konkan', 32), ('Deccan Plateau', 32), ('Tamilakam', 32), ('Kalinga', 32), ('Delhi', 32), ('Bihar', 32), ('Bengal', 32), ('Himalayan Plateau', 32), ('Ayeyarwady', 32), ('Chao Phraya', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Moluccas', 33),
     ('Champa Sea', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangnan', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Eastern Siberia', 33), ('Nippon', 33),
     ('Far East', 33), ('Andes', 32), ('Southern Cone', 31), ('Guiana', 30), ('Amazonia', 32), ('Panama', 31), ('Caribbean', 30), ('Mexico', 31), ('Rio Grande', 31), ('Mississippi', 31), ('Plains', 31), ('Eastern Seaboard', 29), ('Canada', 29),
     ('American West Coast', 33), ('Pacific', 33)])
#East Atlantis Node
expeditions_list.append(Expedition('east_atlantis_node', 'East Atlantis Node', 0, 'Jumping Node', [83]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('East Atlantis Node', 33), ('South Atlantis Node', 25), ('West Atlantis Node', 25), ('North Atlantis Node', 25), ('Iberia', 25), ('Strait of Gibraltar', 25), ('West Mediterranean', 25), ('France', 25), ('Channel', 25), ('North Sea', 25), ('Barbary Coast', 25), ('Tyrrenean Sea', 25), ('Rhineland', 33), ('Lower Nile', 25), ('Po Valley', 25), ('Adriatic Sea', 25), ('Levant', 25), ('Aegean Sea', 25),
     ('Danube', 25), ('Elbe', 33), ('Baltic Sea', 25), ('Vistula', 25), ('Crimea', 25), ('Western Siberia', 25), ('Dnieper', 25), ('Caspian Sea', 25), ('Zalesye', 25), ('Anatolia', 25), ('Sahara', 25), ('Senegambia', 27), ('Niger River', 27), ('Guinea Coast',
                                                                                                                                                                                                                                                    28), ('Lake Tchad', 28), ('Kongo', 28),
     ('South Africa', 30), ('Monomotapa', 30), ('Zanj', 30), ('Red Sea', 32), ('Upper Nile', 32), ('Arabia', 32), ('Iran', 32), ('Khorasan', 32), ('Mawarannahr', 32), ('Yettishar', 32),
     ('Punjab', 32), ('Gurjaratra', 32), ('Konkan', 32), ('Deccan Plateau', 32), ('Tamilakam', 32), ('Kalinga', 32), ('Delhi', 32), ('Bihar', 32), ('Bengal', 32), ('Himalayan Plateau', 32), ('Ayeyarwady', 32), ('Chao Phraya', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Moluccas', 33),
     ('Champa Sea', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangnan', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Eastern Siberia', 33), ('Nippon', 33),
     ('Far East', 33), ('Andes', 32), ('Southern Cone', 31), ('Guiana', 30), ('Amazonia', 32), ('Panama', 31), ('Caribbean', 30), ('Mexico', 31), ('Rio Grande', 31), ('Mississippi', 31), ('Plains', 31), ('Eastern Seaboard', 29), ('Canada', 29),
     ('American West Coast', 33), ('Pacific', 33)])
#West Atlantis Node
expeditions_list.append(Expedition('west_atlantis_node', 'West Atlantis Node', 0, 'Jumping Node', [81]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 33), ('East Zealandia Node', 33), ('South Zealandia Node', 33), ('West Atlantis Node', 33), ('East Atlantis Node', 25), ('South Atlantis Node', 25), ('North Atlantis Node', 25), ('Iberia', 25), ('Strait of Gibraltar', 25), ('West Mediterranean', 25), ('France', 25), ('Channel', 25), ('North Sea', 25), ('Barbary Coast', 25), ('Tyrrenean Sea', 25), ('Rhineland', 33), ('Lower Nile', 25), ('Po Valley', 25), ('Adriatic Sea', 25), ('Levant', 25), ('Aegean Sea', 25),
     ('Danube', 25), ('Elbe', 33), ('Baltic Sea', 25), ('Vistula', 25), ('Crimea', 25), ('Western Siberia', 25), ('Dnieper', 25), ('Caspian Sea', 25), ('Zalesye', 25), ('Anatolia', 25), ('Sahara', 25), ('Senegambia', 27), ('Niger River', 27), ('Guinea Coast',
                                                                                                                                                                                                                                                    28), ('Lake Tchad', 28), ('Kongo', 28),
     ('South Africa', 30), ('Monomotapa', 30), ('Zanj', 30), ('Red Sea', 32), ('Upper Nile', 32), ('Arabia', 32), ('Iran', 32), ('Khorasan', 32), ('Mawarannahr', 32), ('Yettishar', 32),
     ('Punjab', 32), ('Gurjaratra', 32), ('Konkan', 32), ('Deccan Plateau', 32), ('Tamilakam', 32), ('Kalinga', 32), ('Delhi', 32), ('Bihar', 32), ('Bengal', 32), ('Himalayan Plateau', 32), ('Ayeyarwady', 32), ('Chao Phraya', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Moluccas', 33),
     ('Champa Sea', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangnan', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Eastern Siberia', 33), ('Nippon', 33),
     ('Far East', 33), ('Andes', 32), ('Southern Cone', 31), ('Guiana', 30), ('Amazonia', 32), ('Panama', 31), ('Caribbean', 30), ('Mexico', 31), ('Rio Grande', 31), ('Mississippi', 31), ('Plains', 31), ('Eastern Seaboard', 29), ('Canada', 29),
     ('American West Coast', 33), ('Pacific', 33)])
#Zealandia
expeditions_list.append(Expedition('zealandia', 'Zealandia Node', 100, 'Jumping Node', [4]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 25), ('East Zealandia Node', 25), ('South Zealandia Node', 25), ('West Atlantis Node', 48), ('East Atlantis Node', 48), ('South Atlantis Node', 48), ('North Atlantis Node', 48), ('Iberia', 48), ('Strait of Gibraltar', 48), ('Sahara', 48), ('West Mediterranean', 48), ('France', 48), ('Channel', 48), ('North Sea', 48), ('Barbary Coast', 48), ('Tyrrenean Sea', 48), ('Rhineland', 48), ('Lower Nile', 48), ('Po Valley', 48), ('Adriatic Sea', 48), ('Levant', 48),
     ('Aegean Sea', 48), ('Danube', 48), ('Elbe', 48), ('Baltic Sea', 48),
     ('Vistula', 48), ('Crimea', 48), ('Western Siberia', 48), ('Dnieper', 48), ('Caspian Sea', 48), ('Zalesye', 48), ('Anatolia', 48), ('Senegambia', 48), ('Niger River', 48), ('Guinea Coast',
                                                                                                                                                                                  48), ('Lake Tchad', 48), ('Kongo', 48), ('South Africa', 48), ('Monomotapa', 48), ('Zanj', 48), ('Red Sea', 48),
     ('Upper Nile', 48), ('Arabia', 48), ('Iran', 48), ('Khorasan', 48), ('Mawarannahr', 48), ('Yettishar', 48),
     ('Punjab', 48), ('Gurjaratra', 48), ('Konkan', 48), ('Deccan Plateau', 48), ('Tamilakam', 48), ('Kalinga', 48), ('Delhi', 48), ('Bihar', 48), ('Bengal', 48), ('Himalayan Plateau', 48), ('Ayeyarwady', 48), ('Chao Phraya', 48), ('Malacca Strait', 48), ('Mekong', 48), ('Moluccas', 48),
     ('Champa Sea', 48), ('Australia', 25), ('Liangguang', 48), ('Szechwan', 48), ('Huazhong', 48), ('Jiangnan', 48), ('Huabei', 48), ('Xibei', 48), ('Eastern Siberia', 48), ('Zhongyuan', 48), ('Nippon', 48),
     ('Far East', 48), ('Andes', 48), ('Southern Cone', 48), ('Guiana', 48), ('Amazonia', 48), ('Panama', 48), ('Caribbean', 48), ('Mexico', 48), ('Rio Grande', 48), ('Mississippi', 48), ('Plains', 48), ('Eastern Seaboard', 48), ('Canada', 48),
     ('American West Coast', 48), ('Pacific', 33)])
#East Zealandia Node
expeditions_list.append(Expedition('eastzealandia', 'East Zealandia Node', 100, 'Jumping Node', [2]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 25), ('East Zealandia Node', 25), ('South Zealandia Node', 25), ('West Atlantis Node', 48), ('East Atlantis Node', 48), ('South Atlantis Node', 48), ('North Atlantis Node', 48), ('Iberia', 48), ('Strait of Gibraltar', 48), ('Sahara', 48), ('West Mediterranean', 48), ('France', 48), ('Channel', 48), ('North Sea', 48), ('Barbary Coast', 48), ('Tyrrenean Sea', 48), ('Rhineland', 48), ('Lower Nile', 48), ('Po Valley', 48), ('Adriatic Sea', 48), ('Levant', 48),
     ('Aegean Sea', 48), ('Danube', 48), ('Elbe', 48), ('Baltic Sea', 48),
     ('Vistula', 48), ('Crimea', 48), ('Western Siberia', 48), ('Dnieper', 48), ('Caspian Sea', 48), ('Zalesye', 48), ('Anatolia', 48), ('Senegambia', 48), ('Niger River', 48), ('Guinea Coast',
                                                                                                                                                                                  48), ('Lake Tchad', 48), ('Kongo', 48), ('South Africa', 48), ('Monomotapa', 48), ('Zanj', 48), ('Red Sea', 48),
     ('Upper Nile', 48), ('Arabia', 48), ('Iran', 48), ('Khorasan', 48), ('Mawarannahr', 48), ('Yettishar', 48),
     ('Punjab', 48), ('Gurjaratra', 48), ('Konkan', 48), ('Deccan Plateau', 48), ('Tamilakam', 48), ('Kalinga', 48), ('Delhi', 48), ('Bihar', 48), ('Bengal', 48), ('Himalayan Plateau', 48), ('Ayeyarwady', 48), ('Chao Phraya', 48), ('Malacca Strait', 48), ('Mekong', 48), ('Moluccas', 48),
     ('Champa Sea', 48), ('Australia', 25), ('Liangguang', 48), ('Szechwan', 48), ('Huazhong', 48), ('Jiangnan', 48), ('Huabei', 48), ('Xibei', 48), ('Eastern Siberia', 48), ('Zhongyuan', 48), ('Nippon', 48),
     ('Far East', 48), ('Andes', 48), ('Southern Cone', 48), ('Guiana', 48), ('Amazonia', 48), ('Panama', 48), ('Caribbean', 48), ('Mexico', 48), ('Rio Grande', 48), ('Mississippi', 48), ('Plains', 48), ('Eastern Seaboard', 48), ('Canada', 48),
     ('American West Coast', 48), ('Pacific', 33)])
#South Zealandia
expeditions_list.append(Expedition('southzealandia', 'South Zealandia Node', 100, 'Jumping Node', [3]))
expeditions_list[-1].set_node_tech_reqs(
    [('Zealandia Node', 25), ('East Zealandia Node', 25), ('South Zealandia Node', 25), ('West Atlantis Node', 48), ('East Atlantis Node', 48), ('South Atlantis Node', 48), ('North Atlantis Node', 48), ('Iberia', 48), ('Strait of Gibraltar', 48), ('Sahara', 48), ('West Mediterranean', 48), ('France', 48), ('Channel', 48), ('North Sea', 48), ('Barbary Coast', 48), ('Tyrrenean Sea', 48), ('Rhineland', 48), ('Lower Nile', 48), ('Po Valley', 48), ('Adriatic Sea', 48), ('Levant', 48),
     ('Aegean Sea', 48), ('Danube', 48), ('Elbe', 48), ('Baltic Sea', 48),
     ('Vistula', 48), ('Crimea', 48), ('Western Siberia', 48), ('Dnieper', 48), ('Caspian Sea', 48), ('Zalesye', 48), ('Anatolia', 48), ('Senegambia', 48), ('Niger River', 48), ('Guinea Coast',
                                                                                                                                                                                  48), ('Lake Tchad', 48), ('Kongo', 48), ('South Africa', 48), ('Monomotapa', 48), ('Zanj', 48), ('Red Sea', 48),
     ('Upper Nile', 48), ('Arabia', 48), ('Iran', 48), ('Khorasan', 48), ('Mawarannahr', 48), ('Yettishar', 48),
     ('Punjab', 48), ('Gurjaratra', 48), ('Konkan', 48), ('Deccan Plateau', 48), ('Tamilakam', 48), ('Kalinga', 48), ('Delhi', 48), ('Bihar', 48), ('Bengal', 48), ('Himalayan Plateau', 48), ('Ayeyarwady', 48), ('Chao Phraya', 48), ('Malacca Strait', 48), ('Mekong', 48), ('Moluccas', 48),
     ('Champa Sea', 48), ('Australia', 25), ('Liangguang', 48), ('Szechwan', 48), ('Huazhong', 48), ('Jiangnan', 48), ('Huabei', 48), ('Xibei', 48), ('Eastern Siberia', 48), ('Zhongyuan', 48), ('Nippon', 48),
     ('Far East', 48), ('Andes', 48), ('Southern Cone', 48), ('Guiana', 48), ('Amazonia', 48), ('Panama', 48), ('Caribbean', 48), ('Mexico', 48), ('Rio Grande', 48), ('Mississippi', 48), ('Plains', 48), ('Eastern Seaboard', 48), ('Canada', 48),
     ('American West Coast', 48), ('Pacific', 33)])
trade_nodes = {'Pacific': 1, 'East Zealandia Node': 2, 'South Zealandia Node': 3, 'Zealandia Node': 4, 'Australia': 5, 'Jiangnan': 6, 'Far East': 7, 'Eastern Siberia': 8, 'Huabei': 9, 'Nippon': 10,
               'American West Coast': 11, 'Mexico': 12, 'Huazhong': 13, 'Zhongyuan': 14, 'Szechwan': 15,
               'Xibei': 16, 'Amazonia': 17, 'Andes': 18, 'Southern Cone': 19, 'Liangguang': 20, 'Mekong': 21,
               'Champa Sea': 22, 'Ayeyarwady': 23, 'Himalayan Plateau': 24, 'Moluccas': 25, 'Malacca Strait': 26,
               'Chao Phraya': 27, 'Bihar': 28, 'Delhi': 29, 'Yettishar': 30, 'Punjab': 31, 'Mawarannahr': 32,
               'Khorasan': 33, 'Bengal': 34, 'Deccan Plateau': 35, 'Kalinga': 36, 'Tamilakam': 37, 'Konkan': 38, 'Gurjaratra': 39,
               'Upper Nile': 40, 'Red Sea': 41, 'Monomotapa': 42, 'Zanj': 43, 'South Africa': 44, 'Panama': 45,
               'Guiana': 46, 'Kongo': 47, 'Guinea Coast': 48, 'Lake Tchad': 49, 'Niger River': 50, 'Senegambia': 51,
               'Western Siberia': 52, 'Iran': 53, 'Arabia': 54, 'Caspian Sea': 55, 'Levant': 56, 'Barbary Coast': 57,
               'Lower Nile': 58, 'Dnieper': 59, 'Crimea': 60, 'Anatolia': 61, 'Zalesye': 62, 'Vistula': 63, 'Plains': 64,
               'Rio Grande': 65, 'Mississippi': 66, 'Canada': 67, 'Caribbean': 68, 'Eastern Seaboard': 69, 'South Atlantis Node': 70,
               'Strait of Gibraltar': 71, 'Danube': 72, 'Aegean Sea': 73, 'Iberia': 74, 'Po Valley': 75, 'Rhineland': 76,
               'West Mediterranean': 77, 'France': 78, 'Baltic Sea': 79, 'Adriatic Sea': 80, 'West Atlantis Node': 81, 'North Atlantis Node': 82, 'East Atlantis Node': 83, 'Channel': 84,
               'Elbe': 85, 'Tyrrenean Sea': 86, 'Sahara': 87, 'North Sea': 88}
#
can_trigger_MAM_event_15 = ['east_africa', 'arabia', 'indian_ocean', 'western_india', 'southern_india']

# Setup expeditions unlocks dict with keys for each tradenode holding an empty list
expedition_unlocks = {}
for node in trade_nodes:
    expedition_unlocks[node] = []

# Fill expeditions unlocked dict for when you unlock expeditions based on your capital location
for expedition in expeditions_list:
    assert len(set([i[0] for i in expedition.node_tech_reqs])) == len(expedition.node_tech_reqs)  # Assert all trade nodes are unique
    assert len(trade_nodes) == len(expedition.node_tech_reqs), f"{expedition.name} is missing some tech reqs"  # Assert all trade nodes were included
    for (trade_node, tech) in expedition.node_tech_reqs:
        assert trade_node in trade_nodes, f"{trade_node} spelled incorrectly"  # Assert all trade nodes are spelled correctly
        assert tech >= 13
        assert tech < 50
        expedition_unlocks[trade_node].append((expedition.localized_name, int(tech)))
for key in expedition_unlocks:  # Sort the list in each each tradenode by teach level
    expedition_unlocks[key].sort(key=lambda x: x[1])
assert len(trade_nodes) == len(expedition_unlocks), "Expedition unlocks should have 1 key per trade node"

num_total_expeditions = len(expeditions_list)

hash_line = "############################################################################################################\n"

neighboring_colonization_event = """\
# Gives rare colonization of neighboring provinces for countries without colonists
country_event = {
	id = MEC_Expeditions.002
	title = MEC_Expeditions.002.name
	desc = MEC_Expeditions.002.desc
	picture = TRADEGOODS_eventPicture
	
	trigger = {
		total_development = 30
		has_institution = Legalism
		NOT = { has_idea = exploration_ideas_2 } # Doesn't have colonist
		NOT = { has_idea = expansion_ideas_1 }
		OR = {
			AND = {
				is_colonial_nation = yes
				any_owned_province = {
					has_empty_adjacent_province = yes
				}
			}
			any_owned_province = {
				any_empty_neighbor_province = {
					NOT = {
						has_province_flag = ColonyBecomesOwner
						has_province_flag = NoRandomSpread
					}
				}
			}
		}
	}
	
	mean_time_to_happen = {
		years = 100 # 100 years
	}
	
	immediate = {
		hidden_effect = {
			random_owned_province = {
				limit = {
					has_empty_adjacent_province = yes
					OR = {
						ROOT = { is_colonial_nation = yes }
						any_empty_neighbor_province = {
							NOT = {
								has_province_flag = ColonyBecomesOwner
								has_province_flag = NoRandomSpread
							}
						}
					}
				}
				random_empty_neighbor_province = {
					limit = {
						OR = {
							ROOT = { is_colonial_nation = yes }
							NOT = {
								has_province_flag = ColonyBecomesOwner
								has_province_flag = NoRandomSpread
							}
						}
					}
					save_event_target_as = neighbor_province
					discover_country = ROOT
					if = {
						limit = {
							ROOT = { is_colonial_nation = yes }
						}
						change_religion = ROOT # Re-evaluate and probably change after religion rework is complete
						change_culture = ROOT
					}
					add_territorial_core = ROOT 
					cede_province = ROOT
				}
			}
		}
	}
	
	option = {
		name = MEC_Expeditions.002.opt
	}
}
"""

decisions_frame_top = """\
country_decisions = {

	# Decision to highlight all expedition provinces and toggle other expedition decisions
	MEC_Expeditions_Decision = {
		major = no
		potential = { # Always visible for players
			ai = no
		}
		provinces_to_highlight = { # Highlight provinces for all expeditions
			OR = {
"""

decisions_frame_bottom = """\
			}
		}
		allow = { # Always allow
			custom_trigger_tooltip = {
				tooltip = MEC_Expeditions_Decision_Highlight_All
				always = yes
			}
		}
		effect = { # Toggle showing decisions for all expeditions
			custom_tooltip = MEC_Expeditions_Decision_Effect
			if = {
				limit = {
					has_country_flag = MEC_Expeditions_Show_Decisions
				}
				clr_country_flag = MEC_Expeditions_Show_Decisions
			}
			else = {
				set_country_flag = MEC_Expeditions_Show_Decisions
			}
		}
		ai_will_do = { # AI doesn't need informational decisions
			factor = 0
		}
	}
"""

decision_toggle_expeditions = """\
	MEC_Expeditions_Decision_toggle_expeditions = {
		major = no
		potential = {
			has_country_flag = MEC_Expeditions_Show_Decisions
			OR = {
				has_idea = exploration_ideas_3
				has_country_modifier = can_colonize_country_modifier
			}
		}
		allow = {
			OR = {
				has_idea = exploration_ideas_3
				has_country_modifier = can_colonize_country_modifier
			}
		}
		effect = {
			if = {
				limit = {
					has_country_flag = MEC_Expeditions_paused
				}
				custom_tooltip = MEC_Expeditions_Decision_toggle_expeditions_restart
				clr_country_flag = MEC_Expeditions_paused
			}
			else = {
				custom_tooltip = MEC_Expeditions_Decision_toggle_expeditions_stop
				set_country_flag = MEC_Expeditions_paused
			}
		}
		ai_will_do = {
			factor = 0
		}
	}
"""

decision_toggle_always_fight = """\
	MEC_Expeditions_Decision_toggle_always_fight = {
		major = no
		potential = {
			has_country_flag = MEC_Expeditions_Show_Decisions
		}
		allow = {
		    ai = no
		}
		effect = {
			if = {
				limit = {
					has_country_flag = MEC_Expeditions_always_fight
				}
				custom_tooltip = MEC_Expeditions_Decision_toggle_always_fight_no
				clr_country_flag = MEC_Expeditions_always_fight
			}
			else = {
				custom_tooltip = MEC_Expeditions_Decision_toggle_always_fight_yes
				set_country_flag = MEC_Expeditions_always_fight
			}
		}
		ai_will_do = {
			factor = 0
		}
	}
"""

# Has variables: event_num
select_expedition_frame_top = """\
country_event = {{
	id = MEC_Expeditions.{event_num}
	title = MEC_Expeditions.{event_num}.name
	desc = MEC_Expeditions.{event_num}.desc
	picture = TRADEGOODS_eventPicture
	is_triggered_only = yes
	
"""

# Has variables: event_num, expedition_name
select_expedition_option_repeat_frame_top = """\
	option = {{
		name = MEC_Expeditions.{event_num}.{expedition_name}_repeat
		#log = "MEC_Expeditions:[GetYear]:[Root.GetName]:selected expedition to:{expedition_name}:repeated"
		trigger = {{
			MEC_Expeditions_available_{expedition_name}_trigger = yes
			has_country_flag = MEC_Expeditions_sent_{expedition_name}
		}}
		ai_chance = {{
			factor = {ai_base_chance}
"""
# Has variables: event_num, expedition_name
select_expedition_option_regular_frame_top = """\
	option = {{
		name = MEC_Expeditions.{event_num}.{expedition_name}
		#log = "MEC_Expeditions:[GetYear]:[Root.GetName]:selected expedition to:{expedition_name}"
		trigger = {{
			MEC_Expeditions_available_{expedition_name}_trigger = yes
			NOT = {{ has_country_flag = MEC_Expeditions_sent_{expedition_name} }}
		}}
		ai_chance = {{
			factor = {ai_base_chance}
"""
# Has variables: expedition_name
select_expedition_option_frame_bottom_jumping_node = """\
			modifier = {{ # Less likely to send expeditions to places you already have a province
				factor = 0.1
				num_of_provinces_owned_or_owned_by_non_sovereign_subjects_with = {{
					province_group = expedition_provs.{expedition_name}
					OR = {{
						has_province_modifier = trading_post_province
						has_province_flag = TN_Natural
						}}
					value = 1
				}}
			}}
"""
# Has variables: expedition_name
select_expedition_option_frame_bottom_colonial_node = """\
			modifier = {{ # More likely to send expeditions to places you already have a province
				factor = 5
				num_of_provinces_owned_or_owned_by_non_sovereign_subjects_with = {{
					value = 1
					province_group = expedition_provs.{expedition_name}
				}}
			}}
"""
# Has variables: expedition_name
select_expedition_option_frame_bottom_chinese_mainland = """\
			modifier = {{ # Stop AI from sending expeditions to mainlaind China if all of the coast is held by the Emperor. Meant to stop dragging relations to -200. harming trade and causing wars
				factor = 0
				expedition_provs.{expedition_name} = {{
					type = all 
					is_empty = no
					OR = {{
						owner = {{ is_emperor_of_china_meiou = yes }}
						owner = {{ overlord = {{ is_emperor_of_china_meiou = yes }} }}
						owner = {{ overlord = {{ overlord = {{ is_emperor_of_china_meiou = yes }} }} }}
					}}
				}}
			}}
			modifier = {{ # Less likely to send expeditions to places you already have a province
				factor = 0.1
				num_of_provinces_owned_or_owned_by_non_sovereign_subjects_with = {{
					province_group = expedition_provs.{expedition_name}
					OR = {{
						has_province_modifier = trading_post_province
						has_province_flag = TN_Natural
						}}
					value = 1
				}}
			}}
"""
# Has variables: expedition_name, event_num_arrival, event_num_total_failure, event_num_map_failure, event_num_trade_failure, expedition_duration, ai_base_chance, clr_all_sent_flags
select_expedition_option_frame_TN_link_check_top = """\
			modifier = { # Less likely to send expeditions to places you have no trade node connection with
				factor = 0 
				NOT = {is_year = 1650}
"""
select_expedition_option_frame_TN_link_check_inside = """\
				NOT = {{
					num_of_provinces_owned_or_owned_by_non_sovereign_subjects_with = {{
						value = 1
						province_group = tradenode_comb_{TN}
					}}
				}}
"""

select_expedition_option_claim_frame = """\
			modifier = {{ # Stop AI from sending expeditions to colonial regions already populated by another colonisers
				factor = 0.02
				calc_true_if = {{
					all_province = {{
						province_group=expedition_provs.{expedition_name}
						NOT = {{country_or_non_sovereign_subject_holds = ROOT}}
						owner = {{
							OR = {{
								is_colonial_nation = yes
								is_former_colonial_nation = yes
								has_idea = exploration_ideas_1
							}}
						}}
					}}
					amount = 2
				}}
				NOT={{
					num_of_provinces_owned_or_owned_by_non_sovereign_subjects_with = {{
						value = 2
						province_group = expedition_provs.{expedition_name}
					}}
				}}
			}}
"""

# Has variables: expedition_name, event_num_arrival, event_num_total_failure, event_num_map_failure, event_num_trade_failure, expedition_duration, ai_base_chance, clr_all_sent_flags
select_expedition_option_frame_bottom = """\
			modifier = {{ # Far less likely to send expeditions to places you failed a takeover attempt at
				factor = 0.1
				has_country_modifier = MEC_Modifier_Expedition_Failed_{expedition_name}
			}}
			modifier = {{ # Stop AI from loosing expeditions of provinces owned by comparable nations
				factor = 0.05
				expedition_provs.{expedition_name} = {{
					type = all 
					is_empty = no
					owner = {{ check_key = {{ lhs = tech_mil which = ROOT }} }}
				}}
			}}
		}}
		hidden_effect = {{
			add_country_modifier = {{
				name = MEC_Modifier_Expedition_{expedition_name}
				duration = {expedition_duration}
			}}
{clr_all_sent_flags}
			set_country_flag = MEC_Expeditions_sent_{expedition_name}
		}}
		if = {{
			limit = {{
				has_idea = colonialism_ideas_1
			}}
			random_list = {{
				80 = {{
					country_event = {{
						id = MEC_Expeditions.{event_num_arrival}
						days = {expedition_duration}
					}}
				}}
				10 = {{
					country_event = {{
						id = MEC_Expeditions.{event_num_trade_failure}
						days = {expedition_duration}
					}}
				}}
				5 = {{
					country_event = {{
						id = MEC_Expeditions.{event_num_map_failure}
						days = {expedition_duration}
					}}
				}}
				5 = {{
					country_event = {{
						id = MEC_Expeditions.{event_num_total_failure}
						days = {expedition_duration}
					}}
				}}
			}}
		}}
		else = {{
			random_list = {{
				40 = {{
					country_event = {{
						id = MEC_Expeditions.{event_num_arrival}
						days = {expedition_duration}
					}}
				}}
				15 = {{
					country_event = {{
						id = MEC_Expeditions.{event_num_trade_failure}
						days = {expedition_duration}
					}}
				}}
				15 = {{
					country_event = {{
						id = MEC_Expeditions.{event_num_map_failure}
						days = {expedition_duration}
					}}
				}}
				30 = {{
					country_event = {{
						id = MEC_Expeditions.{event_num_total_failure}
						days = {expedition_duration}
					}}
				}}
			}}
		}}
		expedition_provs.{expedition_name} = {{
			clr_province_flag = MEC_Expeditions_owned_by_sender_or_subjects
		}}
	}}
"""

# Has variables: event_num, event_num_landing, expedition_name, event_num_total_failure
expedition_arrival_frame = """\
country_event = {{
	id = MEC_Expeditions.{event_num}
	title = MEC_Expeditions.{event_num}.title
	desc = MEC_Expeditions.{event_num}.desc
	picture = TRADEGOODS_eventPicture
	is_triggered_only = yes
	hidden = yes
	
	option = {{
		name = MEC_Expeditions.arrival
		if = {{ # Have to check again in case of change while expedition was in progress
			limit = {{ 
				expedition_provs.{expedition_name} = {{
					MEC_Expeditions_eligible_province_trigger = yes
				}}
			}}
			set_key = {{ # Counter for loop
				lhs = Tmp_7
				value = 20
			}}
			set_key = {{ # High initial value to guarantee first province will be lower
				lhs = Tmp_8
				value = 1000
			}}
			while = {{
				limit = {{ # Exit loop when counter is below 1
					check_key = {{
						lhs = Tmp_7
						value = 1
					}}
				}}
			    if = {{ # if best value is negative (aka empty with feature)
			        limit = {{
			            NOT = {{
                            check_key = {{
                                lhs = Tmp_8
                                value = 0
                            }}
                        }}
			        }}
			        # Multiply best value by 5 and then add (it's negative) to loop counter
			        set_key = {{
			            lhs = Tmp_6
			            which = Tmp_8
			        }}
			        multiply_key = {{ 
			            lhs = Tmp_6
			            value = 5
			        }}
			        change_key = {{ 
			            lhs = Tmp_7
			            which = Tmp_6
			        }}
			    }}
			    else = {{
                    subtract_key = {{ # Reduce loop counter
                        lhs = Tmp_7
                        value = 1
                    }}
				}}
				random_province = {{  # In province group, not owned by sender or their subjects, and doesn't have truce with owner
					limit = {{ 
						province_group = expedition_provs.{expedition_name}
						MEC_Expeditions_eligible_province_trigger = yes
					}}
					MEC_Expeditions_defence_calc_effect = yes # Sets Tmp 0-4, 9
                    set_key = {{ # Copy current best number from country into this scope
                        lhs = Tmp_8
                        which = ROOT
                    }}
                    if = {{ # If the current province number is better target (lower number) then set it as the new target
                        limit = {{ # 8 < 2
                            NOT = {{ 
                                check_key = {{ 
                                    lhs = Tmp_9
                                    which = Tmp_8
                                }}
                            }}
                        }}
                        save_event_target_as = MEC_Expedition_Target_Province
                        set_key = {{ # Overwrite the number in this scope
                            lhs = Tmp_8
                            which = Tmp_9
                        }}
                        ROOT = {{ # Copy the overwrite to the country scope
                            set_key = {{
                                lhs = Tmp_8
                                which = PREV
                            }}
                        }}
					}}
				}}
			}} 
			event_target:MEC_Expedition_Target_Province = {{ # Call the landing event on the province that was found to be best
			    if = {{ # If player has selected to always fight, skip landing event
			        limit = {{
			            is_empty = no
			            owner = {{
			                has_country_flag = MEC_Expeditions_always_fight
			            }}
			        }}
			        export_to_key = {{ # Expedition sender mil tech
                        lhs = MEC_Expeditions_Comparison
                        value = mil_tech
                        who = FROM
                    }}
                    MEC_Expeditions_defence_calc_effect = yes # Sets Tmp 0-4, 9
                    subtract_key = {{
                        lhs = MEC_Expeditions_Comparison
                        which = Tmp_9
                    }}
		            {landing_success}  
			    }}
			    else = {{
                    province_event = {{ # Call landing event
                        id = MEC_Expeditions.{event_num_landing}
                        days = 0
                    }}
				}}
			}}
		}} 
		else = {{
			country_event = {{ # Call failure event
				id = MEC_Expeditions.{event_num_total_failure}
				days = 0
			}}
		}}
		expedition_provs.{expedition_name} = {{
			clr_province_flag = MEC_Expeditions_owned_by_sender_or_subjects
		}}
	}}
}}
"""

# Tmp key values set by this effect 0: Harbour level or current owner mil tech, 1: Feature level or doubled fort level, 2: colony, 3: manpower, 4: prov size, 9: total
province_defence_calculation = """\
MEC_Expeditions_defence_calc_effect = {
    if = { # If uncolonized province
        limit = {
            is_empty = yes
        }
        set_key = {
            lhs = Tmp_0
            value = 0
        }
        set_key = {
            lhs = Tmp_1
            value = 0
        }
        # Set Tmp_0 based on level of harbour
        if = {
            limit = {
                has_province_flag = TN_Harbour_Major
            }
            change_key = {
                lhs = Tmp_0
                value = -5
            }
        }
        if = {
            limit = {
                has_province_flag = TN_Harbour_Important
            }
            change_key = {
                lhs = Tmp_0
                value = -3
            }
        }
        if = {
            limit = {
                has_province_flag = TN_Harbour_Minor
            }
            change_key = {
                lhs = Tmp_0
                value = -1
            }
        }
        # Set Tmp_1 based on level of natural feature
        if = {
            limit = {
                has_province_flag = TN_Natural_Major
            }
            change_key = {
                lhs = Tmp_1
                value = -3
            }
        }
        if = {
            limit = {
                has_province_flag = TN_Natural_Important
            }
            change_key = {
                lhs = Tmp_1
                value = -2
            }
        }
        if = {
            limit = {
                has_province_flag = TN_Natural_Minor
            }
            change_key = {
                lhs = Tmp_1
                value = -1
            }
        }
        # Total values from harbours and natural features
        set_key = {
            lhs = Tmp_9
            which = Tmp_0
        }
        change_key = {
            lhs = Tmp_9
            which = Tmp_1
        }
    }
    else = {
        export_to_key = { # Current owner mil tech
            lhs = Tmp_0
            value = mil_tech
            who = owner
        }
        export_to_key = { # Get defender fort level
            lhs = Tmp_1
            value = trigger_value:fort_level
        }
        multiply_key = { # Double fort bonus
            lhs = Tmp_1
            value = 2
        }
        set_key = {
            lhs = Tmp_2
            value = 0
        }
        if = {
            limit = { # Bonus against incomplete colonies
                is_colony = yes
            }
            change_key = {
                lhs = Tmp_2
                value = -5
            }
        }
        # Sum manpower in province
        set_key = {
            lhs = Tmp_3
            value = 0
        }
        change_key = {
            lhs = Tmp_3
            which = Tax_MP
        }
        change_key = {
            lhs = Tmp_3
            which = Tax_NOMP
        }
        change_key = {
            lhs = Tmp_3
            which = Tax_BGMP
        }
        change_key = {
            lhs = Tmp_3
            which = Tax_TRMP
        }
        if = { # If manpower sum > 7 set 4 elif > 4 set 2 elif > 2 set 1
            limit = {
                check_key = {
                    lhs = Tmp_3
                    value = 7
                }
            }
            set_key = {
                lhs = Tmp_3
                value = 4
            }
        }
        else_if = {
            limit = {
                check_key = {
                    lhs = Tmp_3
                    value = 4
                }
            }
            set_key = {
                lhs = Tmp_3
                value = 2
            }
        }
        else_if = {
            limit = {
                check_key = {
                    lhs = Tmp_3
                    value = 2
                }
            }
            set_key = {
                lhs = Tmp_3
                value = 1
            }
        }
        else = {
            set_key = {
                lhs = Tmp_3
                value = 0
            }
        }
        set_key = {
            lhs = Tmp_4
            value = 0
        }
        if = { # If Land Province Size > 700 set 4 elif > 400 set 2 elif > 100 set 1
            limit = {
                check_key = {
                    lhs = Land_Size
                    value = 700
                }
            }
            set_key = {
                lhs = Tmp_4
                value = 4
            }
        }
        else_if = {
            limit = {
                check_key = {
                    lhs = Land_Size
                    value = 400
                }
            }
            set_key = {
                lhs = Tmp_4
                value = 2
            }
        }
        else_if = {
            limit = {
                check_key = {
                    lhs = Land_Size
                    value = 100
                }
            }
            set_key = {
                lhs = Tmp_4
                value = 1
            }
        }
        # Sum all values into Tmp_9 for total defence value
        set_key = {
            lhs = Tmp_9
            value = 0
        }
        change_key = {
            lhs = Tmp_9
            which = Tmp_0
        }
        change_key = {
            lhs = Tmp_9
            which = Tmp_1
        }
        change_key = {
            lhs = Tmp_9
            which = Tmp_2
        }
        change_key = {
            lhs = Tmp_9
            which = Tmp_3
        }
        change_key = {
            lhs = Tmp_9
            which = Tmp_4
        }
	}
}
"""

# Uses MEC_Expeditions_Comparison to decide whether to call success or failure event
# Has variables: event_num_success, event_num_total_failure, expedition_name, event_num_no_attack_failure
landing_success = """\
if = {{ # Use MEC_Expeditions_Comparison as success chance
    limit = {{
        check_key = {{
            lhs = MEC_Expeditions_Comparison
            value = 10
        }}
    }}
    FROM = {{ # 100%
        country_event = {{ # Success
            id = MEC_Expeditions.{event_num_success}
            days = 0
        }}
    }} 
}}
else_if = {{
    limit = {{
        check_key = {{
            lhs = MEC_Expeditions_Comparison
            value = 9
        }}
    }}
    random_list = {{
        90 = {{
            FROM = {{
                country_event = {{ # Success
                    id = MEC_Expeditions.{event_num_success}
                    days = 0
                }}
            }} 
        }}
        10 = {{
            FROM = {{
                country_event = {{ # Failure
                    id = MEC_Expeditions.{event_num_total_failure}
                    days = 0
                }}
                hidden_effect = {{
                    add_country_modifier = {{
                        name = MEC_Modifier_Expedition_Failed_{expedition_name}
                        duration = 7300 # 20 years
                        hidden = yes
                    }}
                }}
            }}
        }}
    }}
}}
else_if = {{
    limit = {{
        check_key = {{
            lhs = MEC_Expeditions_Comparison
            value = 8
        }}
    }}
    random_list = {{
        80 = {{
            FROM = {{
                country_event = {{ # Success
                    id = MEC_Expeditions.{event_num_success}
                    days = 0
                }}
            }} 
        }}
        20 = {{
            FROM = {{
                country_event = {{ # Failure
                    id = MEC_Expeditions.{event_num_total_failure}
                    days = 0
                }}
                hidden_effect = {{
                    add_country_modifier = {{
                        name = MEC_Modifier_Expedition_Failed_{expedition_name}
                        duration = 3650
                        hidden = yes
                    }}
                }}
            }}
        }}
    }}
}}
else_if = {{
    limit = {{
        check_key = {{
            lhs = MEC_Expeditions_Comparison
            value = 7
        }}
    }}
    random_list = {{
        70 = {{
            FROM = {{
                country_event = {{ # Success
                    id = MEC_Expeditions.{event_num_success}
                    days = 0
                }}
            }} 
        }}
        30 = {{
            FROM = {{
                country_event = {{ # Failure
                    id = MEC_Expeditions.{event_num_total_failure}
                    days = 0
                }}
                hidden_effect = {{
                    add_country_modifier = {{
                        name = MEC_Modifier_Expedition_Failed_{expedition_name}
                        duration = 3650
                        hidden = yes
                    }}
                }}
            }}
        }}
    }}
}}
else_if = {{
    limit = {{
        check_key = {{
            lhs = MEC_Expeditions_Comparison
            value = 6
        }}
    }}
    random_list = {{
        60 = {{
            FROM = {{
                country_event = {{ # Success
                    id = MEC_Expeditions.{event_num_success}
                    days = 0
                }}
            }} 
        }}
        40 = {{
            FROM = {{
                country_event = {{ # Failure
                    id = MEC_Expeditions.{event_num_total_failure}
                    days = 0
                }}
                hidden_effect = {{
                    add_country_modifier = {{
                        name = MEC_Modifier_Expedition_Failed_{expedition_name}
                        duration = 3650
                        hidden = yes
                    }}
                }}
            }}
        }}
    }}
}}
else_if = {{
    limit = {{
        check_key = {{
            lhs = MEC_Expeditions_Comparison
            value = 5
        }}
    }}
    random_list = {{
        50 = {{
            FROM = {{
                country_event = {{ # Success
                    id = MEC_Expeditions.{event_num_success}
                    days = 0
                }}
            }} 
        }}
        50 = {{
            FROM = {{
                country_event = {{ # Failure
                    id = MEC_Expeditions.{event_num_total_failure}
                    days = 0
                }}
                hidden_effect = {{
                    add_country_modifier = {{
                        name = MEC_Modifier_Expedition_Failed_{expedition_name}
                        duration = 3650
                        hidden = yes
                    }}
                }}
            }}
        }}
    }}
}}
else_if = {{
    limit = {{
        check_key = {{
            lhs = MEC_Expeditions_Comparison
            value = 4
        }}
    }}
    random_list = {{
        40 = {{
            FROM = {{
                country_event = {{ # Success
                    id = MEC_Expeditions.{event_num_success}
                    days = 0
                }}
            }} 
        }}
        60 = {{
            FROM = {{
                country_event = {{ # Failure
                    id = MEC_Expeditions.{event_num_total_failure}
                    days = 0
                }}
                hidden_effect = {{
                    add_country_modifier = {{
                        name = MEC_Modifier_Expedition_Failed_{expedition_name}
                        duration = 3650
                        hidden = yes
                    }}
                }}
            }}
        }}
    }}
}}
else_if = {{
    limit = {{
        check_key = {{
            lhs = MEC_Expeditions_Comparison
            value = 3
        }}
    }}
    random_list = {{
        30 = {{
            FROM = {{
                country_event = {{ # Success
                    id = MEC_Expeditions.{event_num_success}
                    days = 0
                }}
            }} 
        }}
        70 = {{
            FROM = {{
                country_event = {{ # Failure
                    id = MEC_Expeditions.{event_num_total_failure}
                    days = 0
                }}
                hidden_effect = {{
                    add_country_modifier = {{
                        name = MEC_Modifier_Expedition_Failed_{expedition_name}
                        duration = 3650
                        hidden = yes
                    }}
                }}
            }}
        }}
    }}
}}
else = {{
    FROM = {{
        country_event = {{ # Failure
            id = MEC_Expeditions.{event_num_no_attack_failure}
            days = 0
        }}
        hidden_effect = {{
            add_country_modifier = {{
                name = MEC_Modifier_Expedition_Failed_{expedition_name}
                duration = 3650
                hidden = yes
            }}
        }}
    }}
}}
"""

# Has variables: event_num, event_num_success, expedition_name
expedition_landing_frame = """\
province_event = {{ # Called on province being colonized
	id = MEC_Expeditions.{event_num}
	title = MEC_Expeditions.{event_num}.title
	desc = MEC_Expeditions.{event_num}.desc
	picture = TRADEGOODS_eventPicture
	is_triggered_only = yes
	
	immediate = {{
		hidden_effect = {{
			if = {{
				limit = {{
					is_empty = no
				}} # Note if make changes here also have to make changes to the similar section in the previous event
				export_to_key = {{ # Expedition sender mil tech
					lhs = MEC_Expeditions_Comparison
					value = mil_tech
					who = FROM
				}}
				MEC_Expeditions_defence_calc_effect = yes # Sets Tmp 0-4, 9
				subtract_key = {{
					lhs = MEC_Expeditions_Comparison
					which = Tmp_9
				}}
				# Cap value between 0-10 for display purpose
                if = {{ # if >= 10 set to 10
                    limit = {{
                        check_key = {{
                            lhs = MEC_Expeditions_Comparison
                            value = 10
                        }}
                    }}
                    set_key = {{
                        lhs = MEC_Expeditions_Comparison
                        value = 10
                    }}
                }}
                else_if = {{ # if < 0 set to 0
                    limit = {{
                        NOT = {{
                            check_key = {{
                                lhs = MEC_Expeditions_Comparison
                                value = 0
                            }}
                        }}
                    }}
                    set_key = {{
                        lhs = MEC_Expeditions_Comparison
                        value = 0
                    }}
                }}
			}}
		}}
	}}

	option = {{
		name = MEC_Expeditions.colony
		trigger = {{
			is_empty = yes
		}}
		FROM = {{
			country_event = {{ 
				id = MEC_Expeditions.{event_num_success}
				days = 0
			}}
		}} 
	}}
	option = {{
		name = MEC_Expeditions.reject_trade_fort
		trigger = {{
			is_empty = no
		}}
		ai_chance = {{ # Higher ai chance when more likely to fight off colonizers
			factor = 1
			modifier = {{
				factor = 2
				check_key = {{
					lhs = MEC_Expeditions_Comparison
					value = 6
				}}
			}}
			modifier = {{
				factor = 4
				check_key = {{
					lhs = MEC_Expeditions_Comparison
					value = 5
				}}
			}}
			modifier = {{
				factor = 6
				check_key = {{
					lhs = MEC_Expeditions_Comparison
					value = 4
				}}
			}}
			modifier = {{
				factor = 10
				check_key = {{
					lhs = MEC_Expeditions_Comparison
					value = 3
				}}
			}}
			modifier = {{
				factor = 16
				check_key = {{
					lhs = MEC_Expeditions_Comparison
					value = 2
				}}
			}}
			modifier = {{
				factor = 20
				check_key = {{
					lhs = MEC_Expeditions_Comparison
					value = 1
				}}
			}}
			modifier = {{
				factor = 100
				NOT = {{
					check_key = {{
						lhs = MEC_Expeditions_Comparison
						value = 1
					}}
				}}
			}}
		}}
		{landing_success}
	}}
	option = {{
		name = MEC_Expeditions.always_reject_trade_fort
		trigger = {{
			is_empty = no
		}}
		ai_chance = {{
		    factor = 0
		}}
		owner = {{
		    set_country_flag = MEC_Expeditions_always_fight
		}}
        {landing_success}
	}}
	option = {{
		name = MEC_Expeditions.accept_trade_fort
		trigger = {{
			is_empty = no
		}}
		ai_chance = {{ # Higher ai chance when less likely to fight off colonizers
			factor = 1
			modifier = {{
				factor = 9
				check_key = {{
					lhs = MEC_Expeditions_Comparison
					value = 9
				}}
			}}
			modifier = {{
				factor = 4
				check_key = {{
					lhs = MEC_Expeditions_Comparison
					value = 8
				}}
			}}
			modifier = {{
				factor = 2
				check_key = {{
					lhs = MEC_Expeditions_Comparison
					value = 7
				}}
			}}
		}}
		owner = {{
			add_treasury = 100
			add_truce_with = FROM
		}}
		FROM = {{
			country_event = {{ 
				id = MEC_Expeditions.{event_num_success}
				days = 0
			}}
		}}
	}}
}}
"""

# Has variables: event_num, expedition_name
expedition_success_frame = """\
country_event = {{
	id = MEC_Expeditions.{event_num}
	title = MEC_Expeditions.{event_num}.title
	desc = MEC_Expeditions.{event_num}.desc
	picture = TRADEGOODS_eventPicture
	is_triggered_only = yes
	
	immediate = {{
		hidden_effect = {{
			expedition_provs.{expedition_name}_vision = {{ # Note this can cause crashes if the prov group has invalid province numbers
				discover_country = ROOT
			}}
			event_target:MEC_Expedition_Target_Province = {{ # FROM is the province, ROOT is the expedition sender
				if = {{ # if it is a colony then they get a claim on the province they're losing
					limit = {{ # Non-colonies will have cores so don't need anything added
						is_colony = yes
					}}
					add_claim = owner
				}}
				add_territorial_core = ROOT 
				
				if = {{ # Change religion and culture if empty province not in trade company or in trade company with no population
					limit = {{
						is_empty = yes
						has_province_flag = ColonyBecomesOwner
					}} 
					change_religion = ROOT # Re-evaluate and probably change after religion rework is complete
					change_culture = ROOT
					ROOT = {{
						capital_scope = {{
							event_target:MEC_Expedition_Target_Province = {{ set_key = {{ lhs = Plague_Resistance1 which = PREV }} }}
							event_target:MEC_Expedition_Target_Province = {{ set_key = {{ lhs = Plague_Resistance2 which = PREV }} }}
							event_target:MEC_Expedition_Target_Province = {{ set_key = {{ lhs = Plague_Resistance4 which = PREV }} }}
						    
						    event_target:MEC_Expedition_Target_Province = {{ divide_key = {{ lhs = Plague_Resistance1 value = 3 }} }}
						    event_target:MEC_Expedition_Target_Province = {{ divide_key = {{ lhs = Plague_Resistance2 value = 3 }} }}
						    event_target:MEC_Expedition_Target_Province = {{ divide_key = {{ lhs = Plague_Resistance4 value = 3 }} }}
						}}
						
                        if = {{
                            limit = {{
                                any_owned_province = {{
                                    check_key = {{ lhs = Plague_SpawnChance4 value = 0.1 }}
                                }}
                            }}                        
                            event_target:MEC_Expedition_Target_Province = {{
                                if = {{
                                    limit = {{
                                        has_province_flag = possible_malaria
                                    }}
                                    America_Malaria_Calculator = yes
                                }}
                                every_neighbor_province = {{
                                    limit = {{
                                        has_province_flag = possible_malaria
                                    }}
                                    America_Malaria_Calculator = yes
                                }}
                            }}
                        }}
                    }}
                }}
                # System for 'waking' up smallpox in America. 
                random_list = {{ 
                    1 = {{
                        event_target:MEC_Expedition_Target_Province = {{
                            if = {{
                                limit = {{
                                    continent = north_america                                                                 
                                }}
                                if = {{
                                    limit = {{
                                        has_global_flag = not_namerica_smallpox
                                        superregion = east_america_superregion
                                    }}
                                    every_neighbor_province = {{
                                        limit = {{
                                            NOT = {{
                                                check_key = {{ lhs = Plague_SpawnChance2 value = 0.1 }}
                                                check_key = {{ lhs = Plague_Resistance2 value = 0.1 }}
                                            }}
                                            owner = {{
                                                OR = {{
                                                    technology_group = Andes
                                                    technology_group = mesoamerican
                                                    technology_group = south_american
                                                    technology_group = high_american
                                                }}
                                            }}
                                        }}
                                        #log = "MEC_Expeditions:[GetYear]:North America Smallpox Triggered from Expedition"
                                        province_event = {{ id = Plague_Spawner.221 days = 2555 random = 365 }}
                                    }}
                                }}
                                else_if = {{
                                    limit = {{
                                        has_global_flag = not_camerica_smallpox
                                        superregion = central_america_superregion
                                    }}
                                    every_neighbor_province = {{
                                        limit = {{
                                            NOT = {{
                                                check_key = {{ lhs = Plague_SpawnChance2 value = 0.1 }}
                                                check_key = {{ lhs = Plague_Resistance2 value = 0.1 }}
                                            }}
                                            owner = {{
                                                OR = {{
                                                    technology_group = Andes
                                                    technology_group = mesoamerican
                                                    technology_group = south_american
                                                    technology_group = high_american
                                                }}
                                            }}
                                        }}
                                        #log = "MEC_Expeditions:[GetYear]:Central America Smallpox Triggered from Expedition"
                                        province_event = {{ id = Plague_Spawner.222 days = 2555 random = 365 }}
                                    }}
                                }}
                            }}
                            else_if = {{
                                limit = {{
                                    continent = south_america
                                    has_global_flag = not_samerica_smallpox
                                }}
                                every_neighbor_province = {{
                                    limit = {{
                                        NOT = {{
                                            check_key = {{ lhs = Plague_SpawnChance2 value = 0.1 }}
                                            check_key = {{ lhs = Plague_Resistance2 value = 0.1 }}
                                        }}
                                        owner = {{
                                            OR = {{
                                                technology_group = Andes
                                                technology_group = mesoamerican
                                                technology_group = south_american
                                                technology_group = high_american
                                            }}
                                        }}
                                    }}
                                    #log = "MEC_Expeditions:[GetYear]:South America Smallpox Triggered from Expedition"
                                    province_event = {{ id = Plague_Spawner.2 days = 2555 random = 365 }}
                                }}
                            }}
                        }}
                    }}                      
                    2 = {{ 
                    }}
                }}                  
				if = {{ # If not empty add negative opinion for owner against expedition sender
					limit = {{
						is_empty = no
					}}
					#log = "MEC_Expeditions:[GetYear]:[Root.GetName]:received negative opinion modifier from::[MEC_Expedition_Target_Province.Owner.GetName]"
					owner = {{
						add_opinion = {{
							who = ROOT
							modifier = MEC_Expeditions_taken_province
						}}
					}}
				}}
				cede_province = ROOT
				if = {{ # if it is a colony then instantly finish it
					limit = {{
						is_colony = yes
					}}
					add_colonysize = 1000
				}}
			}}
		}}
	}}
	
"""
# Has variables: expedition_name
expedition_success_confirmation_MAM_event_15 = """\
	option = {{
		name = MEC_Expeditions.expedition_success
		#log = "MEC_Expeditions:[GetYear]:[Root.GetName]:successful expedition to:{expedition_name}:[MEC_Expedition_Target_Province.GetName]"
		add_prestige = 3
		hidden_effect = {{ MAM = {{ country_event = {{ id = flavor_mam.15 days = 1 }} }} }}
	}}
}}
"""

# Has variables: expedition_name
expedition_success_confirmation = """\
	option = {{
		name = MEC_Expeditions.expedition_success
		#log = "MEC_Expeditions:[GetYear]:[Root.GetName]:successful expedition to:{expedition_name}:[MEC_Expedition_Target_Province.GetName]"
		add_prestige = 3
	}}
}}
"""

# Has variables: event_num, expedition_name
expedition_total_failure_frame = """\
country_event = {{
	id = MEC_Expeditions.{event_num}
	title = MEC_Expeditions.{event_num}.title
	desc = MEC_Expeditions.{event_num}.desc
	picture = TRADEGOODS_eventPicture
	is_triggered_only = yes

	option = {{
		name = MEC_Expeditions.total_failure
		#log = "MEC_Expeditions:[GetYear]:[Root.GetName]:expedition totally failed:{expedition_name}"
		ai_chance = {{
			factor = 1
		}}
		add_prestige = -3
	}}
}}
"""

# Has variables: event_num, expedition_name
expedition_map_failure_frame = """\
country_event = {{
	id = MEC_Expeditions.{event_num}
	title = MEC_Expeditions.{event_num}.title
	desc = MEC_Expeditions.{event_num}.desc
	picture = TRADEGOODS_eventPicture
	is_triggered_only = yes

	option = {{
		name = MEC_Expeditions.map_failure
		#log = "MEC_Expeditions:[GetYear]:[Root.GetName]:expedition map failed:{expedition_name}"
		ai_chance = {{
			factor = 1
		}}
		add_prestige = -1
		hidden_effect = {{
			expedition_provs.{expedition_name}_vision = {{ # Note this can cause crashes if the prov group has invalid province numbers
				discover_country = ROOT
			}}
		}}
	}}
}}
"""

# Has variables: event_num, expedition_name
expedition_trade_failure_frame = """\
country_event = {{
	id = MEC_Expeditions.{event_num}
	title = MEC_Expeditions.{event_num}.title
	desc = MEC_Expeditions.{event_num}.desc
	picture = TRADEGOODS_eventPicture
	is_triggered_only = yes

	option = {{
		name = MEC_Expeditions.trade_failure
		#log = "MEC_Expeditions:[GetYear]:[Root.GetName]:expedition trade failed:{expedition_name}"
		ai_chance = {{
			factor = 1
		}}
		add_treasury = 20
		hidden_effect = {{
			expedition_provs.{expedition_name}_vision = {{ # Note this can cause crashes if the prov group has invalid province numbers
				discover_country = ROOT
			}}
		}}
	}}
}}
"""

# Has variables: event_num, expedition_name
expedition_no_attack_failure_frame = """\
country_event = {{
	id = MEC_Expeditions.{event_num}
	title = MEC_Expeditions.{event_num}.title
	desc = MEC_Expeditions.{event_num}.desc
	picture = TRADEGOODS_eventPicture
	is_triggered_only = yes

	option = {{
		name = MEC_Expeditions.no_attack_failure
		#log = "MEC_Expeditions:[GetYear]:[Root.GetName]:expedition no attack failed:{expedition_name}"
		ai_chance = {{
			factor = 1
		}}
		add_prestige = -1
		hidden_effect = {{
			expedition_provs.{expedition_name}_vision = {{ # Note this can cause crashes if the prov group has invalid province numbers
				discover_country = ROOT
			}}
		}}
	}}
}}
"""

# Has variables: event_num, expedition_name, more_info_event_num
expedition_decision_events_frame = """\
country_event = {{
	id = MEC_Expeditions.{event_num}
	title = MEC_Expeditions.{event_num}.title
	desc = MEC_Expeditions.{event_num}.desc
	picture = TRADEGOODS_eventPicture
	is_triggered_only = yes
	
	immediate = {{
		hidden_effect = {{
			expedition_provs.{expedition_name} = {{
				MEC_Expeditions_defence_calc_effect = yes
			}}
		}}
	}}
	
	option = {{
		name = MEC_Expeditions.more_info
		highlight = yes
		set_country_flag = MEC_Expeditions_decision_event_{event_num}
		country_event = {{
			id = MEC_Expeditions.{more_info_event_num}
		}}
		ai_chance = {{
			factor = 0
		}}
	}}
	option = {{
		name = MEC_Expeditions.report
		#log = "MEC_Expeditions:[GetYear]:[Root.GetName]:picked decision event for:{expedition_name}:If that is an AI it is a bug."		
		ai_chance = {{
			factor = 1
		}}
	}}
}}
"""

# Has variables: event_num
expedition_decision_info_event_frame_top = """\
country_event = {{
	id = MEC_Expeditions.{event_num}
	title = MEC_Expeditions.{event_num}.title
	desc = MEC_Expeditions.{event_num}.desc
	picture = TRADEGOODS_eventPicture
	is_triggered_only = yes

	option = {{
		name = MEC_Expeditions.back
		ai_chance = {{
			factor = 1
		}}
"""

expedition_decision_info_event_frame_bottom = """\
	}
	option = {
		name = MEC_Expeditions.close
		ai_chance = {
			factor = 1
		}
"""

python_generated_file_warning = """\
############################################################################################################
###############################       DO NOT MANUALLY EDIT THIS FILE    ####################################
############################################################################################################

############################################################################################################
##################  THIS FILE GENERATED BY PYTHON SCRIPT MEC_Expeditions_Writer.py  ########################
############################################################################################################
"""

# Get the province ids from the province groups
provincegroups = Path('map/provincegroup.txt').read_text(encoding='cp1252')
no_comments_pgs = re.sub('#.*', '', provincegroups)  # Get rid of comments
split_pgs = re.split(r'\n\s*expedition_provs.', no_comments_pgs)[1:]  # Split on the expedition province groups

for pg in split_pgs:
    name = re.findall(r'^(.*?)(?:[\s*=#])', pg)[0]  # Get the expedition name
    pg = re.sub(r'.*\{', '', re.sub(r'}.*', '', pg, flags=re.DOTALL), flags=re.DOTALL)  # Get string between brackets
    ids = re.findall(r'\d+', pg, flags=re.DOTALL)  # Pull out the province ids and put in list

    ids = [int(i) for i in ids]  # Convert strings to ints
    for id in ids:
        assert 0 <= id <= 10000, "Must be valid province id"
    assert len(set(ids)) == len(ids), f"Shouldn't have duplicate ids in {name}"

    for expedition in expeditions_list:
        if name == expedition.name:
            assert len(expedition.target_provinces) == 0, "Should only be added once"
            expedition.target_provinces += ids

# Check expeditions have target provinces
for expedition in expeditions_list:
    assert len(expedition.target_provinces) != 0, "Every expedition should have some target provinces"

# Overwrite the modifier file
with open(Path('common/event_modifiers/MEC-Expeditions_modifiers.txt'), 'w', encoding='cp1252') as modifiers:
    modifiers.write(python_generated_file_warning + '\n')
    for expedition in expeditions_list:
        modifiers.write(f'\nMEC_Modifier_Expedition_{expedition.name} = {{\n}}\n')
        modifiers.write(f'\nMEC_Modifier_Expedition_Failed_{expedition.name} = {{\n}}\n')

# Overwrite the decision file
with open(Path('decisions/MEC-Expeditions_decisions.txt'), 'w', encoding='cp1252') as decisions:
    decisions.write(python_generated_file_warning + '\n')

    # Main decision that highlights all provinces and toggles other decisions
    decisions.write(decisions_frame_top)
    for expedition in expeditions_list:
        decisions.write(f'\t\t\t\tprovince_group = expedition_provs.{expedition.name}\n')
    decisions.write(decisions_frame_bottom)

    decisions.write(decision_toggle_expeditions)
    decisions.write(decision_toggle_always_fight)

    # Decisions for each expedition to highlight their provinces
    for index, expedition in enumerate(expeditions_list):
        decisions.write(f"\tMEC_Expeditions_Decision_{expedition.name} = {{\n\t\tmajor = no\n\t\tpotential = {{\n\t\t\thas_country_flag = MEC_Expeditions_Show_Decisions\n\t\t}}\n")
        decisions.write(f"\t\tprovinces_to_highlight = {{\n\t\t\tprovince_group = expedition_provs.{expedition.name}\n\t\t}}\n")
        decisions.write("\t\tallow = {\n\t\t\talways = yes\n\t\t}\n")
        decisions.write(f"\t\teffect = {{\n\t\t\tcountry_event = {{\n\t\t\t\tid = MEC_Expeditions.{str(expedition_decision_events_start_number + index).zfill(3)}\n\t\t\t}}\n\t\t}}\n")
        decisions.write("\t\tai_will_do = {\n\t\t\tfactor = 0\n\t\t}\n\t}\n")

    decisions.write('}\n')

# Overwrite the scripted effects file
with open(Path('common/scripted_effects/MEC-Expeditions_effects.txt'), 'w', encoding='cp1252') as effects:
    effects.write(python_generated_file_warning + '\n')

    effects.write(province_defence_calculation + '\n')

# Overwrite the scripted triggers file
with open(Path('common/scripted_triggers/MEC-Expeditions_triggers.txt'), 'w', encoding='cp1252') as triggers:
    triggers.write(python_generated_file_warning + '\n')

    triggers.write("# Provinces are eligible expedition targets if neither you nor your subjects own them, and you don't have a truce or alliance with the owner.\n")
    triggers.write("MEC_Expeditions_eligible_province_trigger = {\n\tAND = {\n")
    triggers.write("\t\tNOT = {\n\t\t\tcountry_or_vassal_holds = ROOT\n\t\t}\n\t\tNOT = {\n\t\t\towner = {\n\t\t\t\tROOT = {\n\t\t\t\t\ttruce_with = PREV\n\t\t\t\t}\n\t\t\t}\n\t\t}\n\t\tNOT = {\n\t\t\towner = {\n\t\t\t\toverlord_of = ROOT\n\t\t\t}\n\t\t}\n")
    triggers.write("\t\tNOT = {\n\t\t\towner = {\n\t\t\t\tOR = {\n\t\t\t\t\talliance_with = ROOT\n\t\t\t\t\toverlord = {\n\t\t\t\t\t\talliance_with = ROOT\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n\t\t}\n\t}\n}\n\n")

    for expedition in expeditions_list:
        triggers.write(f"MEC_Expeditions_available_{expedition.name}_trigger = {{ # {expedition.localized_name} Expedition Availability Conditions\n\tAND = {{\n")
        triggers.write(f"\t\texpedition_provs.{expedition.name} = {{\n\t\t\tMEC_Expeditions_eligible_province_trigger = yes\n\t\t}}\n")
        triggers.write(f"\t\tOR = {{ # Dip tech requirements based on capital location in trade node\n")
        current_nodes = [False]
        for (node, tech) in sorted(expedition.node_tech_reqs, key=lambda x: x[1], reverse=True):
            if tech == current_nodes[0]:
                current_nodes.append(node)
            elif current_nodes[0] == False:  # First time through don't print
                current_nodes.clear()
                current_nodes.append(tech)
                current_nodes.append(node)
            else:
                triggers.write(f"\t\t\tAND = {{\n\t\t\t\tdip_tech = {current_nodes[0]}\n\t\t\t\tcapital_scope = {{\n\t\t\t\t\tOR = {{\n")
                for trade_node in current_nodes[1:]:
                    triggers.write(f"\t\t\t\t\t\tprovince_group = tradenode_{trade_nodes[trade_node]} # {trade_node}\n")
                current_nodes.clear()
                current_nodes.append(tech)
                current_nodes.append(node)
                triggers.write(f"\t\t\t\t\t}}\n\t\t\t\t}}\n\t\t\t}}\n")
        triggers.write(f"\t\t\tAND = {{\n\t\t\t\tdip_tech = {current_nodes[0]}\n\t\t\t\tcapital_scope = {{\n\t\t\t\t\tOR = {{\n")
        for trade_node in current_nodes[1:]:
            triggers.write(f"\t\t\t\t\t\tprovince_group = tradenode_{trade_nodes[trade_node]} # {trade_node}\n")
        triggers.write("\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n\t\t}\n\t}\n}\n\n")

# Overwrite the custom localization file
with open(Path('customizable_localization/MEC-Expeditions_customloc.txt'), 'w', encoding='cp1252') as custom_loc:
    custom_loc.write(python_generated_file_warning + '\n\n')
    custom_loc.write('defined_text = {\n\tname = MEC_Expeditions_Decision_tradenode\n\n')

    # Custom trigger for every trade node describing when you unlock expeditions
    for trade_node in expedition_unlocks:
        custom_loc.write(f'\ttext = {{\n\t\tlocalisation_key = MEC_Expeditions_Decision_{str(trade_node).replace(" ", "_")}\n')
        custom_loc.write("\t\ttrigger = {\n")
        custom_loc.write(f'\t\t\tcapital_scope = {{\n\t\t\t\tprovince_group = tradenode_{trade_nodes[trade_node]} # {trade_node}\n\t\t\t}}\n\t\t}}\n\t}}\n')
    custom_loc.write("}\n")

    # Custom loc for info events from decisions
    custom_loc.write('defined_text = {\n\tname = MEC_Expeditions_Decision_Event_Info\n\trandom = no\n\n')  # random = no makes it stop at first valid one
    custom_loc.write('\ttext = {\n\t\tlocalisation_key = MEC_Expeditions_Decision_Event_Info_undiscovered\n\t\ttrigger = {\n\t\t\tNOT = {\n\t\t\t\thas_discovered = FROM\n\t\t\t}\n\t\t}\n\t}\n')
    custom_loc.write('\ttext = {\n\t\tlocalisation_key = MEC_Expeditions_Decision_Event_Info_uncolonized\n\t\ttrigger = {\n\t\t\tis_empty = yes\n\t\t}\n\t}\n')
    custom_loc.write('\ttext = {\n\t\tlocalisation_key = MEC_Expeditions_Decision_Event_Info_colony\n\t\ttrigger = {\n\t\t\tis_colony = yes\n\t\t}\n\t}\n')
    custom_loc.write('\ttext = {\n\t\tlocalisation_key = MEC_Expeditions_Decision_Event_Info_owned\n\t\ttrigger = {\n\t\t\talways = yes\n\t\t}\n\t}\n')
    custom_loc.write("}\n")

# Overwrite the event file
with open(Path('events/MEC-Expeditions.txt'), 'w', encoding='cp1252') as events:
    with open(Path('localisation/MEC-Expeditions_l_english.yml'), 'w', encoding='utf-8-sig') as loc:
        loc.write("l_english:\n\n")
        loc.write(python_generated_file_warning + '\n')

        # Province groups localization
        loc.write(' # Province Group Localizations\n')
        for expedition in expeditions_list:
            loc.write(f' expedition_provs.{expedition.name}: "{expedition.localized_name} Expedition Target"\n')
            loc.write(f' expedition_provs.{expedition.name}_vision: "{expedition.localized_name} Expedition Gives Vision"\n')
        loc.write('\n')

        # Opinion modifier localization
        loc.write(' # Opinion Modifier\n')
        loc.write(' MEC_Expeditions_taken_province: "Took Province by Expedition"\n\n')

        # Write the decision localizations
        # Main decision localization
        loc.write(' # Expedition Decision\n')
        loc.write(' MEC_Expeditions_Decision_title: "Expeditions Unlock Tooltip & Decisions Toggle"\n')
        loc.write(' MEC_Expeditions_Decision_desc: "[Root.MEC_Expeditions_Decision_tradenode]"\n')
        loc.write(' MEC_Expeditions_Decision_Effect: "Toggle showing decisions for every expedition which allow province highlighting of only their provinces and tell when each trade node unlocks that expedition."\n')
        loc.write(' MEC_Expeditions_Decision_Highlight_All: "Click to highlight all provinces that are targeted by any expedition."\n')
        level_locations = {}  # Used for alphabetizing locations per level
        for trade_node in expedition_unlocks:
            loc.write(f' MEC_Expeditions_Decision_{str(trade_node).replace(" ", "_")}: "Based on our capital location in {trade_node} trade node, we will be able to send expeditions to these locations when we reach the corresponding §Ydiplomatic technology§! levels:')
            for (location, level) in expedition_unlocks[trade_node]:
                level_locations.setdefault(level, [])
                level_locations.get(level).append(location)
            for level in sorted(level_locations.keys()):
                loc.write(f'\\n§Y{level}§!: ' + ', '.join(sorted(level_locations.get(level))))
            level_locations.clear()
            loc.write('"\n')
        # Expedition specific decision localizations
        for expedition in expeditions_list:
            loc.write(f' MEC_Expeditions_Decision_{expedition.name}_title: "Expedition to {expedition.localized_name} Info"\n')
            loc.write(f' MEC_Expeditions_Decision_{expedition.name}_desc: "This expedition can be unlocked by countries with capitals in the following trade nodes at the corresponding §Ydiplomatic technology§! levels:')
            current_level = 0
            for (location, level) in expedition.node_tech_reqs:
                level_locations.setdefault(level, [])
                level_locations.get(level).append(location)
            for level in sorted(level_locations.keys()):
                loc.write(f'\\n§Y{level}§!: ' + ', '.join(sorted(level_locations.get(level))))
            level_locations.clear()
            loc.write('"\n')
        loc.write('\n')

        # Pause Expeditions Toggle Decision Localizations
        loc.write(' MEC_Expeditions_Decision_toggle_expeditions_title: "Expedition Events Toggle"\n')
        loc.write(' MEC_Expeditions_Decision_toggle_expeditions_desc: "Enable or disable your country getting the event for sending expeditions."\n')
        loc.write(' MEC_Expeditions_Decision_toggle_expeditions_stop: "Stop getting the event for sending expeditions."\n')
        loc.write(' MEC_Expeditions_Decision_toggle_expeditions_restart: "Restart getting the event for sending expeditions."\n')

        # Always Fight Expeditions Toggle Decision Localizations
        loc.write(' MEC_Expeditions_Decision_toggle_always_fight_title: "Expedition Landing Toggle"\n')
        loc.write(' MEC_Expeditions_Decision_toggle_always_fight_desc: "Set response to expeditions landing in your provinces."\n')
        loc.write(' MEC_Expeditions_Decision_toggle_always_fight_no: "Have a choice in responding to expeditions. Expedition landing event will show."\n')
        loc.write(' MEC_Expeditions_Decision_toggle_always_fight_yes: "Always fight off expeditions. Expedition landing event will be skipped."\n')

        # Write the modifier localizations
        loc.write("\n # Expedition Country Modifiers\n")
        for expedition in expeditions_list:
            loc.write(
                f' MEC_Modifier_Expedition_{expedition.name}: "Ongoing expedition to {expedition.localized_name}"\n')

        events.write("namespace = MEC_Expeditions\n\n")
        events.write(python_generated_file_warning + '\n\n')

        # Write the Neighboring Colonization event
        events.write(neighboring_colonization_event + '\n')
        loc.write('\n # Neighboring Colonization event\n')
        loc.write(' MEC_Expeditions.002.name: "Expansion into [neighbor_province.GetName]"\n')
        loc.write(' MEC_Expeditions.002.desc: "Some of our countrymen have long ventured into the uncolonized borderland of [neighbor_province.GetName]. Recently they made an organized effort to become permanently established there and properly integrate it into our country."\n')
        loc.write(' MEC_Expeditions.002.opt: "We shall now call it one of our provinces."\n')

        # Write the Select Expedition section header
        events.write(hash_line)
        events.write(
            "#####################################      Select Expedition       #########################################\n")
        events.write(hash_line + '\n')

        # Write the select expedition event
        # Loops through every expedition writing an option for it and localization
        events.write(select_expedition_frame_top.format(event_num=str(menu_event_number).zfill(3)))
        loc.write('\n # Select Expedition Menu Event')
        loc.write(
            '\n MEC_Expeditions.{event_num}.name: "Select Expedition"\n'.format(event_num=str(menu_event_number).zfill(3)))
        loc.write(
            f' MEC_Expeditions.{str(menu_event_number).zfill(3)}.desc: "We are able to send expeditions to establish our nation far from our capital. This enables us to expand our colonization and trade efforts. While we can make estimates for our chances of success to uncolonized territory, '
            f'if our expeditions arrive at already owned land their success will depend on if our military technology is superior enough against the locals as well as what defenses they have, how many trained men they have, and the size of the province. We would expect to hear back from our expedition within a year."\n')
        loc.write(f' MEC_Expeditions.{str(menu_event_number).zfill(3)}.dont: "Don\'t send an expedition."\n')

        events.write(
            "\ttrigger = {\n\t\tOR = {\n\t\t\thas_idea = exploration_ideas_3\n\t\t\thas_country_modifier = can_colonize_country_modifier\n\t\t}\n\t\tmax_sailors = 1500\n\t\tNOT = {\n\t\t\thas_country_flag = MEC_Expeditions_paused\n\t\t}\n\t\tnum_of_ports = 1\n\t\tOR = { # Has an expedition available\n")
        for expedition in expeditions_list:
            events.write(f"\t\t\tMEC_Expeditions_available_{expedition.name}_trigger = yes\n")
        events.write("\t\t}\n\t}\n\n")
        events.write('\timmediate = {\n\t\thidden_effect = {\n\t\t\tROOT = {\n\t\t\t\tsubtract_key = { lhs = tech_mil value = 5 }\n\t\t\t}\n\t\t}\n\t}\n\n')
        events.write(f"\toption = {{ # AI should take when no expedition available\n\t\tname = MEC_Expeditions.{str(menu_event_number).zfill(3)}.dont\n\t\tai_chance = {{\n\t\t\tfactor = 0.1\n\t\t}}\n\t}}\n\n")

        clr_all_sent_flags = ''
        for expedition in expeditions_list:
            clr_all_sent_flags += f"\t\t\tclr_country_flag = MEC_Expeditions_sent_{expedition.name}\n"

        for index, expedition in enumerate(expeditions_list):
            events.write(f"\t# Option for repeating sending Expedition to {expedition.localized_name}\n")
            events.write(select_expedition_option_repeat_frame_top.format(event_num=str(menu_event_number).zfill(3), expedition_name=expedition.name, ai_base_chance=expedition.ai_preference))

            if expedition.target_type == 'Jumping Node':
                events.write(select_expedition_option_frame_bottom_jumping_node.format(expedition_name=expedition.name))
            if expedition.target_type == 'Colonial Node':
                events.write(select_expedition_option_frame_bottom_colonial_node.format(expedition_name=expedition.name))
            if expedition.target_type == 'Chinese Mainland':
                events.write(select_expedition_option_frame_bottom_chinese_mainland.format(expedition_name=expedition.name))
            events.write(select_expedition_option_frame_TN_link_check_top)
            for i, node_number in enumerate(expedition.associated_TN):
                events.write(select_expedition_option_frame_TN_link_check_inside.format(TN=node_number))
            events.write("\t\t\t}\n")

            events.write(select_expedition_option_frame_bottom.format(expedition_name=expedition.name,
                                                                      event_num_arrival=str(expedition_arrival_start_number + index).zfill(3), event_num_total_failure=str(expedition_total_failure_start_number + index).zfill(3),
                                                                      event_num_map_failure=str(expedition_map_failure_start_number + index).zfill(3),
                                                                      event_num_trade_failure=str(expedition_trade_failure_start_number + index).zfill(3), expedition_duration=expedition_duration, clr_all_sent_flags=''))  # Repeat 0 AI chance
            loc.write(f' MEC_Expeditions.{str(menu_event_number).zfill(3)}.{expedition.name}_repeat: "Send another expedition to {expedition.localized_name}"\n')

        for index, expedition in enumerate(expeditions_list):
            events.write(f"\t# Option for sending Expedition to {expedition.localized_name}\n")
            events.write(select_expedition_option_regular_frame_top.format(event_num=str(menu_event_number).zfill(3), expedition_name=expedition.name, ai_base_chance=expedition.ai_preference))

            if expedition.target_type == 'Jumping Node':
                events.write(select_expedition_option_frame_bottom_jumping_node.format(expedition_name=expedition.name))
            if expedition.target_type == 'Colonial Node':
                events.write(select_expedition_option_frame_bottom_colonial_node.format(expedition_name=expedition.name))
            if expedition.target_type == 'Chinese Mainland':
                events.write(select_expedition_option_frame_bottom_chinese_mainland.format(expedition_name=expedition.name))
            events.write(select_expedition_option_frame_TN_link_check_top)
            for i, node_number in enumerate(expedition.associated_TN):
                events.write(select_expedition_option_frame_TN_link_check_inside.format(TN=node_number))
            events.write("\t\t\t}\n")
            if expedition.target_type == 'Colonial Node':
                events.write(select_expedition_option_claim_frame.format(expedition_name=expedition.name))
            events.write(select_expedition_option_frame_bottom.format(expedition_name=expedition.name,
                                                                      event_num_arrival=str(expedition_arrival_start_number + index).zfill(3), event_num_total_failure=str(expedition_total_failure_start_number + index).zfill(3),
                                                                      event_num_map_failure=str(expedition_map_failure_start_number + index).zfill(3),
                                                                      event_num_trade_failure=str(expedition_trade_failure_start_number + index).zfill(3), expedition_duration=expedition_duration, ai_base_chance=expedition.ai_preference, clr_all_sent_flags=clr_all_sent_flags))

            loc.write(f' MEC_Expeditions.{str(menu_event_number).zfill(3)}.{expedition.name}: "Send the expedition to {expedition.localized_name}"\n')

        events.write('\tafter = {\n\t\tif = {\n\t\t\tlimit = {\n\t\t\t\tNOT = {\n\t\t\t\t\thas_idea = colonialism_ideas_1\n\t\t\t\t}\n\t\t\t}\n\t\t\tset_country_flag = MEC_Expeditions_skip_year\n\t\t}\n')
        events.write('\t\tROOT = {change_key = { lhs = tech_mil value = 5 }}\n\t}\n}\n')
        # Write the Expedition Arrival section header
        events.write(hash_line)
        events.write(
            "##################################        Expedition Arrival       #########################################\n")
        events.write(hash_line + '\n')

        # Loop through every expedition and write arrival events for each
        loc.write("\n # Expedition Arrivals\n")
        loc.write(' MEC_Expeditions.arrival: "Okay."\n')

        for index, expedition in enumerate(expeditions_list):
            events.write(f"# Arrivals of Expedition to {expedition.localized_name}\n")
            events.write(expedition_arrival_frame.format(event_num=str(expedition_arrival_start_number + index).zfill(3), event_num_landing=str(expedition_landing_start_number + index).zfill(3), expedition_name=expedition.name, event_num_total_failure=str(expedition_total_failure_start_number +
                                                                                                                                                                                                                                                                index).zfill(3),
                                                         landing_success='\t\t\t\t\t'.join(landing_success.format(
                                                             event_num_success=str(
                                                                 expedition_success_start_number + index).zfill(3), event_num_total_failure=str(expedition_total_failure_start_number + index).zfill(3),
                                                             expedition_name=expedition.name, event_num_no_attack_failure=str(expedition_no_attack_failure_start_number + index).zfill(3)).splitlines(True))))
            loc.write(f' MEC_Expeditions.{str(expedition_arrival_start_number + index).zfill(3)}.title: "Expedition from [From.GetName]"\n')
            loc.write(f' MEC_Expeditions.{str(expedition_arrival_start_number + index).zfill(3)}.desc: "This event is supposed to be hidden. If you are seeing it please report this bug."\n')

        # Write the Expedition Landing section header
        events.write(hash_line)
        events.write(
            "##################################        Expedition Landings       #########################################\n")
        events.write(hash_line + '\n')

        # Loop through every expedition and write landing events for each
        loc.write("\n # Expedition Landings\n")
        loc.write(' MEC_Expeditions.accept_trade_fort: "We shall sell them the province."\n')
        loc.write(' MEC_Expeditions.reject_trade_fort: "Try to fight them off! We don\'t accept."\n')
        loc.write(' MEC_Expeditions.always_reject_trade_fort: "Try to fight them off, this time and always! (Can change via decision)"\n')
        loc.write(' MEC_Expeditions.colony: "You shouldn\'t be seeing this option. Please report the bug."\n')

        for index, expedition in enumerate(expeditions_list):
            events.write(f"# Landings of Expedition to {expedition.localized_name}\n")
            events.write(expedition_landing_frame.format(event_num=str(expedition_landing_start_number + index).zfill(3), event_num_success=str(expedition_success_start_number + index).zfill(3), expedition_name=expedition.name, landing_success='\t\t'.join(landing_success.format(
                event_num_success=str(
                    expedition_success_start_number + index).zfill(3), event_num_total_failure=str(expedition_total_failure_start_number + index).zfill(3),
                expedition_name=expedition.name, event_num_no_attack_failure=str(expedition_no_attack_failure_start_number + index).zfill(3)).splitlines(True))))
            loc.write(f' MEC_Expeditions.{str(expedition_landing_start_number + index).zfill(3)}.title: "Expedition from [From.GetName]"\n')
            loc.write(f' MEC_Expeditions.{str(expedition_landing_start_number + index).zfill(3)}.desc: "Foreigners have arrived wanting to setup a trading fort on our our province of [Root.GetName]. This would effectively give them control of the province. They offer to pay for the province, '
                      f'but our diplomatic advisor suspects that if we don\'t accept they will try to take it by force anyway. Our military advisor estimates that if it comes down to a fight they have a [GV_MEC_Expeditions_Comparison] out of 10 chance of losing the province."\n')

        # Write the Expedition Success section header
        events.write(hash_line)
        events.write(
            "##################################        Expedition Success       #########################################\n")
        events.write(hash_line + '\n')

        # Loop through every expedition writing expedition success events for each
        loc.write("\n # Successful Expeditions\n")
        loc.write(' MEC_Expeditions.expedition_success: "Great. We have a new province."\n')
        for index, expedition in enumerate(expeditions_list):
            events.write(f"# Success of Expedition to {expedition.localized_name}\n")
            events.write(expedition_success_frame.format(event_num=str(expedition_success_start_number + index).zfill(3),
                                                         expedition_name=expedition.name))
            if expedition.name in can_trigger_MAM_event_15:
                events.write(expedition_success_confirmation_MAM_event_15.format(expedition_name=expedition.name))
            else:
                events.write(expedition_success_confirmation.format(expedition_name=expedition.name))
            loc.write(
                f' MEC_Expeditions.{str(expedition_success_start_number + index).zfill(3)}.title: "Expedition to {expedition.localized_name} Successful"\n')
            loc.write(
                f' MEC_Expeditions.{str(expedition_success_start_number + index).zfill(3)}.desc: "We have heard back from the expedition to {expedition.localized_name}. They have established a settlement at [MEC_Expedition_Target_Province.GetName]. Since they also control the surrounding area they are '
                f'asking for recognition as a province."\n')

        # Write the Expedition Failure section header
        events.write(hash_line)
        events.write(
            "################################        Expedition Total Failure       #######################################\n")
        events.write(hash_line + '\n')

        # Loop through every expedition writing expedition failure events for each
        loc.write("\n # Expedition Total Failure\n")
        loc.write(' MEC_Expeditions.total_failure: "This reflects poorly on us."\n')
        for index, expedition in enumerate(expeditions_list):
            events.write(f"# Failure of Expedition to {expedition.localized_name}\n")
            events.write(expedition_total_failure_frame.format(event_num=str(expedition_total_failure_start_number + index).zfill(3),
                                                               expedition_name=expedition.name))
            loc.write(
                f' MEC_Expeditions.{str(expedition_total_failure_start_number + index).zfill(3)}.title: "Expedition to {expedition.localized_name} Lost at Sea"\n')
            loc.write(
                f' MEC_Expeditions.{str(expedition_total_failure_start_number + index).zfill(3)}.desc: "A prominent trader has been spreading word that we since we haven\'t heard back from our expedition to {expedition.localized_name} for so long that we can only assume it has failed '
                f'completely."\n')

        # Write the Expedition Failure section header
        events.write(hash_line)
        events.write(
            "################################        Expedition Map Failure       #######################################\n")
        events.write(hash_line + '\n')

        # Loop through every expedition writing expedition failure events for each
        loc.write("\n # Expedition Map Failure\n")
        loc.write(' MEC_Expeditions.map_failure: "That\'s better than nothing."\n')
        for index, expedition in enumerate(expeditions_list):
            events.write(f"# Failure of Expedition to {expedition.localized_name}\n")
            events.write(expedition_map_failure_frame.format(event_num=str(expedition_map_failure_start_number + index).zfill(3),
                                                             expedition_name=expedition.name))
            loc.write(
                f' MEC_Expeditions.{str(expedition_map_failure_start_number + index).zfill(3)}.title: "Expedition to {expedition.localized_name} Only Got Maps"\n')
            loc.write(
                f' MEC_Expeditions.{str(expedition_map_failure_start_number + index).zfill(3)}.desc: "A ship returned from our expedition to {expedition.localized_name}! However, they reported they were unsuccessful in establishing a settlement and barely made it back. Though they did bring '
                f'back maps of the region."\n')

        # Write the Expedition Failure section header
        events.write(hash_line)
        events.write(
            "################################        Expedition Trade Failure       #######################################\n")
        events.write(hash_line + '\n')

        # Loop through every expedition writing expedition failure events for each
        loc.write("\n # Expedition Trade Failure\n")
        loc.write(' MEC_Expeditions.trade_failure: "Well at least they got something."\n')
        for index, expedition in enumerate(expeditions_list):
            events.write(f"# Failure of Expedition to {expedition.localized_name}\n")
            events.write(expedition_trade_failure_frame.format(event_num=str(expedition_trade_failure_start_number + index).zfill(3),
                                                               expedition_name=expedition.name))
            loc.write(
                f' MEC_Expeditions.{str(expedition_trade_failure_start_number + index).zfill(3)}.title: "Expedition to {expedition.localized_name} Got Maps and Goods"\n')
            loc.write(
                f' MEC_Expeditions.{str(expedition_trade_failure_start_number + index).zfill(3)}.desc: "A ship returned from our expedition to {expedition.localized_name}! However, they reported they were unsuccessful in establishing a settlement. Though they did bring back a small amount from '
                f'trading and maps of the region."\n')

        # Write the Expedition Failure section header
        events.write(hash_line)
        events.write(
            "################################        Expedition No Attack Failure       #######################################\n")
        events.write(hash_line + '\n')

        # Loop through every expedition writing expedition failure events for each
        loc.write("\n # Expedition No Attack Failure\n")
        loc.write(' MEC_Expeditions.no_attack_failure: "That is unfortunate."\n')
        for index, expedition in enumerate(expeditions_list):
            events.write(f"# Failure of Expedition to {expedition.localized_name}\n")
            events.write(expedition_no_attack_failure_frame.format(event_num=str(expedition_no_attack_failure_start_number + index).zfill(3),
                                                                   expedition_name=expedition.name))
            loc.write(
                f' MEC_Expeditions.{str(expedition_no_attack_failure_start_number + index).zfill(3)}.title: "Expedition to {expedition.localized_name} Didn\'t Find Opportunity"\n')
            loc.write(
                f' MEC_Expeditions.{str(expedition_no_attack_failure_start_number + index).zfill(3)}.desc: "A ship returned from our expedition to {expedition.localized_name}! However, they reported they were unsuccessful in establishing a settlement. They found people settled in each '
                f'province they checked who seemed too strong for us to be able to grab our own foothold. Though they did bring back maps of the region."\n')

        # Write the Expedition Decision Events section header
        events.write(hash_line)
        events.write(
            "################################        Expedition Decision Events      #######################################\n")
        events.write(hash_line + '\n')

        # Localization for options for these events
        loc.write("\n # Expedition Decision Events\n")
        loc.write(' MEC_Expeditions.more_info: "What does this mean?"\n')
        loc.write(' MEC_Expeditions.report: "Thanks for the report."\n')
        loc.write(' MEC_Expeditions.back: "Back."\n')
        loc.write(' MEC_Expeditions.close: "Close."\n')

        # Loop through every expedition writing expedition decision events for each
        for index, expedition in enumerate(expeditions_list):
            events.write(f"# Info on Expeditions to {expedition.localized_name}\n")
            events.write(expedition_decision_events_frame.format(event_num=str(expedition_decision_events_start_number + index).zfill(3),
                                                                 expedition_name=expedition.name, more_info_event_num=str(expedition_decision_events_start_number + len(expeditions_list)).zfill(3)))
            loc.write(
                f' MEC_Expeditions.{str(expedition_decision_events_start_number + index).zfill(3)}.title: "Info for Expeditions to {expedition.localized_name}"\n')
            loc.write(
                f' MEC_Expeditions.{str(expedition_decision_events_start_number + index).zfill(3)}.desc: "')
            for id in expedition.target_provinces:
                loc.write(f'[{id}.MEC_Expeditions_Decision_Event_Info]\\n')
            loc.write('"\n')
        events.write(expedition_decision_info_event_frame_top.format(event_num=str(expedition_decision_events_start_number + len(expeditions_list)).zfill(3)))
        events.write('\t\ttrigger_switch = {\n\t\t\ton_trigger = has_country_flag\n')
        for index, expedition in enumerate(expeditions_list):
            events.write(f'\t\t\tMEC_Expeditions_decision_event_{str(expedition_decision_events_start_number + index).zfill(3)} = {{\n\t\t\t\tclr_country_flag = MEC_Expeditions_decision_event_'
                         f'{str(expedition_decision_events_start_number + index).zfill(3)}\n\t\t\t\tcountry_event = {{\n\t\t\t\t\tid = MEC_Expeditions.{str(expedition_decision_events_start_number + index).zfill(3)}\n\t\t\t\t}}\n\t\t\t}}\n')
        events.write('\t\t}\n')
        events.write(expedition_decision_info_event_frame_bottom)

        for index, expedition in enumerate(expeditions_list):
            events.write(f'\t\tclr_country_flag = MEC_Expeditions_decision_event_{str(expedition_decision_events_start_number + index).zfill(3)}\n')
        events.write('\t}\n}\n\n')
        loc.write(' MEC_Expeditions_Decision_Event_Info_undiscovered: "Undiscovered province"\n')
        loc.write(' MEC_Expeditions_Decision_Event_Info_uncolonized: "[This.GetName] (Uncolonized) Harbour [GV_Tmp_0] Natural Feature [GV_Tmp_1] Total [GV_Tmp_9]"\n')
        loc.write(' MEC_Expeditions_Decision_Event_Info_colony: "[This.GetName] ([This.Owner.GetName]) Mil Tech [GV_Tmp_0] Def [GV_Tmp_1] Colony [GV_Tmp_2] MP [GV_Tmp_3] Size [GV_Tmp_4] Total [GV_Tmp_9]"\n')
        loc.write(' MEC_Expeditions_Decision_Event_Info_owned: "[This.GetName] ([This.Owner.GetName]) Mil Tech [GV_Tmp_0] Def [GV_Tmp_1] MP [GV_Tmp_3] Size [GV_Tmp_4] Total [GV_Tmp_9]"\n')

        loc.write(f' MEC_Expeditions.{str(expedition_decision_events_start_number + len(expeditions_list)).zfill(3)}.title: "Expeditions Detailed Info"\n')
        loc.write(f' MEC_Expeditions.{str(expedition_decision_events_start_number + len(expeditions_list)).zfill(3)}.desc:')
        loc.write(""""\
When expeditions are sent they have a 40% chance of successful landing at their target area, which can be increased to 80% with the first colonialism idea. Otherwise they \
get one of the failure options which brings back nothing, maps, or maps and some ducats.\\nOnce it is determined an expedition successfully landed there is a calculation for which province it landed at, which randomly loops through a bunch of provinces in the target area to evaluate their \
score and picks the one with the lowest score.\\nUncolonized provinces will be picked before owned provinces, with their scores determined by their rank of habour and natural feature. If all the provinces are owned then the owner of the province with the lowest score will get an event with the \
option \
to \
sell the province or defend it. If they choose to defend it then the chance of the expedition sender taking the province is their military tech level minus the province's defensive score divided by 10.\\nThe province's defensive score is calculated by mil tech, plus defensive bonus which \
consists of 2 + 2 * fort level, \
minus 5 if colony, plus bonus depending on sum of taxed manpower in province by the state and all of the elites, plus bonus based on size of the province.\\nIf the expedition sender has mil tech 20 and the province defensive score is 15, and the owner decides to defend, \
the sender would have 50% chance of taking \
the province after landing. It is not directly 50% after landing because at worse odds owners are more likely to choose to sell the province than try to defend. Thus a 5 point advantage actually gives the sender approximately 64% chance of gaining a province after successfully landing."\n""")

# file = open('wiki.txt', 'w+')
#
# for expedition in expeditions_list:
#     tabletext = """
# ==={}===
# {| class="mildtable sortable" style="width:100%"
# ! style="width:150px" class="unsortable" | Trade Node
# ! style="width:50px" | Tech Requirement
# """.format(expedition.expedition_name)
#     for (trade_node,tech) in expedition.node_tech_reqs:
#         tabletext += """
# |-
#
# |
# {}
# |
# {}
# |
# """.format(trade_node, tech)
#     tabletext += "}\n"
#     file.write(tabletext)
# file.close()
