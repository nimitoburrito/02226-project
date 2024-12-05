class Switch:
    def __init__(self, id, ports):
        self.all_frames = []
        self.shaped_queues = dict()
        self.id = id
        self.ports = ports
    
    def add_frame(self, frame, ingress):
        self.all_frames.append(frame)
        if ingress not in self.shaped_queues:
            self.shaped_queues[ingress] = dict()
        if frame[0] not in self.shaped_queues[ingress]:
            self.shaped_queues[ingress][frame[0]] = []
        
        self.shaped_queues[ingress][frame[0]].append(frame)

    def calculate_individual_delay(self, frame_j):
        higher_priorities = []
        same_priorities = []
        lower_priorities = []

        for frame in self.all_frames:
            if frame_j[0] < frame[0]:
                higher_priorities.append(frame)
            if frame_j != frame and frame_j[0] == frame[0]:
                same_priorities.append(frame)
            if frame_j[0] > frame[0]:
                lower_priorities.append(frame)
        
        b_H_hat = 0
        r_H_hat = 0
        for frame in higher_priorities:
            b_H_hat += (int(frame[5])/8)
            r_H_hat += (int(frame[5])/8)/(int(frame[6])*1000000)
        b_C_j_hat = 0
        for frame in same_priorities:
            b_C_j_hat += (int(frame[5])/8)

        b_j_hat = int(frame_j[5])/8

        l_j_breve = int(frame_j[5])/8
        l_L_hat = 0

        if lower_priorities:
            l_L_hat = int(lower_priorities[0][5])/8

        for frame in lower_priorities:
            if int(frame[5]) > l_L_hat:
                l_L_hat = int(frame[5])/8

        r = 1000000000


        return ((b_H_hat + b_C_j_hat + b_j_hat - l_j_breve + l_L_hat)/(r-r_H_hat) + (l_j_breve/r))*1000000

    def calculate_delay(self, frame, ingress):
        highest = self.calculate_individual_delay(frame)
        for interfering_frame in self.shaped_queues[ingress][frame[0]]:
            new_value = self.calculate_individual_delay(interfering_frame)
            if self.calculate_individual_delay(interfering_frame) > highest:
                highest = new_value

        return highest
    
    def __eq__(self, other):
        return self.id == other.id


    def __hash__(self):
        return hash(self.id)

