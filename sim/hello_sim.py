from sim.scheduler import Scheduler

def node_action(name):
    print(f"  --> {name} végrehajtotta a feladatát.")

def start_hello_simulation():
    sch = Scheduler()

    sch.schedule(delay=1.0, callback=lambda _: node_action("Szenzor_1"))
    sch.schedule(delay=2.5, callback=lambda _: node_action("Szenzor_2"))
    sch.schedule(delay=0.5, callback=lambda _: node_action("Gateway"))

    sch.run(until=5.0)

if __name__ == "__main__":
    start_hello_simulation()