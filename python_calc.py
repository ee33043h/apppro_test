import PySimpleGUI as sg


def format_number():
    return  float("".join(var["front"]) + "." + "".join(var["back"]) )
 
def update_display(display_value):
    try:
         window["_DISPLAY_"].update( value ="{:,.4f}".format(display_value) )
    except:
         window["_DISPLAY_"].update( value = display_value )
 
def number_click(event):    
    global var
    if event in ["0","1","2","3","4","5","6","7","8","9"]:  
        if var["decimal"] == True:
            var["front"].append(event)
        else:
            var["back"].append(event)
        update_display(format_number())   
 
def decimal_click(event):
    global var
    if event in [".",","]:
        var["decimal"] = False
 
def operator_click(event):
    global var
    if event in ["+","-","*","/","%"]:
        var["operator"] = event
        var["x_val"] =  format_number()
        clear_click()
 
def clear_click():  
    global var
    var["front"].clear()
    var["back"].clear()
    var["decimal"]=True
    var["result"]=0.0
    update_display(var["result"]) 

def calculate_click():
    global var
    var["y_val"] = format_number()
    var['result'] = eval(str(var['x_val']) + var['operator'] + str(var['y_val']))
    update_display(var["result"]) 


#
# Main 関数
#
if __name__ == "__main__":
    
    layout = [[sg.Text("0.0000",key="_DISPLAY_",size=(30, 1))],
            [sg.Button("7",key="7",size=(3, 1)),sg.Button("8",key="8",size=(3, 1)), sg.Button("9",key="9",size=(3, 1)), sg.Button("/",key="/",size=(3, 1))], 
            [sg.Button("4",key="4",size=(3, 1)),sg.Button("5",key="5",size=(3, 1)), sg.Button("6",key="6",size=(3, 1)), sg.Button("*",key="*",size=(3, 1))],
            [sg.Button("1",key="1",size=(3, 1)),sg.Button("2",key="2",size=(3, 1)), sg.Button("3",key="3",size=(3, 1)), sg.Button("+",key="+",size=(3, 1))],
            [sg.Button("0",key="0",size=(3, 1)),sg.Button(".",key=".",size=(3, 1)), sg.Button("-",key="-",size=(3, 1)), sg.Button("calc",key="calc",size=(3, 1))]
            ]
    window = sg.Window("簡単電卓",layout,size=(200,200), background_color="#272533",
                    return_keyboard_events=True)
    var = {"front":[],"back":[],"decimal":True,
        "x_val":0.0,"y_val":0.0,"result":0.0,"operator":"+"}
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event in ['=',"calc"]:
            calculate_click()

        if event in ["C","CE"]:
            clear_click()
        number_click(event)
        decimal_click(event)
        operator_click(event) 
    window.close()
