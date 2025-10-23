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
    status_label = tk.Label(root, text="Reactor Status")
    status_label.place(x=0, y=0)

    temp_label = tk.Label(root, text="Temperature: 0°C")
    temp_label.place(x=0, y=20)

    power_label = tk.Label(root, text="Power Output: 0 MW")
    power_label.place(x=0, y=40)

    rod_label = tk.Label(root, text="Control Rod Position: 0%")
    rod_label.place(x=0, y=60)

    cv_label = tk.Label(root, text="Coolant Valve: Open")
    cv_label.place(x=150, y=60)

    ignition_button = tk.Button(root, text="Toggle Reactor", command=lambda: reactor.toggle_reactor())
    ignition_button.place(x=0, y=80)

    rod_up_button = tk.Button(root, text="Start Raising Control Rods", command=lambda: reactor.toggle_move_rods_down())
    rod_up_button.place(x=0, y=105)

    rod_down_button = tk.Button(root, text="Start Lowering Control Rods", command=lambda: reactor.toggle_move_rods_up())
    rod_down_button.place(x=0, y=130)

    coolant_valve_button = tk.Button(root, text="Open/Close Coolant Valve",  command=lambda: reactor.toggle_coolant_valve())
    coolant_valve_button.place(x=0, y=155)

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
        turbine_rpm_label.config(text=f"Turbine RPM: {turbine.rpm:.0f}")
        turbine_power_label.config(text=f"Turbine Power Output: {turbine.powerOutput:.2f} MW")
        turbine_valve_label.config(text=f"Turbine Valve Position: {turbine.valve*100:.0f}%")
        cv_label.config(text=f"Coolant Valve: {"Open" if reactor.cvOpen else "Closed"}")
        root.after(int(1000/framerate), refresh)

    refresh()
    root.geometry("800x600")
    root.mainloop()

create_gui()