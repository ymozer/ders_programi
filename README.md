# ADÜ Ders Programı Windows Bildirim Yazılımı

For Aydın Adnan Menderes University students. This program creates a toast notification on 'WINDOWS' machine before lesson starts. You need to download your syllabus (ders programı) from OBIS as XML file format. 
'/ouput' folder contains executable file. You need to put syllabus at the same directory as executable. There is no terminal output for now. (I don't think we need it.)
Once you started exe it will be run until you stop it from "Task Manager". But I would'nt bother cause program uses 'sched' module, means there is a lot of resting room. RAM usage is minimal. It can be run on the background while you doing your thing (as intended).

If you want to run this program when pc starts, you can do following:
* Enter 'WIN+R' then type 'shell:startup'
* Create shortcut of an executable
* Move the shortcut to the startup folder that opened after first step
* Done

Be sure not to move XML file to startup. Keep those to wherever but keep 'em together.



## Installation for Development
'''bash
python -m venv .                  # Create Virtual Environment
.\Scripts\Activate.ps1            # Activate it
pip install -r .\requirements.txt #`install dependencies
'''
