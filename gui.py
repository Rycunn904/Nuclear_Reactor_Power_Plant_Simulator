import tkinter as tk
import reactor as Reactor
import turbine as Turbine

reactor = Reactor.Reactor()
turbine = Turbine.Turbine()

root = tk.Tk()
root.title("Nuclear Reactor Simulator")

framerate = 60

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
    turbine_label = tk.Label(root, text="Turbine Status")
    turbine_label.place(x=250, y=0)

    turbine_rpm_label = tk.Label(root, text="Turbine RPM: 0")
    turbine_rpm_label.place(x=250, y=20)

    turbine_power_label = tk.Label(root, text="Turbine Power Output: 0 MW")
    turbine_power_label.place(x=250, y=40)

    turbine_valve_label = tk.Label(root, text="Turbine Valve Position: 0%")
    turbine_valve_label.place(x=250, y=60)

    turbine_valve_scale = tk.Scale(root, length=200, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, label="Turbine Valve", command=lambda val: setattr(turbine, 'valve', float(val)))
    turbine_valve_scale.place(x=250, y=80)

    def refresh():
        update_status()
        status_label.config(text=f"Reactor {reactor.status}")
        temp_label.config(text=f"Temperature: {reactor.temperature:.1f}°C")
        power_label.config(text=f"Power Output: {reactor.powerOutput:.0f} MW")
        rod_label.config(text=f"Control Rod Position: {int(reactor.controlRodPosition)}%")
        rod_movement_label.config(text=f"Control Rod Movement: {reactor.rodMovementRate}")
        pump_label.config(text=f"Pumps A/B: {"1" if reactor.pumpA else "0"}/{"1" if reactor.pumpB else "0"}")
        turbine_rpm_label.config(text=f"Turbine RPM: {turbine.rpm:.0f}")
        turbine_power_label.config(text=f"Turbine Power Output: {turbine.powerOutput:.2f} MW")
        turbine_valve_label.config(text=f"Turbine Valve Position: {turbine.valve*100:.0f}%")
        cv_label.config(text=f"Coolant Valve: {"Open" if reactor.cvOpen else "Closed"}")
        root.after(int(1000/framerate), refresh)

    refresh()
    root.geometry("800x600")
    root.mainloop()

def main():
    create_gui()

if __name__ == "__main__":
    main()