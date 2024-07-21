import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import scapy.all as scapy

class PacketSnifferGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Packet Sniffer")
        self.root.geometry("800x600")

        self.create_widgets()
        self.style_widgets()

        self.sniffer_thread = None
        self.running = False

    def create_widgets(self):
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.start_button = tk.Button(self.root, text="Start Sniffing", command=self.start_sniffing)
        self.start_button.pack(pady=10, side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(self.root, text="Stop Sniffing", command=self.stop_sniffing, state=tk.DISABLED)
        self.stop_button.pack(pady=10, side=tk.LEFT, padx=10)

        self.info_frame = tk.LabelFrame(self.root, text="Packet Information", padx=10, pady=10)
        self.info_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.source_ip_label = tk.Label(self.info_frame, text="Source IP:")
        self.source_ip_label.pack(anchor=tk.W)

        self.dest_ip_label = tk.Label(self.info_frame, text="Destination IP:")
        self.dest_ip_label.pack(anchor=tk.W)

        self.protocol_label = tk.Label(self.info_frame, text="Protocol:")
        self.protocol_label.pack(anchor=tk.W)

        self.payload_label = tk.Label(self.info_frame, text="Payload:")
        self.payload_label.pack(anchor=tk.W)

    def style_widgets(self):
        self.text_area.config(font=("Arial", 12))
        self.start_button.config(font=("Arial", 12), width=15)
        self.stop_button.config(font=("Arial", 12), width=15)
        self.source_ip_label.config(font=("Arial", 12))
        self.dest_ip_label.config(font=("Arial", 12))
        self.protocol_label.config(font=("Arial", 12))
        self.payload_label.config(font=("Arial", 12))
        self.info_frame.config(font=("Arial", 12))

    def packet_callback(self, packet):
        if packet.haslayer(scapy.IP):
            ip_src = packet[scapy.IP].src
            ip_dst = packet[scapy.IP].dst
            protocol = packet[scapy.IP].proto
            length = len(packet)

            info = f"IP Source: {ip_src}\nIP Destination: {ip_dst}\nProtocol: {protocol}\nLength: {length}\n"
            self.text_area.insert(tk.END, info)

            self.source_ip_label.config(text=f"Source IP: {ip_src}")
            self.dest_ip_label.config(text=f"Destination IP: {ip_dst}")
            self.protocol_label.config(text=f"Protocol: {protocol}")

            if packet.haslayer(scapy.Raw):
                payload = packet[scapy.Raw].load
                payload_info = f"Payload: {payload.hex()}\n"
                self.text_area.insert(tk.END, payload_info)

                self.payload_label.config(text=f"Payload: {payload.hex()}")

    def start_sniffing(self):
        if not self.running:
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

            self.sniffer_thread = threading.Thread(target=self.sniff_packets)
            self.sniffer_thread.start()
        else:
            messagebox.showinfo("Info", "Sniffing is already running.")

    def stop_sniffing(self):
        if self.running:
            self.running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

            if self.sniffer_thread and self.sniffer_thread.is_alive():
                self.sniffer_thread.join(timeout=1.0)  # Wait for thread to join with timeout
        else:
            messagebox.showinfo("Info", "Sniffing is not running.")

    def sniff_packets(self):
        while self.running:
            try:
                scapy.sniff(prn=self.packet_callback, store=False, timeout=1.0)
            except Exception as e:
                print(f"Error occurred in sniff_packets: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PacketSnifferGUI(root)
    root.mainloop()
