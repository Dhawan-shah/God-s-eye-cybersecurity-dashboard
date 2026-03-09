import tkinter as tk
from tkinter import ttk
import socket
import random
import csv
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.pdfgen import canvas

scan_log=[]
alerts_log=[]

root=tk.Tk()
root.title("👁 GOD'S EYE Cyber Command Center")
root.geometry("1700x950")
root.configure(bg="#0f172a")

title=tk.Label(
root,
text="👁 GOD'S EYE Cyber Defense Command Center",
font=("Arial",26,"bold"),
fg="cyan",
bg="#0f172a"
)
title.pack(pady=10)

cards=tk.Frame(root,bg="#0f172a")
cards.pack()

def create_card(text):
    frame=tk.Frame(cards,bg="#111827",width=200,height=90)
    frame.pack(side="left",padx=10,pady=5)
    label=tk.Label(frame,text=text,font=("Arial",14),fg="cyan",bg="#111827")
    label.pack(expand=True)
    return label

device_label=create_card("Devices: 0")
port_label=create_card("Open Ports: 0")
vuln_label=create_card("Vulnerabilities: 0")
risk_label=create_card("Risk Level: Low")

main=tk.Frame(root,bg="#0f172a")
main.pack(fill="both",expand=True)

panel=tk.Frame(main,bg="#111827",width=230)
panel.pack(side="left",fill="y")

console_frame=tk.Frame(main)
console_frame.pack(side="left",fill="both",expand=True)

analytics=tk.Frame(main,bg="#0f172a",width=450)
analytics.pack(side="right",fill="y")

console=tk.Text(console_frame,bg="black",fg="lime",font=("Consolas",10))
console.pack(fill="both",expand=True)

def log(msg):
    console.insert(tk.END,msg+"\n")
    console.see(tk.END)
    scan_log.append(msg)

alert_title=tk.Label(
analytics,
text="Threat Alerts",
font=("Arial",12,"bold"),
fg="cyan",
bg="#0f172a"
)
alert_title.pack()

alerts=tk.Listbox(analytics,height=6,bg="black",fg="red")
alerts.pack(fill="x")

def add_alert(msg):
    alerts.insert(tk.END,msg)
    alerts_log.append(msg)

timeline_label=tk.Label(
analytics,
text="Incident Timeline",
font=("Arial",12,"bold"),
fg="cyan",
bg="#0f172a"
)
timeline_label.pack(pady=5)

timeline=tk.Listbox(analytics,height=5,bg="#111827",fg="white")
timeline.pack(fill="x")

def add_incident(msg):
    timeline.insert(tk.END,msg)

columns=("Host","Risk Score")
table=ttk.Treeview(analytics,columns=columns,show="headings",height=5)

for col in columns:
    table.heading(col,text=col)

table.pack(pady=10)

def discover_devices():
    table.delete(*table.get_children())
    for i in range(6):
        host=f"192.168.1.{random.randint(2,200)}"
        risk=random.randint(1,10)
        table.insert("",tk.END,values=(host,risk))
    device_label.config(text="Devices: 6")
    log("Network discovery completed")
    add_incident("Devices discovered on network")

def domain_lookup():
    domain=target_entry.get()
    try:
        ip=socket.gethostbyname(domain)
        log(f"{domain} resolved to {ip}")
    except:
        log("Domain lookup failed")

def port_scan():
    target=target_entry.get()
    ports=port_entry.get().split(",")
    open_count=0
    for p in ports:
        try:
            port=int(p)
            s=socket.socket()
            s.settimeout(0.5)
            result=s.connect_ex((target,port))
            if result==0:
                log(f"Port {port} OPEN")
                open_count+=1
            s.close()
        except:
            pass
    port_label.config(text=f"Open Ports: {open_count}")

def threat_monitor():
    threats=[
    "Possible brute force",
    "Suspicious connection",
    "Traffic anomaly",
    "Network scan detected"
    ]
    for i in range(4):
        t=random.choice(threats)
        log("⚠ "+t)
        add_alert(t)
        add_incident(t)

def network_map():
    G=nx.Graph()
    router="Router"
    G.add_node(router)
    for i in range(5):
        d=f"Host-{i}"
        G.add_node(d)
        G.add_edge(router,d)
    plt.figure("Network Topology")
    nx.draw(G,with_labels=True,node_color="red")
    plt.show()

def analytics_chart():
    labels=["Ports","Vulnerabilities","Threats"]
    values=[
    random.randint(1,20),
    random.randint(1,10),
    random.randint(1,6)
    ]
    plt.figure("Security Analytics")
    plt.bar(labels,values)
    plt.show()

def heatmap():
    data=[[random.randint(0,10) for i in range(6)] for j in range(6)]
    sns.heatmap(data,annot=True,cmap="Reds")
    plt.title("Device Vulnerability Heatmap")
    plt.show()

graph_title=tk.Label(
analytics,
text="Live Network Traffic",
fg="cyan",
bg="#0f172a",
font=("Arial",12,"bold")
)
graph_title.pack()

fig = plt.Figure(figsize=(5,3.4), dpi=100)
ax = fig.add_subplot(111)

ax.set_facecolor("#0f172a")
ax.grid(color="cyan", linestyle="--", linewidth=0.3)

traffic=[random.randint(1,10) for _ in range(10)]
line,=ax.plot(traffic,color="lime",linewidth=2)

fig.tight_layout()

chart=FigureCanvasTkAgg(fig,analytics)
chart_widget=chart.get_tk_widget()
chart_widget.pack(fill="both",expand=True,pady=10)

def update_graph():
    traffic.append(random.randint(1,10))
    traffic.pop(0)
    line.set_ydata(traffic)
    line.set_xdata(range(len(traffic)))
    ax.relim()
    ax.autoscale_view()
    fig.tight_layout()
    chart.draw()
    root.after(2000,update_graph)

update_graph()

def generate_report():
    c=canvas.Canvas("security_report.pdf")
    y=800
    c.drawString(50,y,"GOD'S EYE Security Report")
    y-=40
    for line in scan_log:
        c.drawString(50,y,line)
        y-=20
        if y<50:
            c.showPage()
            y=800
    c.save()
    log("PDF report generated")

def export_logs():
    with open("security_logs.csv","w",newline="") as f:
        writer=csv.writer(f)
        for l in scan_log:
            writer.writerow([l])
    log("Logs exported to CSV")

target_entry=tk.Entry(panel)
target_entry.pack(pady=5)
target_entry.insert(0,"example.com")

port_entry=tk.Entry(panel)
port_entry.pack(pady=5)
port_entry.insert(0,"80,443,22")

tk.Button(panel,text="Discover Network",command=discover_devices).pack(pady=6)
tk.Button(panel,text="Domain Lookup",command=domain_lookup).pack(pady=6)
tk.Button(panel,text="Custom Port Scan",command=port_scan).pack(pady=6)
tk.Button(panel,text="Threat Monitor",command=threat_monitor).pack(pady=6)
tk.Button(panel,text="Network Map",command=network_map).pack(pady=6)
tk.Button(panel,text="Security Analytics",command=analytics_chart).pack(pady=6)
tk.Button(panel,text="Vulnerability Heatmap",command=heatmap).pack(pady=6)
tk.Button(panel,text="Generate Report",command=generate_report).pack(pady=6)
tk.Button(panel,text="Export Logs CSV",command=export_logs).pack(pady=6)
tk.Button(panel,text="Clear Console",command=lambda:console.delete(1.0,tk.END)).pack(pady=6)

root.mainloop()