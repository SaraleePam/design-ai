import Rhino.Geometry as rh

class Agent:

    def __init__(self, pt, r, ro, adj):
        self.cp = pt
        self.radius = r
        self.room = ro
        self.adjacency = adj
        self.neighbors = []

    def add_neighbor(self, other):
        self.neighbors.append(other)

    def collide(self, other, alpha):
        d = self.cp.DistanceTo(other.cp)
        amount = 0
        if d < self.radius + other.radius:
            pt_2 = other.cp
            pt_1 = self.cp
            # get vector from self to other
            v = pt_2 - pt_1
            # change vector magnitude to 1
            v.Unitize()
            # set magnitude to half the overlap distance
            v *= (self.radius + other.radius - d) / 2
            # multiply by alpha parameter to control
            # amount of movement at each time step
            v *= alpha
            amount = v.Length
            # move other object
            t = rh.Transform.Translation(v)
            pt_2.Transform(t)
            # reverse vector and move self same amount
            # in opposite direction
            v.Reverse()
            t = rh.Transform.Translation(v)
            pt_1.Transform(t)
        return amount

    def cluster(self, other, alpha):
        d = self.cp.DistanceTo(other.cp)
        amount = 0
        if d > self.radius + other.radius:
            pt_2 = other.cp
            pt_1 = self.cp
            # get vector from self to other
            v = pt_2 - pt_1
            # change vector magnitude to 1
            v.Unitize()
            # set magnitude to half the overlap distance
            v *= (d - (self.radius + other.radius)) / 2
            # multiply by alpha parameter to control
            # amount of movement at each time step
            v *= alpha
            amount = v.Length
            # move self
            t = rh.Transform.Translation(v)
            pt_1.Transform(t)
            # reverse vector and move other object same amount
            # in opposite direction
            v.Reverse()
            t = rh.Transform.Translation(v)
            pt_2.Transform(t)
        return amount
    def get_circle(self):
        return rh.Circle(self.cp, self.radius)


def run(pts, radii, rooms, adjacencies, max_iters, alpha):

    agents = []

    for i, pt in enumerate(pts):
        my_agent = Agent(pt, radii[i], rooms[i], adjacencies[i])
        agents.append(my_agent)

    for i in range(len(agents)):
        # Second loop to iterate over all instances of agent
        for j in range(len(agents)):
            if agents[j-1].room in agents[i].adjacency:
                #print(agents[i].adjacency)
                agents[j].add_neighbor(agents[i])
            else:
                pass

    # Iterate over agents to generate scores for clustering behaviors
    for i in range(max_iters):
        total_amount = 0
        for j, agent_1 in enumerate(agents):
            # cluster to all agent's neighbors
            for agent_2 in agent_1.neighbors:
                total_amount += agent_1.cluster(agent_2, alpha)
            # collide with all agents after agent in list
            for agent_2 in agents[j+1:]:
                # add extra multiplier to decrease effect of cluster
                total_amount += agent_1.collide(agent_2, alpha/2)
        if total_amount < .01:
            break

    iters = i


    circles = []

    # Call function and append circles to Rhino
    for agent in agents:
        circles.append(agent.get_circle())
    return circles, iters