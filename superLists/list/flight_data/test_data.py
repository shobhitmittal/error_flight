import os
import json
from datetime import datetime
import calendar
import pdb
import time
import random

flight_info = {}

master_flight_info = {'src':{}, 'dest':{}}

master_flight_info_lvl_1 = {}


carrier_list = ['Air_Heritage']

#carrier_list = ['Air_Heritage']

city_to_flight_code_mapping_dict_temp = {"jamnagar": "JGA",
									"aurangabad": "IXU",
									"pakyong": "PYG",
									"jharsuguda": "JRG",
									"kandla": "IXY",
									"rajkot": "RAJ",
									"kanpur": "KNU",
									"dharamshala": "DHM",
									"durgapur": "RDP",
									"pithoragarh": "PGH",
									"kishangarh":"KQH",
									"adampur": "AIP",
									"dimapur": "DMU",
									"hindon": "HDX",
									"jaisalmer": "JSA",
									"porbander": "PBD",
									"khajuraho": "HJR",
									"leh": "IXL",
									"thoise": "VI57",
									"gwalior": "GWL",
									"nanded": "NDC",
									"pondicherry": "PNY",
									"Ahmedabad":"AMD",
									"Agartala":"IXA",
									"Aizawal":"AJL",
									"Allahabad":"IXD",
									"Amritsar":"LUH",
									"Bagdogra":"IXB",
									"Bangalore":"BLR",
									"Belgaum":"IXG",
									"Bhopal":"BHO",
									"Bhubaneshwar":"BBI",
									"Calicut":"CCJ",
									"Chandigarh":"IXC",
									"Chennai":"MAA",
									"Coimbatore":"CJB",
									"Dehradun":"DED",
									"Delhi":"DEL",
									"Dibrugarh":"DIB",
									"Dimapur":"DMU",
									"Goa":"GOI",
									"Gaya":"GAY",
									"Gorakhpur":"GOP",
									"Guwahati":"GAU",
									"Hubli":"HBX",
									"Hyderabad":"HYD",
									"Imphal":"IMF",
									"Indore":"IDR",
									"Jabalpur":"JLR",
									"Jaipur":"JAI",
									"Jammu":"IXJ",
									"Kannur":"CNN",
									"Jodhpur":"JDH",
									"Jorhat":"JRH",
									"Kochi":"COK",
									"Kolhapur":"KLH",
									"Kolkata":"CCU",
									"Lucknow":"LKO",
									"Madurai":"IXM",
									"Mumbai":"BOM",
									"Mangalore":"IXE",
									"Mysore":"MYQ",
									"Nagpur":"NAG",
									"Patna":"PAT",
									"Port_Blair":"IXZ",
									"Pune":"PNQ",
									"Raipur":"RPR",
									"Rajamundry":"RJA",
									"Ranchi":"IXR",
									"Shillong":"SHL",
									"Shirdi":"SAG",
									"Silchar":"IXS",
									"Srinagar":"SXR",
									"Surat":"STV",
									"Tirupathi":"TIR",
									"Trichy":"TRZ",
									"Trivandrum":"TRV",
									"Tuticorin":"TCR",
									"Udaipur":"UDR",
									"Vadodara":"BDQ",
									"Varanasi":"VNS",
									"Vijaywada":"VGA",
									"Vizag":"VTZ"}

city_to_flight_code_mapping_dict_final = {}

for city_name in city_to_flight_code_mapping_dict_temp.keys():

	city_name_lower = city_name.lower()
	city_to_flight_code_mapping_dict_final[city_name_lower] = city_to_flight_code_mapping_dict_temp[city_name].upper()
									
city_unique_dict = {}

#ghost flights are flights either taking off and not landing.
normal_flights_code = {}
ghost_flights_code = {}

def read_file(file_path):
	with open(file_path, 'r') as ap:
		return ap.readlines()

def Search_route_data():
	for carrier_name in carrier_list:

			# if count >0:
			#    break
			# count+=1

			# temp_ds

		city_list_temp = []

		carrier_name_lower = str(carrier_name).lower()

		if carrier_name_lower not in flight_info:
			flight_info[carrier_name_lower] = {}
		else:
			raise Exception('%s seen again.' % (carrier_name_lower))
		prefix_path='/home/aditya/Desktop/Test/Django/superLists/skillenza_hackthon/superLists/list/'
		flight_data_file = prefix_path+'flight_data/' + carrier_name + '/flight_data'
		city_data_file = prefix_path+'flight_data/' + carrier_name + '/city_list'

		flight_data = read_file(file_path=flight_data_file)
		city_data = read_file(file_path=city_data_file)

			# Find unique city list.
		for city_name in city_data:
			city_name = '_'.join(city_name.strip().lower().split(' '))

			city_list_temp.append(city_name)

			if len(city_list_temp) != len(list(set(city_list_temp))):
				raise Exception('Duplicate cities found for %s.' % (carrier_name_lower))
			else:
				pass
			if city_name not in city_unique_dict:
				city_unique_dict[city_name] = ""
			else:
				pass

			# Main_data_parsing.

		city_done_count = -1
		for flight_data_iter in flight_data:
			flight_data_iter_list = str(flight_data_iter).strip().split()
			if bool(flight_data_iter_list) is True:
				# 8 I5 1459 I5 A 320 Daily BLR 21:00 27-Oct-19 28-Mar-20
				# ['6', 'I5', '1453', 'I5', 'A', '320', '134567', 'BLR', '11:05', '27-Oct-19', '28-Mar-20']
				# print flight_data_iter_list

				serial_no = int(flight_data_iter_list[0])
				flight_no = '%s %s' % (flight_data_iter_list[1], flight_data_iter_list[2])
				operator_code = flight_data_iter_list[3]
				aircraft_type = '%s%s' % (flight_data_iter_list[4], flight_data_iter_list[5])
				frequency = flight_data_iter_list[6]
				if str(frequency).lower() == 'daily':
					frequency = '1234567'
				src_or_dest_city = flight_data_iter_list[7].lower()
				if len(src_or_dest_city) > 3:
					src_or_dest_city = city_to_flight_code_mapping_dict_final[src_or_dest_city]
				else:
					src_or_dest_city = src_or_dest_city.upper()
				src_or_dest_time = human_to_epoch_time(time_human=flight_data_iter_list[8],
													   is_calendar_format=False)
				src_or_dest_time_human = flight_data_iter_list[8]
				effective_start_date = human_to_epoch_time(time_human=flight_data_iter_list[9])
				effective_end_date = human_to_epoch_time(time_human=flight_data_iter_list[10])
				if effective_start_date == effective_end_date:
					continue
				else:
					pass

				if flight_no not in normal_flights_code:
					normal_flights_code[flight_no] = 1
				else:
					normal_flights_code[flight_no] += 1

				for flight_no_normal in normal_flights_code.keys():
					# print flight_no
					if normal_flights_code[flight_no_normal] % 2 != 0:
						ghost_flights_code[flight_no_normal] = normal_flights_code[flight_no_normal]
					else:
						pass
				# print flight_no_normal

				if serial_no == 1:
					city_done_count += 1
					current_city_name = city_to_flight_code_mapping_dict_final[city_list_temp[city_done_count]]

				else:
					pass

				if current_city_name not in flight_info[carrier_name_lower]:
					flight_info[carrier_name_lower][current_city_name] = []
				temp_dict = {}
				temp_dict['serial_no'] = serial_no
				temp_dict['flight_no'] = flight_no
				temp_dict['operator_code'] = operator_code
				temp_dict['aircraft_type'] = aircraft_type
				temp_dict['frequency'] = frequency
				temp_dict['src_or_dest_city'] = src_or_dest_city
				temp_dict['src_or_dest_time'] = src_or_dest_time
				temp_dict['src_or_dest_time_human'] = src_or_dest_time_human
				temp_dict['effective_start_date'] = effective_start_date
				temp_dict['effective_end_date'] = effective_end_date
				##if multiple flights from same src to same dest, then need to handle.
				to_be_added = True
				for crr_city_data in flight_info[carrier_name_lower][current_city_name]:
					if crr_city_data['flight_no'] == flight_no:
						to_be_added = False
					else:
						pass
				if to_be_added is True:
					flight_info[carrier_name_lower][current_city_name].append(temp_dict)
				else:
					pass
			else:
				# Blank line on flight data.
				pass

	# master_flight_info = {'src':{}, 'dest':{}}
	for carrier_name_iter in flight_info.keys():
		city_data_dict = flight_info[carrier_name_iter]
		for city_name_iter in city_data_dict.keys():

				# VTZ
			for city_data_iter in city_data_dict[city_name_iter]:

				# {'src_or_dest_city': 'CCU', 'effective_end_date': 1585353600, 'flight_no': 'I5 519', 'serial_no': 1, 'effective_start_date': 1572134400, 'frequency': '1234567', 'aircraft_type': 'A320', 'operator_code': 'I5', 'src_or_dest_time': -2208964800}
				src_or_dest_city = city_data_iter['src_or_dest_city']
				src_or_dest_time = city_data_iter['src_or_dest_time']
				flight_no = city_data_iter['flight_no']

				# Finding whether the flight seen above is landing at src or taking off from dest.
				for city_name_iter_2 in city_data_dict.keys():
					# print city_name_iter_2

					if city_name_iter_2 == src_or_dest_city:
						for city_data_iter_2 in city_data_dict[city_name_iter_2]:

							src_or_dest_city_2 = city_data_iter_2['src_or_dest_city']
							src_or_dest_time_2 = city_data_iter_2['src_or_dest_time']
							flight_no_2 = city_data_iter_2['flight_no']

							if city_name_iter == src_or_dest_city_2 and flight_no == flight_no_2:
								# print city_name_iter, src_or_dest_city_2

								time_a = src_or_dest_time
								time_b = src_or_dest_time_2

								final_time_1 = time_a - time_b

								final_time_2 = time_b - time_a

								if final_time_1 < 0:
										# pdb.set_trace()
									final_time = final_time_1
									src_city_final = src_or_dest_city_2
									dest_city_final = src_or_dest_city
									src_data_iter_final = city_data_iter
									dest_data_iter_final = city_data_iter_2
								elif final_time_1 > 0:
									# pdb.set_trace()
									final_time = final_time_2
									src_city_final = src_or_dest_city
									dest_city_final = src_or_dest_city_2
									src_data_iter_final = city_data_iter_2
									dest_data_iter_final = city_data_iter
								else:
									continue
								src_data_iter_final['flight_duration'] = final_time
								dest_data_iter_final['flight_duration'] = final_time
								if src_city_final not in master_flight_info['src']:
									master_flight_info['src'][src_city_final] = []
								else:
									pass
								to_be_added = True
								for i in master_flight_info['src'][src_city_final]:
									if src_data_iter_final['flight_no'] == i['flight_no']:
										to_be_added = False
									else:
										pass
								if to_be_added is True:
									master_flight_info['src'][src_city_final].append(src_data_iter_final)
								else:
									pass
								if dest_city_final not in master_flight_info['dest']:
									master_flight_info['dest'][dest_city_final] = []
								else:
									pass
								to_be_added = True
								for j in master_flight_info['dest'][dest_city_final]:
									if dest_data_iter_final['flight_no'] == j['flight_no']:
										to_be_added = False
									else:
										pass
								if to_be_added is True:
									master_flight_info['dest'][dest_city_final].append(dest_data_iter_final)
								else:
									pass
							else:
								pass

					else:
						pass

	# Level 1 code for 1 stop flights.
	# It consists of 2 paths: 1st is src to intm location, 2nd is intm location to dest.
	# master_flight_info_lvl_1 = {}

	all_dest_list = master_flight_info['dest'].keys()

	for all_dest_city_key in all_dest_list:
		for src_city_key in master_flight_info['src'].keys():
			# print '366', src_city_key

			for dest_city_key in master_flight_info['dest'].keys():

				if src_city_key != dest_city_key and all_dest_city_key != dest_city_key and src_city_key != all_dest_city_key:
					# print dest_city_key

					is_master_lvl1_key_created = False
					if dest_city_key in master_flight_info['src']:
						for lvl_2_src_city_data in master_flight_info['src'][dest_city_key]:

							if lvl_2_src_city_data['src_or_dest_city'] == all_dest_city_key:
								# print lvl_2_src_city_data
								master_flight_info_lvl_1_key = '%s_%s_%s_%s_%s' % (
								src_city_key, all_dest_city_key, dest_city_key, time.time(), random.randint(0, 10000))
								# print master_flight_info_lvl_1_key
								# if master_flight_info_lvl_1_key.find('HDX_DED_PGH') >=0:
								#	pdb.set_trace()
								if master_flight_info_lvl_1_key not in master_flight_info_lvl_1:
									master_flight_info_lvl_1[master_flight_info_lvl_1_key] = {}
									master_flight_info_lvl_1[master_flight_info_lvl_1_key]['path_1'] = []
									master_flight_info_lvl_1[master_flight_info_lvl_1_key]['path_2'] = []
									is_master_lvl1_key_created = True
								else:
									pass
							else:
								pass

							if is_master_lvl1_key_created is True:
								# chose only if flight is less than 10 hours including stay.
								for master_flight_city_dest_data in master_flight_info['dest'][dest_city_key]:
									# print '388',master_flight_city_dest_data, dest_city_key
									# pdb.set_trace()
									if master_flight_city_dest_data['src_or_dest_city'] == dest_city_key:
										# path1
										master_flight_info_lvl_1[master_flight_info_lvl_1_key]['path_1'].append(
										master_flight_city_dest_data)
									else:
										pass
									# path2
								master_flight_info_lvl_1[master_flight_info_lvl_1_key]['path_2'].append(
									lvl_2_src_city_data)
							else:
								pass
				else:
					pass

	return master_flight_info, master_flight_info_lvl_1

def path_data():
	return Search_route_data()

def human_to_epoch_time(time_human, is_calendar_format=True):
	if is_calendar_format is True:
		try: 
			return int(calendar.timegm((datetime.strptime(time_human.strip(), "%d-%b-%y")).timetuple()))
		except:
			return int(calendar.timegm((datetime.strptime(time_human.strip(), "%d-%b-%Y")).timetuple()))
	else:
		return int(calendar.timegm((datetime.strptime(time_human.strip(), "%H:%M")).timetuple()))



