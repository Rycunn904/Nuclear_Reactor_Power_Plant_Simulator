import tkinter as tk
import reactor as Reactor
import turbine as Turbine

root = tk.Tk()
root.title("Nuclear Reactor Simulator")

reactor = Reactor.Reactor()
turbine = Turbine.Turbine(root)

framerate = 60

def scram(event):
    reactor.scram()

def update_status():
    reactor.update()
    turbine.update(reactor.powerOutput)

def create_gui():
    stat_frame = tk.Frame(root, bg="lightgray", borderwidth=3, relief="ridge")
    stat_frame.place(x=5, y=5)

    primary_func = tk.Frame(root, bg="lightgray", borderwidth=3, relief="ridge")
    primary_func.place(x=5, y=160)

    status_label = tk.Label(stat_frame, text="Reactor Status", bg="lightgray")
    status_label.pack(anchor="w")

    temp_label = tk.Label(stat_frame, text="Temperature: 0°C", bg="lightgray")
    temp_label.pack(anchor="w")

    power_label = tk.Label(stat_frame, text="Power Output: 0 MW", bg="lightgray")
    power_label.pack(anchor="w")

    rod_label = tk.Label(stat_frame, text="Control Rod Position: 0%", bg="lightgray")
    rod_label.pack(anchor="w")

    rod_movement_label = tk.Label(stat_frame, text="Control Rod Movement: IDLE", bg="lightgray")
    rod_movement_label.pack(anchor="w")

    cv_label = tk.Label(stat_frame, text="Coolant Valve: Closed", bg="lightgray")
    cv_label.pack(anchor="w")

    pump_label = tk.Label(stat_frame, text="Pumps A/B: 0/0", bg="lightgray")
    pump_label.pack(anchor="w")

    ignition_button = tk.Button(primary_func, text="Toggle Reactor", command=lambda: reactor.toggle_reactor())
    ignition_button.pack()

    rod_up_button = tk.Button(primary_func, text="Start Raising Control Rods", command=lambda: reactor.toggle_move_rods_down())
    rod_up_button.pack()

    rod_down_button = tk.Button(primary_func, text="Start Lowering Control Rods", command=lambda: reactor.toggle_move_rods_up())
    rod_down_button.pack()

    coolant_valve_button = tk.Button(primary_func, text="Open/Close Coolant Valve",  command=lambda: reactor.toggle_coolant_valve())
    coolant_valve_button.pack()

    pump_alpha_button = tk.Button(primary_func, text="Toggle Pump A", command=lambda: reactor.toggle_pump_alpha())
    pump_alpha_button.pack()

    pump_beta_button = tk.Button(primary_func, text="Toggle Pump B", command=lambda: reactor.toggle_pump_beta())
    pump_beta_button.pack()

    # show turbine info on the right side

    turbine_panel = tk.Frame(root, bg="lightgray", borderwidth=3, relief="ridge")
    turbine_panel.place(x=250, y=5)

    grid_panel = tk.Frame(root, bg="lightgray", borderwidth=3, relief="ridge")
    grid_panel.place(x=250, y = 180)

    turbine_label = tk.Label(turbine_panel, text="Turbine Status", bg="lightgray")
    turbine_label.pack(anchor="w")

    turbine_rpm_label = tk.Label(turbine_panel, text="Turbine RPM: 0", bg="lightgray")
    turbine_rpm_label.pack(anchor="w")

    turbine_power_label = tk.Label(turbine_panel, text="Turbine Power Output: 0 MW", bg="lightgray")
    turbine_power_label.pack(anchor="w")

    turbine_valve_label = tk.Label(turbine_panel, text="Turbine Valve Position: 0%", bg="lightgray")
    turbine_valve_label.pack(anchor="w")

    turbine_valve_scale = tk.Scale(root, length=200, from_=0, to=100, resolution=1, orient=tk.HORIZONTAL, label="Turbine Valve", command=lambda val: turbine.set_valve(float(val)/100))
    turbine_valve_scale.place(x=250, y=100)

    turbine_grid_sync = tk.Button(grid_panel, text="Sync to grid", command=lambda: turbine.grid_sync())
    turbine_grid_sync.pack()

    turbine_trip = tk.Button(grid_panel, text="Trip Turbine", command=lambda: turbine.trip())
    turbine_trip.pack()

    turbine_breaker_open = tk.Button(grid_panel, text="Open Breaker", command=lambda: turbine.open_breaker())
    turbine_breaker_open.pack()

    # AZ-5 Canvas

    az5_canvas = tk.Canvas(root, width=75, height=85, bg="black")
    az5_canvas.place(x=171, y=100)

    az5_canvas.create_oval(8,8,70,70, fill="#FF0000", outline="#A40000", width=3, tags="1")
    az5_canvas.create_line(17,17,60,60, fill="#A40000", width=5)
    az5_canvas.create_text(75/2,80, text="AZ-5", fill="#FFFFFF")

    az5_canvas.bind("<Button-1>", scram)

    def refresh():
        update_status()

        if turbine.exploded:
            turb_stat = f"Broken {5000 - turbine.repairTimer}"
        elif turbine.triped:
            turb_stat = "Tripped"
        elif turbine.breakers:
            turb_stat = "Selling Power"
        elif turbine.synced:
            turb_stat = "Synced"
        elif 0 < turbine.rpm < 3200:
            turb_stat = "Running"
        elif turbine.rpm >= 3200:
            turb_stat = "High RPM"
        else:
            turb_stat = "Offline"

        status_label.config(text=f"Reactor {reactor.status}")
        temp_label.config(text=f"Temperature: {reactor.temperature:.1f}°C")
        power_label.config(text=f"Power Output: {reactor.powerOutput:.0f} MW")
        rod_label.config(text=f"Control Rod Position: {int(reactor.controlRodPosition)}%")
        rod_movement_label.config(text=f"Control Rod Movement: {reactor.rodMovementRate}")
        pump_label.config(text=f"Pumps A/B: {"ON" if reactor.pumpA else "OFF"}/{"ON" if reactor.pumpB else "OFF"}")
        turbine_label.config(text=f"Turbine Status: {turb_stat}")
        turbine_rpm_label.config(text=f"Turbine RPM: {turbine.rpm:.0f}")
        turbine_power_label.config(text=f"Turbine Power Output: {turbine.powerOutput:.2f} MW")
        turbine_valve_label.config(text=f"Turbine Valve Position: {turbine.valve*100:.0f}%")
        cv_label.config(text=f"Coolant Valve: {"Open" if reactor.cvOpen else "Closed"}")
        root.after(int(1000/framerate), refresh)

    refresh()
    root.geometry("800x600")
    root.mainloop()

create_gui()