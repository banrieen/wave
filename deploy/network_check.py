import subprocess




def lan_ping(network: str, mask: int=24):
    for i in range(1,255):
        addr = ".".join([network, str(i)])
        cmd = f"ping {addr}"
        returned_value = subprocess.call(cmd, shell=True)  # returns the exit code in unix
        print('returned value:', returned_value)

lan_ping("192.168.1", mask=24)

