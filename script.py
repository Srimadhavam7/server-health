import os
import paramiko
import psutil

# Remote Server Credentials 
REMOTE_HOST = "ssh root@bitnami.com" 
REMOTE_USERNAME = "bitnami"
REMOTE_PASSWORD = "(Ask for a demo key)"

# Thresholds
CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 10
DISK_THRESHOLD = 10

def check_local_health():
    """Check health of the local machine."""
    alerts = []

    print("Checking local system health...")  

    # Get CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"Local CPU usage: {cpu_usage}%")  
    if cpu_usage > CPU_THRESHOLD:
        alerts.append(f"High CPU usage: {cpu_usage}%")

    # Get memory usage
    memory_usage = psutil.virtual_memory().percent
    print(f"Local Memory usage: {memory_usage}%")  
    if memory_usage > MEMORY_THRESHOLD:
        alerts.append(f"High Memory usage: {memory_usage}%")

    # Get disk usage
    disk_usage = psutil.disk_usage('/').percent
    print(f"Local Disk usage: {disk_usage}%")  
    if disk_usage > DISK_THRESHOLD:
        alerts.append(f"High Disk usage: {disk_usage}%")

    if alerts:
        message = "\n".join(alerts)
        print("ALERT:", message)
    else:
        print("Local System health is normal.")

def check_remote_health():
    """Check health of a remote server via SSH."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Establish SSH Connection
        client.connect(REMOTE_HOST, username=REMOTE_USERNAME, password=REMOTE_PASSWORD)

        # Run health check commands on remote server
        _, cpu_stdout, _ = client.exec_command("top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'")
        _, mem_stdout, _ = client.exec_command("free | awk 'FNR == 2 {print $3/$2 * 100}'")
        _, disk_stdout, _ = client.exec_command("df -h / | awk 'FNR == 2 {print $5}'")

        # Read and process outputs
        cpu_usage = float(cpu_stdout.read().decode().strip())
        memory_usage = float(mem_stdout.read().decode().strip())
        disk_usage = float(disk_stdout.read().decode().strip().replace('%', ''))

        alerts = []
        if cpu_usage > CPU_THRESHOLD:
            alerts.append(f"High CPU usage: {cpu_usage}%")
        if memory_usage > MEMORY_THRESHOLD:
            alerts.append(f"High Memory usage: {memory_usage}%")
        if disk_usage > DISK_THRESHOLD:
            alerts.append(f"High Disk usage: {disk_usage}%")

        if alerts:
            message = "\n".join(alerts)
            print("REMOTE ALERT:", message)
        else:
            print("Remote System health is normal.")

    except paramiko.AuthenticationException:
        print("Authentication failed, please verify your credentials.")
    except paramiko.SSHException as sshException:
        print(f"Unable to establish SSH connection: {str(sshException)}")
    except Exception as e:
        print(f"Error connecting to remote server: {str(e)}")
    finally:
        client.close()

# Run both health checks
print("Checking Local System Health...")
check_local_health()
print("\nChecking Remote Server Health...")
check_remote_health()
