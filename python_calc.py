import PySimpleGUI as sg
import math

def format_number():
    """Convert the stored number lists into a floating-point number."""
    if not var["front"]:
        return 0.0
    num_str = "".join(var["front"])
    if not var["decimal"]:
        num_str += "." + "".join(var["back"])
    return float(num_str)

def update_display(display_value):
    """Update the display with formatted output."""
    try:
        window["_DISPLAY_"].update(value="{:,.4f}".format(display_value))
    except:
        window["_DISPLAY_"].update(value=display_value)

def number_click(event):
    """Handle number button clicks."""
    global var
    if event in "0123456789":
        if var["decimal"]:
            var["front"].append(event)
        else:
            var["back"].append(event)
        update_display(format_number())

def decimal_click(event):
    """Handle decimal point click."""
    global var
    if event in [".", ","] and var["decimal"]:  # Allow decimal only once
        var["decimal"] = False

def operator_click(event):
    """Handle operator button clicks."""
    global var
    if event in ["+", "-", "*", "/", "%"]:
        var["operator"] = event
        var["x_val"] = format_number()
        clear_entry()
        
def clear_click():
    """Clear all values."""
    global var
    var["front"].clear()
    var["back"].clear()
    var["decimal"] = True
    var["result"] = 0.0
    var["x_val"] = 0.0
    var["y_val"] = 0.0
    update_display(var["result"])

def clear_entry():
    """Clear only the last entered number."""
    global var
    var["front"].clear()
    var["back"].clear()
    var["decimal"] = True
    update_display(0.0)

def calculate_click():
    """Perform the calculation."""
    global var
    try:
        var["y_val"] = format_number()
        if var["operator"] == "/" and var["y_val"] == 0:
            update_display("Error: Div by 0")
            return
        var["result"] = eval(f"{var['x_val']} {var['operator']} {var['y_val']}")
        update_display(var["result"])
        var["x_val"] = var["result"]  # Store result for next operation
        clear_entry()
    except Exception as e:
        update_display("Error")

def trig_function(event):
    """Handle trigonometric functions (sin, cos, tan)."""
    global var
    try:
        angle = format_number()
        radians = math.radians(angle)  # Convert degrees to radians
        
        if event == "sin":
            result = math.sin(radians)
        elif event == "cos":
            result = math.cos(radians)
        elif event == "tan":
            if (angle % 180) == 90:  # tan(90°), tan(270°) などの無限大エラー防止
                update_display("Error: Undefined")
                return
            result = math.tan(radians)

        var["result"] = result
        update_display(var["result"])
        clear_entry()
    except Exception as e:
        update_display("Error")

# GUI Layout
layout = [
    [sg.Text("0.0000", key="_DISPLAY_", size=(30, 1))],
    [sg.Button("7"), sg.Button("8"), sg.Button("9"), sg.Button("/")], 
    [sg.Button("4"), sg.Button("5"), sg.Button("6"), sg.Button("*")],
    [sg.Button("1"), sg.Button("2"), sg.Button("3"), sg.Button("+")],
    [sg.Button("0"), sg.Button("."), sg.Button("-", size=(3, 1)), sg.Button("calc", size=(6, 1))],
    [sg.Button("C", size=(6, 1)), sg.Button("CE", size=(6, 1))],
    [sg.Button("sin"), sg.Button("cos"), sg.Button("tan")]
]

window = sg.Window("簡単電卓", layout, background_color="#272533")

# Variable Storage
var = {"front": [], "back": [], "decimal": True, "x_val": 0.0, "y_val": 0.0, "result": 0.0, "operator": "+"}

while True:
    event, _ = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event in ["=", "calc"]:
        calculate_click()
    elif event == "C":
        clear_click()
    elif event == "CE":
        clear_entry()
    elif event in "0123456789":
        number_click(event)
    elif event in [".", ","]:
        decimal_click(event)
    elif event in ["+", "-", "*", "/", "%"]:
        operator_click(event)
    elif event in ["sin", "cos", "tan"]:
        trig_function(event)

window.close()
