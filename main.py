'''
Author: Muhammad Mobeen
Reg No: 200901097
BS-CS-01  (B)
Lab Task [21 DEC 2022]
Submitted to Mam Reeda Saeed

Explaination of Task:-
I have made a list of Processes and each process is made up of an individual list that contains the attributes
to specify that spacific list. This was done to simplify the class/functions structure for the Round Robin Algorithm.

                       Process = [No.,at,bt,ct,tat,wt]
'''
from queue import Queue

class RoundRobin:
    def __init__(self):
        self.quantum = int()
        self.process_list = None
        self.ready_queue = Queue()
        self.AvgTAT = 0
        self.AvgWT = 0
        self.Gantt_Chart = 0
        self.RealGanttChart = []

    def findCompletionTime(self):
        completed_processes = []

        self.prepareProcessList()

        self.increment_unitime(inc=False)
        while not len(self.process_list) == len(completed_processes):
            if self.ready_queue:
                process_no = self.ready_queue.get()
                if self.quantum < self.process_list[process_no-1][2][0]:
                    for i in range(self.quantum):
                        self.process_list[process_no-1][2][0] -= 1
                        self.RealGanttChart.append(process_no)
                        self.increment_unitime()
                    self.ready_queue.put(process_no)
                elif self.quantum == self.process_list[process_no-1][2][0]:
                    for i in range(self.quantum):
                        self.process_list[process_no-1][2][0] -= 1
                        self.RealGanttChart.append(process_no)
                        self.increment_unitime()
                    self.process_list[process_no-1].append(self.Gantt_Chart) # Adding Completion Time
                    completed_processes.append(process_no)
                elif self.quantum > self.process_list[process_no-1][2][0]:
                    while self.process_list[process_no-1][2][0] > 0:
                        self.process_list[process_no-1][2][0] -= 1
                        self.RealGanttChart.append(process_no)
                        self.increment_unitime()
                    self.process_list[process_no-1].append(self.Gantt_Chart) # Adding Completion Time
                    completed_processes.append(process_no)
            else:
                self.increment_unitime()
        self.prepareProcessList(repair=True)

    def increment_unitime(self, inc=True, check=True):
        if inc:
            self.Gantt_Chart += 1
        if check:    
            for p in self.process_list:
                if self.Gantt_Chart == p[1]:
                    self.ready_queue.put(p[0])

    def prepareProcessList(self, repair=False):
        if not repair:
            for i,p in enumerate(self.process_list):
                self.process_list[i][2] = [p[2],p[2]]
        else:
            for i,p in enumerate(self.process_list):
                self.process_list[i][2] = p[2][1]
            
    def findTAT(self):
        for i,p in enumerate(self.process_list):
            self.process_list[i].append(p[3]-p[1])

    def findWT(self):
        for i,p in enumerate(self.process_list):
            self.process_list[i].append(p[4]-p[2])

    def findAvgTAT(self):
        for i,p in enumerate(self.process_list):
            self.AvgTAT += p[4]
        self.AvgTAT /= len(self.process_list)

    def findAvgWT(self):
        for i,p in enumerate(self.process_list):
            self.AvgWT += p[5]
        self.AvgWT /= len(self.process_list)

    def SortRealGanttChart(self):
        realGanttChart = []
        for v in self.RealGanttChart:
            if realGanttChart:
                if realGanttChart[-1] != v:
                    realGanttChart.append(v)
            else:
                realGanttChart.append(v)
        self.RealGanttChart = realGanttChart

    def showData(self):
        print("____________________________________________________________________________")
        print("Processes Ran from 0 --> {}".format(self.Gantt_Chart))
        print("Processes Sequence Gantt Chart: ",end="")
        self.SortRealGanttChart()
        for x,p in enumerate(self.RealGanttChart):
            if x == len(self.RealGanttChart)-1:
                print("{}".format(p))
            else:
                print("{}".format(p),end="-->")
        print("Average Turn-around Time = ", self.AvgTAT)
        print("Average Wait Time = ", self.AvgWT)

        for p in self.process_list:
            print("\n-----------------------------------------------------------------")
            print("Process #{}:-".format(p[0]))
            print("Arrival Time: ", p[1])
            print("Burst Time: ", p[2])
            print("Completion Time: ", p[3])
            print("Turn-around Time: ", p[4])
            print("Wait Time: ", p[5])

if __name__ == "__main__":
    scheduler = RoundRobin()

    scheduler.quantum = 4
    # Processes |  Process No. | Arrival Time |  Burst Time |
    P1          = [     1      ,      0       ,       5     ]
    P2          = [     2      ,      1       ,       6     ]
    P3          = [     3      ,      2       ,       3     ]
    P4          = [     4      ,      3       ,       1     ]
    P5          = [     5      ,      4       ,       5     ]
    P6          = [     6      ,      6       ,       4     ]
    scheduler.process_list = [P1, P2, P3, P4, P5, P6]

    scheduler.findCompletionTime()
    scheduler.findTAT()
    scheduler.findWT()
    scheduler.findAvgTAT()
    scheduler.findAvgWT()
    scheduler.showData()
    

