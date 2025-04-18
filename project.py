import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = -1  # -1 means not started yet

class CPUScheduler:
    def __init__(self):
        self.processes = []
        self.gantt_chart = []
        self.current_time = 0
        self.completed_processes = 0
        
    def add_process(self, process):
        self.processes.append(process)
        
    def calculate_metrics(self):
        total_waiting = 0
        total_turnaround = 0
        total_response = 0
        
        for process in self.processes:
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            total_waiting += process.waiting_time
            total_turnaround += process.turnaround_time
            total_response += process.response_time - process.arrival_time
            
        avg_waiting = total_waiting / len(self.processes)
        avg_turnaround = total_turnaround / len(self.processes)
        avg_response = total_response / len(self.processes)
        
        return {
            "Average Waiting Time": avg_waiting,
            "Average Turnaround Time": avg_turnaround,
            "Average Response Time": avg_response
        }
        
    def fcfs(self):
        self.gantt_chart = []
        self.current_time = 0
        
        # Create a copy of processes to work with
        processes = sorted(self.processes, key=lambda p: p.arrival_time)
        
        for process in processes:
            # If current time is less than arrival time, there's idle time
            if self.current_time < process.arrival_time:
                if len(self.gantt_chart) > 0:
                    self.gantt_chart.append({"pid": "Idle", "start": self.current_time, "end": process.arrival_time})
                self.current_time = process.arrival_time
                
            # Set response time if not already set
            if process.response_time == -1:
                process.response_time = self.current_time
                
            # Add process to Gantt chart
            self.gantt_chart.append({"pid": process.pid, "start": self.current_time, "end": self.current_time + process.burst_time})
            
            # Update current time and completion time
            self.current_time += process.burst_time
            process.completion_time = self.current_time
            process.remaining_time = 0
            
        return self.gantt_chart
    
    def sjf_non_preemptive(self):
        self.gantt_chart = []
        self.current_time = 0
        remaining_processes = self.processes.copy()
        
        while remaining_processes:
            available_processes = [p for p in remaining_processes if p.arrival_time <= self.current_time]
            
            if not available_processes:
                # Find the next process to arrive
                next_process = min(remaining_processes, key=lambda p: p.arrival_time)
                if len(self.gantt_chart) > 0:
                    self.gantt_chart.append({"pid": "Idle", "start": self.current_time, "end": next_process.arrival_time})
                self.current_time = next_process.arrival_time
                continue
                
            # Select process with shortest burst time
            next_process = min(available_processes, key=lambda p: p.burst_time)
            
            # Set response time if not already set
            if next_process.response_time == -1:
                next_process.response_time = self.current_time
                
            # Add process to Gantt chart
            self.gantt_chart.append({"pid": next_process.pid, "start": self.current_time, "end": self.current_time + next_process.burst_time})
            
            # Update current time and completion time
            self.current_time += next_process.burst_time
            next_process.completion_time = self.current_time
            next_process.remaining_time = 0
            
            # Remove the process from remaining processes
            remaining_processes.remove(next_process)
            
        return self.gantt_chart
    
    def sjf_preemptive(self):
        self.gantt_chart = []
        self.current_time = 0
        remaining_processes = self.processes.copy()
        n = len(remaining_processes)
        completed = 0
        prev_process = None
        
        # Reset values
        for process in remaining_processes:
            process.remaining_time = process.burst_time
        
        while completed != n:
            # Find process with minimum remaining time among arrived processes
            min_burst = float('inf')
            shortest_process = None
            
            for process in remaining_processes:
                if process.arrival_time <= self.current_time and process.remaining_time > 0 and process.remaining_time < min_burst:
                    min_burst = process.remaining_time
                    shortest_process = process
            
            if shortest_process is None:
                # No process available, find next arrival
                next_arrival = min([p.arrival_time for p in remaining_processes if p.remaining_time > 0])
                if prev_process is not None:
                    self.gantt_chart.append({"pid": "Idle", "start": self.current_time, "end": next_arrival})
                self.current_time = next_arrival
                continue
            
            # Set response time if not already set
            if shortest_process.response_time == -1:
                shortest_process.response_time = self.current_time
            
            # If process changes, add to Gantt chart
            if prev_process != shortest_process and prev_process is not None:
                # Close previous process entry
                self.gantt_chart[-1]["end"] = self.current_time
                # Start new process entry
                self.gantt_chart.append({"pid": shortest_process.pid, "start": self.current_time, "end": None})
            elif prev_process is None:
                # First process
                self.gantt_chart.append({"pid": shortest_process.pid, "start": self.current_time, "end": None})
            
            # Execute for 1 time unit
            self.current_time += 1
            shortest_process.remaining_time -= 1
            
            # Process completed
            if shortest_process.remaining_time == 0:
                completed += 1
                shortest_process.completion_time = self.current_time
                # Close Gantt chart entry
                self.gantt_chart[-1]["end"] = self.current_time
                prev_process = None
            else:
                prev_process = shortest_process
        
        return self.gantt_chart
    
    def priority_non_preemptive(self):
        self.gantt_chart = []
        self.current_time = 0
        remaining_processes = self.processes.copy()
        
        while remaining_processes:
            available_processes = [p for p in remaining_processes if p.arrival_time <= self.current_time]
            
            if not available_processes:
                # Find the next process to arrive
                next_process = min(remaining_processes, key=lambda p: p.arrival_time)
                if len(self.gantt_chart) > 0:
                    self.gantt_chart.append({"pid": "Idle", "start": self.current_time, "end": next_process.arrival_time})
                self.current_time = next_process.arrival_time
                continue
                
            # Select process with highest priority (lower number = higher priority)
            next_process = min(available_processes, key=lambda p: p.priority)
            
            # Set response time if not already set
            if next_process.response_time == -1:
                next_process.response_time = self.current_time
                
            # Add process to Gantt chart
            self.gantt_chart.append({"pid": next_process.pid, "start": self.current_time, "end": self.current_time + next_process.burst_time})
            
            # Update current time and completion time
            self.current_time += next_process.burst_time
            next_process.completion_time = self.current_time
            next_process.remaining_time = 0
            
            # Remove the process from remaining processes
            remaining_processes.remove(next_process)
            
        return self.gantt_chart
    
    def priority_preemptive(self):
        self.gantt_chart = []
        self.current_time = 0
        remaining_processes = self.processes.copy()
        n = len(remaining_processes)
        completed = 0
        prev_process = None
        
        # Reset values
        for process in remaining_processes:
            process.remaining_time = process.burst_time
        
        while completed != n:
            # Find process with highest priority among arrived processes
            highest_priority = float('inf')
            selected_process = None
            
            for process in remaining_processes:
                if process.arrival_time <= self.current_time and process.remaining_time > 0:
                    if process.priority < highest_priority:
                        highest_priority = process.priority
                        selected_process = process
            
            if selected_process is None:
                # No process available, find next arrival
                next_arrival = min([p.arrival_time for p in remaining_processes if p.remaining_time > 0])
                if prev_process is not None:
                    self.gantt_chart.append({"pid": "Idle", "start": self.current_time, "end": next_arrival})
                self.current_time = next_arrival
                continue
            
            # Set response time if not already set
            if selected_process.response_time == -1:
                selected_process.response_time = self.current_time
            
            # If process changes, add to Gantt chart
            if prev_process != selected_process and prev_process is not None:
                # Close previous process entry
                self.gantt_chart[-1]["end"] = self.current_time
                # Start new process entry
                self.gantt_chart.append({"pid": selected_process.pid, "start": self.current_time, "end": None})
            elif prev_process is None:
                # First process
                self.gantt_chart.append({"pid": selected_process.pid, "start": self.current_time, "end": None})
            
            # Execute for 1 time unit
            self.current_time += 1
            selected_process.remaining_time -= 1
            
            # Process completed
            if selected_process.remaining_time == 0:
                completed += 1
                selected_process.completion_time = self.current_time
                # Close Gantt chart entry
                self.gantt_chart[-1]["end"] = self.current_time
                prev_process = None
            else:
                prev_process = selected_process
        
        return self.gantt_chart
    
    def round_robin(self, time_quantum):
        self.gantt_chart = []
        self.current_time = 0
        remaining_processes = sorted(self.processes.copy(), key=lambda p: p.arrival_time)
        
        # Reset values
        for process in remaining_processes:
            process.remaining_time = process.burst_time
        
        # Create ready queue
        ready_queue = []
        completed = 0
        n = len(remaining_processes)
        
        while completed != n:
            # Add newly arrived processes to ready queue
            new_arrivals = [p for p in remaining_processes if p.arrival_time <= self.current_time and p.remaining_time > 0 and p not in ready_queue]
            ready_queue.extend(new_arrivals)
            
            if not ready_queue:
                # No process in ready queue, find next arrival
                next_arrivals = [p for p in remaining_processes if p.remaining_time > 0]
                if not next_arrivals:
                    break
                next_arrival = min(next_arrivals, key=lambda p: p.arrival_time)
                if len(self.gantt_chart) > 0:
                    self.gantt_chart.append({"pid": "Idle", "start": self.current_time, "end": next_arrival.arrival_time})
                self.current_time = next_arrival.arrival_time
                continue
            
            # Get the first process from ready queue
            current_process = ready_queue.pop(0)
            
            # Set response time if not already set
            if current_process.response_time == -1:
                current_process.response_time = self.current_time
            
            # Calculate execution time in this round
            execute_time = min(time_quantum, current_process.remaining_time)
            
            # Add to Gantt chart
            self.gantt_chart.append({"pid": current_process.pid, "start": self.current_time, "end": self.current_time + execute_time})
            
            # Update current time
            self.current_time += execute_time
            current_process.remaining_time -= execute_time
            
            # Add newly arrived processes during this time quantum
            new_arrivals = [p for p in remaining_processes if p.arrival_time <= self.current_time and p.remaining_time > 0 and p not in ready_queue and p != current_process]
            ready_queue.extend(new_arrivals)
            
            # Check if process completed
            if current_process.remaining_time == 0:
                completed += 1
                current_process.completion_time = self.current_time
            else:
                # Put the process back in the ready queue
                ready_queue.append(current_process)
        
        return self.gantt_chart

class CPUSchedulerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Intelligent CPU Scheduler Simulator")
        self.geometry("1200x800")
        self.processes = []
        self.scheduler = CPUScheduler()
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Algorithm selection frame
        algorithm_frame = ttk.LabelFrame(main_frame, text="Scheduling Algorithm")
        algorithm_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.algorithm_var = tk.StringVar(value="FCFS")
        algorithms = ["FCFS", "SJF", "Priority", "Round Robin"]
        for i, alg in enumerate(algorithms):
            ttk.Radiobutton(algorithm_frame, text=alg, variable=self.algorithm_var, value=alg, 
                            command=self.on_algorithm_change).grid(row=0, column=i, padx=5, pady=5)
        
        # Preemption option
        self.preemptive_var = tk.BooleanVar(value=False)
        self.preemptive_check = ttk.Checkbutton(algorithm_frame, text="Preemptive", variable=self.preemptive_var)
        self.preemptive_check.grid(row=0, column=len(algorithms), padx=5, pady=5)
        self.preemptive_check.config(state=tk.DISABLED)  # Initially disabled for FCFS
        
        # Time quantum (for Round Robin)
        ttk.Label(algorithm_frame, text="Time Quantum:").grid(row=0, column=len(algorithms)+1, padx=5, pady=5)
        self.time_quantum_var = tk.StringVar(value="2")
        self.time_quantum_entry = ttk.Entry(algorithm_frame, textvariable=self.time_quantum_var, width=5)
        self.time_quantum_entry.grid(row=0, column=len(algorithms)+2, padx=5, pady=5)
        self.time_quantum_entry.config(state=tk.DISABLED)  # Initially disabled
        
        # Process input frame
        process_frame = ttk.LabelFrame(main_frame, text="Process Details")
        process_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        # Process ID
        ttk.Label(process_frame, text="Process ID:").grid(row=0, column=0, padx=5, pady=5)
        self.pid_var = tk.StringVar()
        ttk.Entry(process_frame, textvariable=self.pid_var, width=10).grid(row=0, column=1, padx=5, pady=5)
        
        # Arrival Time
        ttk.Label(process_frame, text="Arrival Time:").grid(row=0, column=2, padx=5, pady=5)
        self.arrival_var = tk.StringVar(value="0")
        ttk.Entry(process_frame, textvariable=self.arrival_var, width=10).grid(row=0, column=3, padx=5, pady=5)
        
        # Burst Time
        ttk.Label(process_frame, text="Burst Time:").grid(row=0, column=4, padx=5, pady=5)
        self.burst_var = tk.StringVar()
        ttk.Entry(process_frame, textvariable=self.burst_var, width=10).grid(row=0, column=5, padx=5, pady=5)
        
        # Priority
        ttk.Label(process_frame, text="Priority:").grid(row=0, column=6, padx=5, pady=5)
        self.priority_var = tk.StringVar(value="0")
        self.priority_entry = ttk.Entry(process_frame, textvariable=self.priority_var, width=10)
        self.priority_entry.grid(row=0, column=7, padx=5, pady=5)
        self.priority_entry.config(state=tk.DISABLED)  # Initially disabled for FCFS
        
        # Add process button
        ttk.Button(process_frame, text="Add Process", command=self.add_process).grid(row=0, column=8, padx=5, pady=5)
        
        # Process table frame
        table_frame = ttk.LabelFrame(main_frame, text="Process Table")
        table_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        # Treeview for process table
        columns = ("pid", "arrival", "burst", "priority")
        self.process_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.process_table.heading("pid", text="Process ID")
        self.process_table.heading("arrival", text="Arrival Time")
        self.process_table.heading("burst", text="Burst Time")
        self.process_table.heading("priority", text="Priority")
        
        self.process_table.column("pid", width=100)
        self.process_table.column("arrival", width=100)
        self.process_table.column("burst", width=100)
        self.process_table.column("priority", width=100)
        
        self.process_table.pack(fill="both", expand=True)
        
        # Control buttons frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        
        ttk.Button(control_frame, text="Run Simulation", command=self.run_simulation).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Clear All", command=self.clear_all).pack(side=tk.LEFT, padx=5)
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Simulation Results")
        results_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
        
        # Figure for Gantt chart
        self.fig, self.ax = plt.subplots(figsize=(10, 2))
        self.canvas = FigureCanvasTkAgg(self.fig, results_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Metrics frame
        metrics_frame = ttk.Frame(results_frame)
        metrics_frame.pack(fill="x", padx=5, pady=5)
        
        self.avg_waiting_var = tk.StringVar()
        self.avg_turnaround_var = tk.StringVar()
        self.avg_response_var = tk.StringVar()
        
        ttk.Label(metrics_frame, text="Avg. Waiting Time:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(metrics_frame, textvariable=self.avg_waiting_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(metrics_frame, text="Avg. Turnaround Time:").grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(metrics_frame, textvariable=self.avg_turnaround_var).grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(metrics_frame, text="Avg. Response Time:").grid(row=0, column=4, padx=5, pady=5)
        ttk.Label(metrics_frame, textvariable=self.avg_response_var).grid(row=0, column=5, padx=5, pady=5)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(4, weight=2)
        
    def on_algorithm_change(self):
        algorithm = self.algorithm_var.get()
        
        # Reset UI states based on selected algorithm
        if algorithm == "FCFS":
            self.preemptive_check.config(state=tk.DISABLED)
            self.preemptive_var.set(False)
            self.priority_entry.config(state=tk.DISABLED)
            self.time_quantum_entry.config(state=tk.DISABLED)
        elif algorithm == "Round Robin":
            self.preemptive_check.config(state=tk.DISABLED)
            self.preemptive_var.set(True)  # Round Robin is always preemptive
            self.priority_entry.config(state=tk.DISABLED)
            self.time_quantum_entry.config(state=tk.NORMAL)
        elif algorithm == "SJF":
            self.preemptive_check.config(state=tk.NORMAL)
            self.priority_entry.config(state=tk.DISABLED)
            self.time_quantum_entry.config(state=tk.DISABLED)
        elif algorithm == "Priority":
            self.preemptive_check.config(state=tk.NORMAL)
            self.priority_entry.config(state=tk.NORMAL)
            self.time_quantum_entry.config(state=tk.DISABLED)
    
    def add_process(self):
        try:
            pid = self.pid_var.get()
            arrival_time = int(self.arrival_var.get())
            burst_time = int(self.burst_var.get())
            priority = int(self.priority_var.get())
            
            if not pid or burst_time <= 0:
                messagebox.showerror("Input Error", "Process ID must be provided and burst time must be positive")
                return
                
            # Check for duplicate PID
            existing_pids = [process.pid for process in self.processes]
            if pid in existing_pids:
                messagebox.showerror("Input Error", f"Process ID '{pid}' already exists")
                return
                
            # Create process and add to list
            process = Process(pid, arrival_time, burst_time, priority)
            self.processes.append(process)
            
            # Add to table
            self.process_table.insert("", "end", values=(pid, arrival_time, burst_time, priority))
            
            # Clear input fields
            self.pid_var.set("")
            self.burst_var.set("")
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values")
    
    def clear_all(self):
        self.processes = []
        self.scheduler.processes = []
        self.process_table.delete(*self.process_table.get_children())
        self.ax.clear()
        self.canvas.draw()
        self.avg_waiting_var.set("")
        self.avg_turnaround_var.set("")
        self.avg_response_var.set("")
    
    def run_simulation(self):
        if not self.processes:
            messagebox.showerror("Error", "No processes to simulate")
            return
            
        # Reset scheduler
        self.scheduler = CPUScheduler()
        for process in self.processes:
            # Reset process values for new simulation
            process.remaining_time = process.burst_time
            process.completion_time = 0
            process.waiting_time = 0
            process.turnaround_time = 0
            process.response_time = -1
            self.scheduler.add_process(process)
            
        # Run selected algorithm
        algorithm = self.algorithm_var.get()
        is_preemptive = self.preemptive_var.get()
        
        if algorithm == "FCFS":
            gantt_chart = self.scheduler.fcfs()
        elif algorithm == "SJF":
            if is_preemptive:
                gantt_chart = self.scheduler.sjf_preemptive()
            else:
                gantt_chart = self.scheduler.sjf_non_preemptive()
        elif algorithm == "Priority":
            if is_preemptive:
                gantt_chart = self.scheduler.priority_preemptive()
            else:
                gantt_chart = self.scheduler.priority_non_preemptive()
        elif algorithm == "Round Robin":
            try:
                time_quantum = int(self.time_quantum_var.get())
                if time_quantum <= 0:
                    messagebox.showerror("Input Error", "Time quantum must be positive")
                    return
                gantt_chart = self.scheduler.round_robin(time_quantum)
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid time quantum")
                return
        
        # Calculate metrics
        metrics = self.scheduler.calculate_metrics()
        
        # Display metrics
        self.avg_waiting_var.set(f"{metrics['Average Waiting Time']:.2f}")
        self.avg_turnaround_var.set(f"{metrics['Average Turnaround Time']:.2f}")
        self.avg_response_var.set(f"{metrics['Average Response Time']:.2f}")
        
        # Display Gantt chart
        self.plot_gantt_chart(gantt_chart)
    
    def plot_gantt_chart(self, gantt_chart):
        self.ax.clear()
        
        # Colors for processes (excluding "Idle")
        colors = plt.cm.tab10(np.linspace(0, 1, len(self.processes)))
        color_map = {process.pid: colors[i] for i, process in enumerate(self.processes)}
        color_map["Idle"] = "white"
        
        # Plot each process segment
        for i, segment in enumerate(gantt_chart):
            pid = segment["pid"]
            start = segment["start"]
            end = segment["end"]
            duration = end - start
            
            self.ax.barh(0, duration, left=start, height=0.5, 
                         color=color_map.get(pid, "gray"), 
                         edgecolor="black", 
                         alpha=0.8 if pid != "Idle" else 0.3)
            
            # Add process ID label
            self.ax.text(start + duration/2, 0, pid, 
                         ha='center', va='center', 
                         color='black' if pid != "Idle" else "gray",
                         fontweight='bold')
        
        # Add time markers
        end_time = gantt_chart[-1]["end"]
        self.ax.set_xlim(0, end_time)
        self.ax.set_xticks(list(range(0, end_time + 1)))
        self.ax.set_yticks([])
        self.ax.set_xlabel("Time")
        self.ax.set_title("CPU Scheduling Gantt Chart")
        self.ax.grid(axis='x', linestyle='--', alpha=0.7)
        
        # Add a legend
        handles = [plt.Rectangle((0,0), 1, 1, color=color_map[process.pid]) for process in self.processes]
        labels = [process.pid for process in self.processes]
        if any(segment["pid"] == "Idle" for segment in gantt_chart):
            handles.append(plt.Rectangle((0,0), 1, 1, color=color_map["Idle"], alpha=0.3))
            labels.append("Idle")
        self.ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=5)
        
        plt.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    app = CPUSchedulerApp()
    app.mainloop()