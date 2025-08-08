import tkinter as tk
from tkinter import filedialog , messagebox
import subprocess
import os




class PlusPlusEditor:

    #Constructor
    def __init__(self , window):
        self.window = window
        
        self.fontsize = 12
    
        #self.window.geometry("400x400") for fixed Size if you want
        self.window.title("PlusPlus-Editor")
        self.text = tk.Text(window, wrap="word" , font=("Consolas" , self.fontsize))
        self.text.pack(expand=1 , fill = "both")
        self.filename = None
               


        #Creating Menu
        menu = tk.Menu(window)
        file_menu = tk.Menu(menu, tearoff = 0)

        file_menu.add_command(label="New" , command=self.new_file)
        file_menu.add_command(label="Open" , command=self.open_file)
        file_menu.add_command(label="Save" , command=self.save_file)
        file_menu.add_command(label="Compile & Run" , command=self.candr_file)
        menu.add_cascade(label="File" , menu=file_menu)

        window.config(menu = menu)

    
    
    #Function For New File
    def new_file(self):
        self.filename = None
        self.text.delete(1.0 , tk.END)

    #Funtion For Open File
    def open_file(self):
        file = filedialog.askopenfilename(defaultextension=".cpp",
                                          filetypes=[("C++ Files" , "*.cpp")])
        if file:
            self.filename = file # You can add File Name to Title aswell
            with open(file , "r") as f:
                self.text.delete(1.0 , tk.END)
                self.text.insert(tk.END , f.read())
    
    # Saving Files
    def save_file(self):
        if not self.filename:
            self.filename = filedialog.asksaveasfilename(defaultextension=".cpp", filetypes=[("C++ Files" , "*.cpp")])
        
        if self.filename:
            with open(self.filename, "w") as f:
                f.write(self.text.get(1.0 , tk.END))
    
    # Compiling And Running
    def candr_file(self):
        if not self.filename:
            messagebox.showerror("Error", "Save the File Before Compiling")
            return

        self.save_file()

        # Output file depending on OS
        output_file = "a.exe" if os.name == "nt" else "a.out"
        #“If the operating system is Windows (os.name == "nt"), then set output_file to 'a.exe'.
        #Otherwise (Linux/macOS), set output_file to 'a.out'.”

        # Use local MinGW g++ if on Windows
        if os.name == "nt":
            gpp_path = os.path.join("mingw", "bin", "g++.exe")
        else:
            gpp_path = "g++"  # Use system g++ on Linux/macOS

        # Build compile command
        compile_cmd = [gpp_path, self.filename, "-o", output_file]

        try:
            # Compile
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)

            if compile_result.returncode != 0:
                messagebox.showerror("Compilation Error", compile_result.stderr)
            else:
                # Run compiled output
                run_cmd = [output_file] if os.name == "nt" else [f"./{output_file}"]
                run_result = subprocess.run(run_cmd, capture_output=True, text=True)

                # Display output
                output_window = tk.Toplevel(self.window)
                output_window.title("Program Output")
                output_text = tk.Text(output_window)
                output_text.insert(tk.END, run_result.stdout + run_result.stderr)
                output_text.pack()
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":

    window = tk.Tk()
    app = PlusPlusEditor(window)

    window.mainloop()