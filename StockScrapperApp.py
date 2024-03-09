import tkinter as tk
from StockScrapper import StockScrapper
import time
import json
import os


def save_json(response, fname):
    response_json = json.dumps(response)
    with open(fname, 'w') as f:
        f.write(response_json)

class StockScrapperApp:
    def __init__(self):
        self.driver = StockScrapper()
        self.wait_time = 20

        self.window = tk.Tk()
        self.window.title("StockScrapper")
        self.window.resizable(width=0, height=0)
        
        self.input_frame = tk.Frame(self.window)
        self.input_frame.pack(padx=10, pady=10)
        
        self.label = tk.Label(self.input_frame, text="Symbol:")
        self.label.grid(row=0, column=0, padx=5, pady=5)
        
        self.symbol = tk.StringVar(self.window)
        self.symbol_entry = tk.Entry(self.input_frame, textvariable=self.symbol)
        self.symbol_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.button = tk.Button(self.input_frame, text="Search", command=self.search)
        self.button.grid(row=0, column=2, padx=5, pady=5)
        
        self.output = tk.Text(self.window, state="disabled", height=8, width=50)
        self.output.pack(pady=10)
    
    def promt(self, msg):
        self.output.configure(state='normal')
        self.output.insert(1.0, msg)
        self.output.configure(state='disabled')

    def search(self):
        symbol = self.symbol.get()
        response = self.driver.scrap(symbol)
        if response=="ERROR1":
            self.promt(f"ERROR: Unknown symbol {symbol}\n")
        elif response=="ERROR2":
            self.promt(f"ERROR: Connection problems... Restarting kernel\n")
            self.driver.initialize_driver()
        else:
            self.promt(f"Scrapped {symbol} data\n")
            save_json(response, f"{symbol}.json")        
        time.sleep(self.wait_time)

    def run(self):
        self.window.mainloop()

if __name__=="__main__":
    app = StockScrapperApp()
    app.run()