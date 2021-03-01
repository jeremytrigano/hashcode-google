import sys

# READ FILE
data = []
input = sys.argv[1]

with open(f"{input}.txt", "r") as file:
    for line in file:
        data.append(line.replace('\n', ''))

class Street:
    def __init__(self, intersection, name, duration):
        self.intersection = intersection
        self.name = name
        self.duration = duration

class Car:
    def __init__(self, id, path, current_street):
        self.id = id
        self.path = path
        self.current_street = current_street


# GET FIRST LINE DATA
first = data[0]
first_line = first.split(' ')
simulation_duration, intersections, streets, cars, points = [int(x) for x in first_line]
streets_lines = data[1:streets+1]
cars_lines = data[streets+1:]

list_streets = []
dict_inters_incoming = {str(i):[] for i in range(intersections)}
for street in streets_lines:
    values = street.split(' ')
    street_obj = Street(values[1], values[2], values[3])
    list_streets.append(street_obj)
    dict_inters_incoming[values[1]].append(street_obj)

dict_street_weight = {}
list_cars = []
ids_cars = 0
max_path = []
paths = []
for car in cars_lines:
    path = car.split(' ')[1:]
    if len(path) > len(max_path):
        max_path = path
    paths.append(path)
    for street in path[:-1]:
        dict_street_weight[street] = 1 if street not in dict_street_weight else dict_street_weight[street] + 1
    car_obj = Car(ids_cars, path, path[0])
    list_cars.append(car_obj)
    ids_cars += 1

dict_street_weight = {street:weight for street, weight in dict_street_weight.items() if weight > 2}

len_max_path = len(max_path)
for path in paths:
    for index, street in enumerate(path[:-1]):
        value = len_max_path - (index + 1)
        dict_street_weight[street] = value if street not in dict_street_weight else dict_street_weight[street] + value

count = 0
dict_total_streets_weight_inter = {}
dict_inters_incoming_weighted = {}
intersections = []
for key, value in dict_inters_incoming.items():
    total_streets_weight_inter = sum([dict_street_weight[street.name] for street in value if street.name in dict_street_weight])
    dict_total_streets_weight_inter[key] = total_streets_weight_inter

    for street in value:
        if street.name in dict_street_weight:
            dict_inters_incoming_weighted[key] = [street] if key not in dict_inters_incoming_weighted else dict_inters_incoming_weighted[key] + [street]

with open(f"result_{input}", "w") as output:
    output.write(f"{len(dict_inters_incoming_weighted)}\n")
    for intersection, streets in dict_inters_incoming_weighted.items():
        output.write(f"{intersection}\n")
        output.write(f"{len(streets)}\n")
        tmp_dict = {street.name:dict_street_weight[street.name] for street in streets}
        tmp_dict = {k: v for k, v in sorted(tmp_dict.items(), key=lambda item: item[1], reverse=True)}
        streets_ordered_by_weight = list(tmp_dict)
        for street in streets_ordered_by_weight:
            light_duration = 2 if dict_street_weight[street] > dict_total_streets_weight_inter[intersection] * 0.75 and len(streets) > 1 else 1
            output.write(f"{street} {light_duration}\n")