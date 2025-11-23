"""
Real-time training monitor
Shows progress, ETA, and loss curves
"""
import os
import re
import time
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import deque

# Configuration
LOG_FILE = "training.log"
REFRESH_INTERVAL = 5  # seconds
MAX_POINTS = 100  # points to show on graph

class TrainingMonitor:
    def __init__(self):
        self.losses = deque(maxlen=MAX_POINTS)
        self.steps = deque(maxlen=MAX_POINTS)
        self.start_time = None
        self.current_epoch = 0
        self.current_step = 0
        self.total_epochs = 60
        self.steps_per_epoch = 1000
        self.total_steps = self.total_epochs * self.steps_per_epoch
        
        # Setup plot
        plt.ion()
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(10, 8))
        self.fig.suptitle('Training Monitor', fontsize=16, fontweight='bold')
        
    def parse_log_line(self, line):
        """Extract metrics from log line"""
        # Match pattern like: "123/Unknown - 145s 1s/step - loss: 975.7608"
        match = re.search(r'(\d+)/Unknown.*?loss:\s*([\d.]+)', line)
        if match:
            step = int(match.group(1))
            loss = float(match.group(2))
            return step, loss
        return None, None
    
    def calculate_eta(self, elapsed_seconds, completed_steps):
        """Calculate estimated time remaining"""
        if completed_steps == 0:
            return "Calculating..."
        
        seconds_per_step = elapsed_seconds / completed_steps
        remaining_steps = self.total_steps - completed_steps
        remaining_seconds = seconds_per_step * remaining_steps
        
        eta = timedelta(seconds=int(remaining_seconds))
        return str(eta)
    
    def update_display(self):
        """Update the real-time display"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("="*80)
        print("TRAINING MONITOR - Real-time Progress")
        print("="*80)
        
        if self.start_time:
            elapsed = datetime.now() - self.start_time
            elapsed_str = str(elapsed).split('.')[0]
        else:
            elapsed_str = "00:00:00"
            elapsed = timedelta(0)
        
        total_completed = (self.current_epoch - 1) * self.steps_per_epoch + self.current_step
        progress_pct = (total_completed / self.total_steps) * 100
        
        print(f"\nEpoch: {self.current_epoch}/{self.total_epochs}")
        print(f"Step: {self.current_step}/{self.steps_per_epoch}")
        print(f"Overall Progress: {total_completed}/{self.total_steps} ({progress_pct:.2f}%)")
        
        # Progress bar
        bar_length = 50
        filled = int(bar_length * progress_pct / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"[{bar}] {progress_pct:.1f}%")
        
        print(f"\nElapsed Time: {elapsed_str}")
        
        if total_completed > 0:
            eta = self.calculate_eta(elapsed.total_seconds(), total_completed)
            print(f"Estimated Time Remaining: {eta}")
        
        if self.losses:
            current_loss = self.losses[-1]
            avg_loss = sum(self.losses) / len(self.losses)
            print(f"\nCurrent Loss: {current_loss:.2f}")
            print(f"Average Loss (last {len(self.losses)} steps): {avg_loss:.2f}")
        
        print("\n" + "="*80)
        print("Press Ctrl+C to stop monitoring (training will continue)")
        print("="*80)
    
    def update_plot(self):
        """Update loss curve plot"""
        if len(self.steps) < 2:
            return
        
        # Clear previous plots
        self.ax1.clear()
        self.ax2.clear()
        
        # Plot 1: Loss over steps
        self.ax1.plot(list(self.steps), list(self.losses), 'b-', linewidth=2)
        self.ax1.set_xlabel('Step', fontweight='bold')
        self.ax1.set_ylabel('Loss', fontweight='bold')
        self.ax1.set_title('Training Loss', fontweight='bold')
        self.ax1.grid(True, alpha=0.3)
        
        # Plot 2: Loss trend (smoothed)
        if len(self.losses) > 10:
            window = min(20, len(self.losses))
            smoothed = []
            for i in range(len(self.losses)):
                start = max(0, i - window + 1)
                smoothed.append(sum(list(self.losses)[start:i+1]) / (i - start + 1))
            
            self.ax2.plot(list(self.steps), smoothed, 'r-', linewidth=2, label='Smoothed')
            self.ax2.plot(list(self.steps), list(self.losses), 'b-', alpha=0.3, linewidth=1, label='Raw')
            self.ax2.set_xlabel('Step', fontweight='bold')
            self.ax2.set_ylabel('Loss', fontweight='bold')
            self.ax2.set_title('Loss Trend (Smoothed)', fontweight='bold')
            self.ax2.legend()
            self.ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.pause(0.01)
    
    def monitor(self):
        """Main monitoring loop"""
        print("Starting training monitor...")
        print("Looking for training output...")
        
        last_position = 0
        
        try:
            while True:
                # Read new lines from process output
                # Since we can't directly read from the process, we'll check for updates
                time.sleep(REFRESH_INTERVAL)
                
                # For now, just update display with current info
                self.update_display()
                self.update_plot()
                
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped. Training continues in background.")
            plt.close()

if __name__ == "__main__":
    monitor = TrainingMonitor()
    
    print("="*80)
    print("TRAINING MONITOR")
    print("="*80)
    print("\nThis monitor will show real-time training progress.")
    print("Note: Currently displays static info. For live updates,")
    print("training output needs to be logged to a file.")
    print("\nStarting in 3 seconds...")
    time.sleep(3)
    
    monitor.monitor()
