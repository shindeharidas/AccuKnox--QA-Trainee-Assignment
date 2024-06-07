import psutil

# Define thresholds
CPU_THRESHOLD = 80  # Percentage
MEMORY_THRESHOLD = 80  # Percentage
DISK_THRESHOLD = 80   # Percentage
PROCESS_THRESHOLD = 100  # Number of processes

# Function to check CPU usage
def check_cpu_usage():
    cpu_percent = psutil.cpu_percent(interval=1)
    if cpu_percent > CPU_THRESHOLD:
        print(f"CPU usage is high: {cpu_percent}%")

# Function to check memory usage
def check_memory_usage():
    memory_percent = psutil.virtual_memory().percent
    if memory_percent > MEMORY_THRESHOLD:
        print(f"Memory usage is high: {memory_percent}%")

# Function to check disk space
def check_disk_usage():
    disk_percent = psutil.disk_usage('/').percent
    if disk_percent > DISK_THRESHOLD:
        print(f"Disk space is low: {disk_percent}%")

# Function to check running processes
def check_running_processes():
    processes_count = len(psutil.pids())
    if processes_count > PROCESS_THRESHOLD:
        print(f"Number of running processes is high: {processes_count}")

# Main function
def main():
    check_cpu_usage()
    check_memory_usage()
    check_disk_usage()
    check_running_processes()

if __name__ == "__main__":
    main()
