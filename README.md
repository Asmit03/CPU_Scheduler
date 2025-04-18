A comprehensive educational tool for simulating and visualizing various CPU scheduling algorithms with an intuitive graphical interface.
Features

Multiple Scheduling Algorithms:

First-Come-First-Serve (FCFS)
Shortest Job First (SJF) - both preemptive and non-preemptive
Priority Scheduling - both preemptive and non-preemptive
Round Robin with configurable time quantum


Interactive Visualization:

Color-coded Gantt charts for visualizing process execution
Real-time performance metrics calculation
Clear representation of CPU idle time


Process Management:

Add custom processes with unique IDs
Configure arrival time, burst time, and priority
Organized process table view


Performance Metrics:

Average Waiting Time
Average Turnaround Time
Average Response Time


Screenshots

![Screenshot 2025-04-18 215657](https://github.com/user-attachments/assets/47f6a4f8-74e6-4ecf-afb8-d5a560afdfaf)
![Screenshot 2025-04-18 215537](https://github.com/user-attachments/assets/66b14160-d310-48fb-831f-1b676c8fe695)
![Screenshot 2025-04-18 215606](https://github.com/user-attachments/assets/934006d1-d696-488a-b5db-6074d01bb9e7)

Requirements

Python 3.x
Tkinter (usually included with Python)
Matplotlib
NumPy
Pandas

Installation

Clone this repository:
git clone https://github.com/Asmit03/CPU_Scheduler.git
cd CPU_Scheduler

Install the required dependencies:
pip install matplotlib numpy pandas tkinter

Run the simulator:
python cpu_scheduler.py


How to Use

Select a Scheduling Algorithm:

Choose between FCFS, SJF, Priority, or Round Robin
For SJF and Priority, you can toggle between preemptive and non-preemptive modes
For Round Robin, specify the time quantum


Add Processes:

Enter a unique Process ID
Specify Arrival Time (when the process enters the system)
Enter Burst Time (CPU execution time needed)
Set Priority value (lower number means higher priority, used only for Priority scheduling)
Click "Add Process"


Run the Simulation:

Click "Run Simulation" to execute the selected algorithm
View the Gantt chart showing process execution timeline
Check the performance metrics displayed at the bottom


Analyze Results:

Compare different algorithms by running simulations multiple times
Observe how different parameters affect performance



Implementation Details
Core Classes
Process Class
Represents a process with attributes including:

Process ID
Arrival time
Burst time
Priority
Remaining time
Completion time
Waiting time
Turnaround time
Response time

CPUScheduler Class
Implements various scheduling algorithms:

FCFS (First-Come-First-Serve)
SJF (Shortest Job First) - both preemptive and non-preemptive
Priority Scheduling - both preemptive and non-preemptive
Round Robin with configurable time quantum

CPUSchedulerApp Class
Implements the GUI using Tkinter:

Algorithm selection interface
Process input form
Process table
Gantt chart visualization using Matplotlib
Performance metrics display

Algorithms Implementation

FCFS: Processes are executed in order of arrival.
SJF Non-preemptive: Selects the process with shortest burst time among arrived processes.
SJF Preemptive (SRTF): Preempts current process if a new process arrives with shorter remaining time.
Priority Non-preemptive: Selects the process with highest priority (lowest number) among arrived processes.
Priority Preemptive: Preempts current process if a new process arrives with higher priority.
Round Robin: Executes each process for a fixed time quantum in a cyclic manner.

Data Flow
The simulator follows this data flow:

User inputs process details and algorithm parameters
Process objects are created and stored
Selected scheduling algorithm is executed
Gantt chart and metrics are calculated
Results are displayed visually
![Screenshot 2025-04-18 215221](https://github.com/user-attachments/assets/18f9eeb4-decd-47f1-812c-afcc50f128ac)

Contributing
Contributions are welcome! Here are some ways you can contribute:

Add new scheduling algorithms
Improve the visualization
Enhance the user interface
Fix bugs or optimize performance

License
This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments

Inspired by operating system concepts and CPU scheduling principles
Built with Python and Tkinter for educational purposes
