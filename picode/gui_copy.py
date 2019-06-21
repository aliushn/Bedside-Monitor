import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.animation as animation
import datetime as dt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
import sched

class GUI():
    def __init__(self, patient_name, dob_str, doctor_name,Tempq,PPGirq,PPGredq,hrq,rrq,spo2q,ecgfiltq):
        self.root = tk.Tk()
        self.root.configure(bg = "black")
        self.root.geometry("800x480")
        plt.style.use('dark_background')
        self.patient_name=patient_name
        self.dob_str=dob_str
        self.doctor_name=doctor_name
        self.connected=True
        #Displaying Patient-Doctor info
        dob_obj = dt.datetime.strptime(self.dob_str, '%d%m%y')
        patient_info = tk.Label(self.root, text = "Name: "+self.patient_name+"  DOB: "+dt.datetime.strftime(dob_obj, '%d/%m/%y'), fg="white", bg="black")
        patient_info.grid(row=0, column=0, sticky='W')
        doctor_info = tk.Label(self.root, text = "Doctor: "+self.doctor_name, fg="white", bg="black")
        doctor_info.grid(row=0, column=1, sticky='W')
        #Heart Rate Digital Initilisation
        self.hr_info1 = tk.Label(self.root, text = "Heart Rate:", fg="green", bg="black", font=("Arial",14))
        self.hr_info2 = tk.Label(self.root, text = "--", fg="green", bg="black", font=("Arial", 40))
        self.hr_info3 = tk.Label(self.root, text = "bpm", fg="green", bg="black", font=("Arial", 14))
        self.hr_info1.grid(row=1, column=2)
        self.hr_info2.grid(row=2, column=2)
        self.hr_info3.grid(row=3, column=2)
        #SPO2 Digital Initilisaton
        self.spo2_info1 = tk.Label(self.root, text = "SpO2:", fg="yellow", bg="black", font=("Arial",14))
        self.spo2_info2 = tk.Label(self.root, text = "--", fg="yellow", bg="black", font=("Arial", 40))
        self.spo2_info3 = tk.Label(self.root, text = "%", fg="yellow", bg="black", font=("Arial", 14))
        self.spo2_info1.grid(row=4, column=2)
        self.spo2_info2.grid(row=5, column=2)
        self.spo2_info3.grid(row=6, column=2)
        #Temperature Digital Inilisation
        self.temp_info1 = tk.Label(self.root, text = "Temperature:", fg="red", bg="black", font=("Arial",14))
        self.temp_info2 = tk.Label(self.root, text = "--", fg="red", bg="black", font=("Arial", 40))
        self.temp_info3 = tk.Label(self.root, text = "˚C", fg="red", bg="black", font=("Arial", 14))
        self.temp_info1.grid(row=7, column=2)
        self.temp_info2.grid(row=8, column=2)
        self.temp_info3.grid(row=9, column=2)
        # Respiration Rate
        self.resp_info1 = tk.Label(self.root, text = "Respiration Rate:", fg="blue", bg="black", font=("Arial",14))
        self.resp_info2 = tk.Label(self.root, text = "--", fg="blue", bg="black", font=("Arial", 40))
        self.resp_info3 = tk.Label(self.root, text = "˚C", fg="blue", bg="black", font=("Arial", 14))
        self.resp_info1.grid(row=10, column=2)
        self.resp_info2.grid(row=11, column=2)
        self.resp_info3.grid(row=12, column=2)
        #Graphs Initilisation
        self.ecg_len=600
        self.ppg_len=200
        self.rr_len=200
        self.x_rr1=0
        self.x_ecg=list(range(0,self.ecg_len))
        self.x_ppg=list(range(0,self.ppg_len))
        self.x_rr=list(range(0,self.rr_len))
        #print(xs)
        self.y_ecg=[0]*self.ecg_len
        self.y_ppg=[0]*self.ppg_len
        self.y_rr=[0]*self.rr_len
        # ECG Graph pane
        self.fig_ecg = Figure(figsize=(6.7,1.3), constrained_layout=True)
        self.ax_ecg = self.fig_ecg.add_subplot(111)
        self.format_axis('e', self.ax_ecg)
        self.graph_ecg = FigureCanvasTkAgg(self.fig_ecg, master=self.root)
        self.graph_ecg.get_tk_widget().grid(row=1, column=0, columnspan=2, rowspan=4)
        self.ecg_line, =self.ax_ecg.plot(self.x_ecg, self.y_ecg, color="#59eaed")
        self.ax_ecg.set_ylim([400,700])
        # PPG Graph pane
        self.fig_ppg = Figure(figsize=(6.7,1.3), constrained_layout=True)
        self.ax_ppg = self.fig_ppg.add_subplot(111)
        self.format_axis('p', self.ax_ppg)
        self.graph_ppg = FigureCanvasTkAgg(self.fig_ppg, master=self.root)
        self.graph_ppg.get_tk_widget().grid(row=5, column=0, columnspan=2, rowspan=4)
        self.ppg_line, =self.ax_ppg.plot(self.x_ppg, self.y_ppg, color="#f51a18")
        self.ax_ppg.set_ylim([0,35000])
        # Respiration Graph pane
        self.fig_resp = Figure(figsize=(6.7,1.3), constrained_layout=True)
        self.ax_resp = self.fig_resp.add_subplot(111)
        self.format_axis('r', self.ax_resp)
        self.graph_resp = FigureCanvasTkAgg(self.fig_resp, master=self.root)
        self.graph_resp.get_tk_widget().grid(row=9, column=0, columnspan=2, rowspan=4)
        self.rr_line, =self.ax_resp.plot(self.x_rr, self.y_rr, color="#3cd82c")
        self.ax_resp.set_ylim([-2,2])
        # Report issue button
        self.report_button = tk.Button(self.root, text="REPORT ISSUE", command=self.report, width=70, height=2, fg="white", highlightbackground="black", bg="gray", activebackground="red")
        self.report_button.grid(row = 13, column=0, columnspan = 2, sticky='E')
        #self.ecg_thread=ecgthread
        #self.ppg_thread=ppgthread
        #self.rr_thread=rrthread
        self.Tempq=Tempq
        self.PPGirq=PPGirq
        self.PPGredq=PPGredq
        self.hrq=hrq
        self.spo2q=spo2q
        self.ecgfiltq=ecgfiltq
        # Apply appropriate formatting to axes
    def format_axis(self,id, ax):
        if id == 'e':
            ax.set_ylabel('V', fontsize=8)
            ax.set_title("ECG",fontsize=9)
        elif id == 'p':
            ax.set_ylabel('PPG unit', fontsize=8)
            ax.set_title("PPG",fontsize=9)
        else:
            ax.set_ylabel('rpm', fontsize=8)
            ax.set_title("Respiration",fontsize=9)
        ax.set_xlabel("Time", fontsize=8)
        for tick in ax.get_xticklabels():
            tick.set_fontsize(6)
        for tick in ax.get_yticklabels():
            tick.set_fontsize(6)

    # Set critical flag when report issue button is pressed - send this info to DB
    def report(self):
        critical = True
        critical_time = dt.datetime.utcnow()
    def animateecg(self,i,ys):

        global x_ecg
        # Read data into arrays
        #xar.append(dt.datetime.utcnow())
        ys.extend(self.ecgfiltq.get()) 
        #y_ppg.append(x)
        #y_resp.append(x**3)

        # Limit arrays to store only the most recent 20 readings
        #xar = xar[-200:]
        ys = ys[-self.ecg_len:]
        #y_ppg = y_ppg[-100:]
        #y_resp = y_resp[-100:]

        # remove - just for RT testing
        #self.x_ecg += 1
        #if (x_ecg/(2*math.pi))==1:
        #x_ecg=0
        #print("helooo")
        self.ecg_line.set_ydata(ys)
        #print("wassp")
        #ppg_line.set_ydata(y_ppg)
        #rr_line.set_ydata(y_resp)
        return self.ecg_line,
        # Produce ECG plot
        #plotter('e', ax_ecg, xar, y_ecg)

        # Produce PPG plot
        #plotter('p', ax_ppg, xar, y_ppg)

        # Produce respiration plot
        #plotter('r', ax_resp, xar, y_resp)

    def animateppg(self,i,ys):

        global x_ppg
        # Read data into arrays
        #xar.append(dt.datetime.utcnow())
        #print(self.PPGirq.get())
        ys.extend(self.PPGirq.get()) 
        #ys.append(math.sin(x_ppg/2*math.pi)) 
        #y_ppg.append(x)
        #y_resp.append(x**3)

        # Limit arrays to store only the most recent 20 readings
        #xar = xar[-200:]
        ys = ys[-self.ppg_len:]
        #y_ppg = y_ppg[-100:]
        #y_resp = y_resp[-100:]

        # remove - just for RT testing
        #self.x_ppg += 1
        #if (x_ppg/(2*math.pi))==1:
            #x_ppg=0
        #print("helooo")
        self.ppg_line.set_ydata(ys)
        #print("wassp")
        #ppg_line.set_ydata(y_ppg)
        #rr_line.set_ydata(y_resp)
        return self.ppg_line,
        # Produce ECG plot
        #plotter('e', ax_ecg, xar, y_ecg)

        # Produce PPG plot
        #plotter('p', ax_ppg, xar, y_ppg)

        # Produce respiration plot
        #plotter('r', ax_resp, xar, y_resp)
    def animater(self,i,ys):

        global x_resp

        #temp=self.Tempq.get()
        #self.temp_info2 = tk.Label(self.root, text = str(temp), fg="red", bg="black", font=("Arial", 40))
        #self.temp_info2.grid(row=8, column=2)

        # Read data into arrays
        #xar.append(dt.datetime.utcnow())
        ys.append(math.sin(self.x_rr1/2*math.pi)) 
        #y_ppg.append(x)
        #y_resp.append(x**3)

        # Limit arrays to store only the most recent 20 readings
        #xar = xar[-200:]
        ys = ys[-self.rr_len:]
        #y_ppg = y_ppg[-100:]
        #y_resp = y_resp[-100:]

        # remove - just for RT testing
        self.x_rr1 += 1
        if (self.x_rr1/(2*math.pi))==1:
            self.x_rr1=0
        #print("helooo")
        self.rr_line.set_ydata(ys)
        #print("wassp")
        #ppg_line.set_ydata(y_ppg)
        #rr_line.set_ydata(y_resp)
        return self.rr_line,
        # Produce ECG plot
        #plotter('e', ax_ecg, xar, y_ecg)

        # Produce PPG plot
        #plotter('p', ax_ppg, xar, y_ppg)

        # Produce respiration plot
        #
    def animatesp02(self):
        spo2=self.spo2q.get()
        self.spo2_info2 = tk.Label(self.root, text = "98.7", fg="yellow", bg="black", font=("Arial", 40))
        self.spo2_info2.grid(row=5, column=2)
    def animatehr(self):
        hr=self.hrq.get()
        self.hr_info2 = tk.Label(self.root, text = "65" , fg="green", bg="black", font=("Arial", 40))
        self.hr_info2.grid(row=2, column=2)
    def animatetemp(self):
        temp=self.Tempq.get()
        self.temp_info2.configure(text=str(temp))
        #sc.enter(3000, 1, g.animatetemp, (sc,))
    def animaterr(self):
        rr=self.rrq.get()
        self.resp_info2 = tk.Label(self.root, text = "20", fg="blue", bg="black", font=("Arial", 40))
        self.resp_info2.grid(row=11, column=2)
        
        
#ani = animation.FuncAnimation(fig_ecg, animate, fargs = (), interval=1000) # animate graph every 1000 ms

#self.root.mainloop() # tkinter GUI window