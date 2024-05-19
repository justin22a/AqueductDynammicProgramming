import heapq

def load(file_path):
    #here we just open the file and begin reading it
    with open(file_path, 'r') as file:
        grid_size = file.readline().strip().split(',')
        rows, cols = int(grid_size[0]), int(grid_size[1])
        #initialize a container for the grid heights
        grid_height_container = []
        for _ in range(rows):
            row = []
            for _ in range(cols):
                row.append(0)
            grid_height_container.append(row)

        #iterate the rows and columns of the given data
        for r in range(rows):
            for c in range(cols):
                line = file.readline().strip().split(',')
                height, xpos, ypos = int(line[0]), int(line[1]), int(line[2])
                grid_height_container[xpos][ypos] = height

        #map our data
        start_x, start_y = map(int, file.readline().strip().split(','))

        special_stations = []

        #iterate the file
        for coordinates in file:
            #Remove leading whitespaces and split the line by comma
            split_coordinates = coordinates.strip().split(',')

            #Convert each coordinate to an integer
            x = int(split_coordinates[0])
            y = int(split_coordinates[1])

            special_stations.append((x, y))

    #retrun all the read data
    return rows, cols, grid_height_container, start_x, start_y, special_stations

def compute_minimum_path(rows, cols, grid_heights, start_x, start_y, special_stations):
    indices_of_stations = {}
    for i in range(len(special_stations)):
        indices_of_stations[special_stations[i]] = i

    full_visit_mask = 0
    for _ in range(len(special_stations)):
        full_visit_mask <<= 1
        full_visit_mask |= 1

    path_costs = {}
    initial_mask = 0
    if (start_x, start_y) in indices_of_stations:
        initial_mask |= (1 << indices_of_stations[(start_x, start_y)])
    path_costs[(start_x, start_y, initial_mask)] = 0
    priority_queue = [(0, start_x, start_y, initial_mask)]

    def travel_time(xi, yi, xf, yf):
        #here is the given formula that we will use in this project
        return max(-1, 1 + (grid_heights[xf][yf] - grid_heights[xi][yi]))

    while priority_queue:
        # Pop the item with the smallest cost from the priority queue
        item = heapq.heappop(priority_queue)
        cost = item[0]
        x = item[1]
        y = item[2]
        visited = item[3]

        # Check if the cost to reach the current cell with the current visited state is already stored
        if (x, y, visited) in path_costs and path_costs[(x, y, visited)] < cost:
            continue

        path_costs[(x, y, visited)] = cost

        for move_x, move_y in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x = x + move_x
            new_y = y + move_y

            if 0 <= new_x < rows and 0 <= new_y < cols:
                new_visited = visited

                if (new_x, new_y) in indices_of_stations:
                    station_index = indices_of_stations[(new_x, new_y)]
                    new_visited |= (1 << station_index)

                new_cost = cost + travel_time(x, y, new_x, new_y)

                if (new_x, new_y, new_visited) not in path_costs or new_cost < path_costs[(new_x, new_y, new_visited)]:
                    path_costs[(new_x, new_y, new_visited)] = new_cost
                    heapq.heappush(priority_queue, (new_cost, new_x, new_y, new_visited))
    least_cost = float('inf')

    for (loc_x, loc_y), idx in indices_of_stations.items():
        full_visit_tuple = (loc_x, loc_y, full_visit_mask)

        if full_visit_tuple in path_costs:
            cost_for_station = path_costs[full_visit_tuple]

            least_cost = min(least_cost, cost_for_station)

    return least_cost


def execute():
    file_name = "grid.txt"
    rows, cols, grid_heights, start_x, start_y, special_stations = load(file_name)
    min_cost = compute_minimum_path(rows, cols, grid_heights, start_x, start_y, special_stations)
    with open('pathLength.txt', 'w') as file:  # write as pathLength.txt as destination
        file.write(str(min_cost))

if __name__ == '__main__':
    execute()

