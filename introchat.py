'''

Drank from the forbidden chalice for this--an experiment in using chatGPT to code the app.
More work than was worth, especially after the first instruction.

Game creates bilateral matches among an even number of students, where students are simultaneously randomly assigned as buyer and seller in an ultimatum game.

Introduces the notion of unknown buyer value and volume-margin trade-off in negotiation settings.

'''
import tkinter as tk
from tkinter import ttk
import random

class FloatsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Floats and Price Game")

        # Frame for Number of Floats
        self.frame_num_rp = tk.Frame(self.root)
        self.frame_num_rp.pack(pady=10)

        self.label_num_rp = tk.Label(self.frame_num_rp, text="Enter number of floats:")
        self.label_num_rp.pack(side=tk.LEFT)

        self.entry_num_rp = tk.Entry(self.frame_num_rp)
        self.entry_num_rp.pack(side=tk.LEFT)

        self.btn_set_rp = tk.Button(self.frame_num_rp, text="Set", command=self.create_rp_entries)
        self.btn_set_rp.pack(side=tk.LEFT, padx=5)

        # Frame for Float and Price Entries
        self.frame_rp_entries = None
        self.frame_results = None
        self.frame_results = None
        self.canvas = None

        # Store float and price entries
        self.rp_list_entries = []
        self.prices_list_entries = []

    def create_rp_entries(self):
        num_rp = self.entry_num_rp.get()

        # Clear previous entries if they exist
        if self.frame_rp_entries:
            self.frame_rp_entries.destroy()
        if self.frame_results:
            self.frame_results.destroy()

        self.frame_rp_entries = tk.Frame(self.root)
        self.frame_rp_entries.pack(pady=5)

        self.canvas = tk.Canvas(self.frame_rp_entries, width=20, height=20)
        self.canvas.grid(row=0, column=1, rowspan=100)

        try:
            self.num_rp = int(num_rp)
            self.rp_list_entries = []
            self.prices_list_entries = []
            self.results_list_output = []
            self.matches_list_output = []

            # Column titles
            buyer_rp_title = tk.Label(self.frame_rp_entries, text="Buyer RP", font=('Helvetica', 10, 'bold'))
            buyer_rp_title.grid(row=0, column=0)
            posted_price_title = tk.Label(self.frame_rp_entries, text="Posted Price", font=('Helvetica', 10, 'bold'))
            posted_price_title.grid(row=0, column=2)
            matches_title = tk.Label(self.frame_rp_entries, text="Matched", font=('Helvetica', 10, 'bold'))
            matches_title.grid(row=0, column=4)
            profit_title = tk.Label(self.frame_rp_entries, text="Profit", font=('Helvetica', 10, 'bold'))
            profit_title.grid(row=0, column=5)

            for i in range(self.num_rp):
                # Float entry
                float_label = tk.Label(self.frame_rp_entries, text=f"{i+1}:")
                float_label.grid(row=i+1, column=0)

                float_entry = tk.Entry(self.frame_rp_entries)
                float_entry.grid(row=i+1, column=1)
                self.rp_list_entries.append(float_entry)

                # Price entry
                price_label = tk.Label(self.frame_rp_entries, text=f"{i+1}:")
                price_label.grid(row=i+1, column=2)

                price_entry = tk.Entry(self.frame_rp_entries)
                price_entry.grid(row=i+1, column=3)
                self.prices_list_entries.append(price_entry)
                

                matches_label = tk.Label(self.frame_rp_entries, text=' '*15)
                matches_label.grid(row=i+1, column=4, sticky="w")
                self.matches_list_output.append(matches_label)
                
                result_label = tk.Label(self.frame_rp_entries, text=' '*15)
                result_label.grid(row=i+1, column=5, sticky="w")
                self.results_list_output.append(result_label)


        except ValueError:
            print("Please enter a valid number")

        # Button to evaluate prices against floats
        self.btn_submit = tk.Button(self.root, text="Submit", command=self.evaluate_prices)
        self.btn_submit.pack(pady=10)

        # Reset Button
        self.btn_reset = tk.Button(self.root, text="Reset", command=self.reset_entries)
        self.btn_reset.pack(pady=10)

    def evaluate_prices(self):
        # Collect floats from entries
        rp_list = []
        for entry in self.rp_list_entries:
            try:
                rp_list.append(float(entry.get()))
            except ValueError:
                print("Please enter valid floats")
                return

        # Collect prices from entries
        prices_list = []
        for entry in self.prices_list_entries:
            try:
                prices_list.append(float(entry.get()))
            except ValueError:
                print("Please enter valid prices")
                return

        # Randomly choose an entry from rp_list for each price
        results = []
        match_outcomes = []
        matches = random.sample(range(self.num_rp), k = self.num_rp)
        for i, price in enumerate(prices_list):
            chosen_float = rp_list[matches[i]]
            match_outcomes.append(f'Matched with buyer {matches[i]+1}, RP of  {chosen_float}')
            if price > chosen_float:
                results.append("No sale :(")
            else:
                results.append(f"Sale! Profits = {price:.2f}.")

            # Draw arrow between Buyer RP and Posted Price columns
            line_opts = dict(fill='red', width=5)
            sell_posx = 1
            sell_posy = i 
            buy_posx = 4 
            buy_posy = chosen_float 
            self.canvas.create_line(
                    sell_posx,sell_posy, 
                    buy_posx, buy_posy,
                    arrow=tk.LAST, **line_opts)


        # Display results
        for i, result in enumerate(results):
            self.results_list_output[i].config(text=result)
        for i, match in enumerate(match_outcomes):
            self.matches_list_output[i].config(text=match)

    def reset_entries(self):
        self.entry_num_rp.delete(0, tk.END)
        for entry in self.rp_list_entries:
            entry.delete(0, tk.END)
        for entry in self.prices_list_entries:
            entry.delete(0, tk.END)
        for result_label in self.results_list_output:
            result_label.config(text=' '*15)
        for match_label in self.matches_list_output:
            match_label.config(text=' '*15)

if __name__ == "__main__":
    root = tk.Tk()
    app = FloatsApp(root)
    root.mainloop()

