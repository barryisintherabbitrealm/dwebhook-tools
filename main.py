#!/usr/bin/python3
# Import some critical libraries
import os
import sys
# Make an attempt at importing some other libraries needed.
# This is inside of a try except block as not all computers may have these
# modules installed.
try:
    import discord
    if len(sys.argv) > 1:
        if sys.argv[1] == "--use-qt":
            import PySimpleGUIQt as sg
        else:
            import PySimpleGUIQt
    else:
        import PySimpleGUI as sg
    from discord import SyncWebhook
except ImportError as e:
    print("One or more modules cannot be imported correctly. Please make sure that all required dependencies are installed. (Check requirements.txt)")
    print(e)
    
    os.system("kdialog --title 'dwebhook-tools' --detailederror 'An error has occured, and the program must be stopped'" + " '" + str(e) + "'")
    exit()
    
# Set the theme
sg.theme("SystemDefaultforReal")

# Create the main layout
main_layout = [
    [sg.Text("Discord Webhook Tools")],
    [sg.Text("Webhook URL:"), sg.InputText(key="-webhook_url-"), sg.Button("Sync")],
    [sg.Text("Message Text:"), sg.InputText(key="-msg_text-"), sg.Button("Send")],
    [sg.Text("Other Tools:"), sg.Button("Delete")],
    [sg.Text("Are you sure?", key="-yousure-", visible=False), sg.Button("Yes", key="-delyes-", visible=False), sg.Button("No", key="-delno-", visible=False)],
    [sg.Text("Window Title:"), sg.InputText(key="-wintitle-"), sg.Button("Apply")],
    [sg.Button("Close"), sg.Button("Clear")]
    ]

# Create the main window
window = sg.Window("dwebhook-tools", main_layout)

while True:
    event, values = window.read();
    
    if event == "Sync":
        print("Attempting to sync with webhook")
        try:
            webhook = SyncWebhook.from_url(values["-webhook_url-"])
            os.system("notify-send -a '' 'dwebhook-tools' 'Webhook synced!!'")
        except Exception as e:
            os.system("kdialog --title 'dwebhook-tools' --detailedsorry 'An error has occured...'" + " '" + str(e) + "'")
            print("An error has occured. The program is able to continue")
            print(e)
            
    if event == "Send":
        print("Attempting to send message with synced webhook")
        try:
            webhook.send(values["-msg_text-"])
            os.system("notify-send -a '' 'dwebhook-tools' 'Webhook message sent!'")
        except Exception as e:
            print("An error has occured. The program is able to continue")
            print(e)
            
            if str(e) == "name 'webhook' is not defined":
                os.system("kdialog --title 'dwebhook-tools' --sorry 'You must sync to a webhook first before sending a message'")
            else:
                os.system("kdialog --title 'dwebhook-tools' --detailedsorry 'An error has occured...'" + " '" + str(e) + "'")
    
    if event == "-delyes-":
        print("Attempting to delete synced webhook")
        try:
            webhook.delete()
            os.system("notify-send -a '' 'dwebhook-tools' 'Webhook deleted!'")
            window["-yousure-"].update(visible=False)
            window["-delno-"].update(visible=False)
            window["-delyes-"].update(visible=False)
        except Exception as e:
            print("An error has occured. The program is able to continue")
            print(e)
            
            if str(e) == "name 'webhook' is not defined":
                os.system("kdialog --title 'dwebhook-tools' --sorry 'You must sync to a webhook first before deleting it'")
            else:
                os.system("kdialog --title 'dwebhook-tools' --detailedsorry 'An error has occured...'" + " '" + str(e) + "'")
    if event == "-delno-":
        window["-yousure-"].update(visible=False)
        window["-delno-"].update(visible=False)
        window["-delyes-"].update(visible=False)
        
    if event == "Delete":
        window["-yousure-"].update(visible=True)
        window["-delno-"].update(visible=True)
        window["-delyes-"].update(visible=True)
                
    if event == "Clear":
        window["-webhook_url-"].update("")
        window["-msg_text-"].update("")
        
    if event == "Apply":
        try:
            window.TKroot.title(values["-wintitle-"])
        except:
            pass
    
    
    if event == sg.WIN_CLOSED or event == "Close" or event == "Exit":
        break
        
# Close the window
window.close()
exit()
