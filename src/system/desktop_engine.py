import subprocess
import os
import webbrowser


class DesktopEngine:

    def __init__(self):
        print("💻 Desktop Engine: READY")

    def execute(self, command):

        if not command:
            return "Please say a command."

        text = command.lower().strip()

        # =========================
        # OPEN YOUTUBE
        # =========================
        if (
            "open youtube" in text
            or "youtube" == text
            or "युट्यूब" in text
            or "यूट्यूब" in text
        ):
            webbrowser.open("https://www.youtube.com")
            return "Opening YouTube."

        # =========================
        # OPEN CHROME
        # =========================
        if (
            "open chrome" in text
            or "chrome" in text
            or "गुगल क्रोम" in text
            or "गूगल क्रोम" in text
            or "क्रोम उघड" in text
            or "क्रोम चालू कर" in text
            or "क्रोम सुरू कर" in text
            or "गुगल क्रोम उघड" in text
            or "गुगल क्रोम ओपन कर" in text
):    
            subprocess.Popen(
                ["cmd", "/c", "start", "", "chrome"],
                shell=False
            )
            return "Opening Google Chrome."

        # =========================
        # OPEN VS CODE
        # =========================
        if (
            "open vs code" in text
            or "open visual studio code" in text
            or "व्हीएस कोड" in text
            or "वीएस कोड" in text
        ):
            subprocess.Popen(
                ["cmd", "/c", "code"],
                shell=False
            )
            return "Opening Visual Studio Code."

        # =========================
        # OPEN NOTEPAD
        # =========================
        if (
            "open notepad" in text
            or "नोटपॅड" in text
            or "नोटपैड" in text
        ):
            subprocess.Popen(
                ["notepad.exe"]
            )
            return "Opening Notepad."

        # =========================
        # OPEN CALCULATOR
        # =========================
        if (
        "open calculator" in text
        or "open calc" in text
        or "calculator" in text
        or "कॅल्क्युलेटर" in text
        or "कॅल्क्युलेटर उघड" in text
        or "कॅल्क्युलेटर चालू कर" in text
        or "कॅल्क्युलेटर सुरू कर" in text
):
            subprocess.Popen(
                ["calc.exe"]
            )
            return "Opening Calculator."

        # =========================
        # FILE EXPLORER
        # =========================
        if (
            "open file explorer" in text
            or "open explorer" in text
            or "file explorer" == text
            or "फाइल एक्सप्लोरर" in text
            or "फाईल एक्सप्लोरर" in text
            or "फोल्डर उघड" in text
        ):
            subprocess.Popen(
                ["explorer.exe"]
            )
            return "Opening File Explorer."

        # =========================
        # SHOW DESKTOP
        # =========================
        if (
            "show desktop" in text
            or "डेस्कटॉप दाखव" in text
            or "डेस्कटॉप दाखवा" in text
        ):
            subprocess.Popen([
                "powershell",
                "-Command",
                "(New-Object -ComObject Shell.Application).MinimizeAll()"
            ])
            return "Showing desktop."

        # =========================
        # SYSTEM INFO
        # =========================
        if (
            "system information" in text
            or "system info" in text
            or "सिस्टम माहिती" in text
            or "सिस्टम इन्फो" in text
        ):
            return (
                f"Computer: "
                f"{os.environ.get('COMPUTERNAME', 'Unknown')}"
            )

        # =========================
        # GOOGLE PLAY STORE
        # =========================
        if (
            "open play store" in text
            or "open google play store" in text
            or "launch play store" in text
            or "प्ले स्टोअर उघड" in text
            or "प्ले स्टोअर चालू कर" in text
            or "प्ले स्टोअर सुरू कर" in text
            or "गुगल प्ले स्टोअर उघड" in text
        ):
            subprocess.Popen(
                [
                    "cmd",
                    "/c",
                    "start",
                    "",
                    "https://play.google.com/store"
                ]
            )
            return "Opening Google Play Store."

        return None
            # =========================
        # OPEN YOUTUBE
        # =========================
        if (
            "open youtube" in text
            or "youtube" == text
            or "युट्यूब उघड" in text
            or "यूट्यूब उघड" in text
            or "युट्यूब चालू कर" in text
            or "यूट्यूब चालू कर" in text
            or "युट्यूब सुरू कर" in text
        ):
            webbrowser.open("https://www.youtube.com")
            return "Opening YouTube."

if __name__ == "__main__":

    engine = DesktopEngine()

    print()
    print("Desktop Engine Test")
    print("-------------------")

    while True:

        command = input("Command: ").strip()

        if command.lower() in {
            "exit",
            "quit"
        }:
            break

        result = engine.execute(command)

        if result:
            print("AURA:", result)
        else:
            print("AURA: Command not supported.")
