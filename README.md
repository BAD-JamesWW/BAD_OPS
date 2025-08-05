
<img width="1024" height="1024" alt="CompanyLogo" src="https://github.com/user-attachments/assets/77a92ff5-eeda-4082-829f-95346fb1cd6f" />

# **O.P.S. — Operational Preparedness System**

## Company & Legal Information

O.P.S. is developed and owned by B.A.D. Black Apex Development LLC — a registered business entity in the State of Ohio (Entity #5448030).  
Trademark rights are claimed under common law.  
All rights reserved.

© 2025 B.A.D. Black Apex Development LLC.  
This software, its name, and associated brand elements are the intellectual property of B.A.D. Black Apex Development LLC.  
Unauthorized reproduction, modification, distribution, or use of this project, its name, or associated branding without express written permission is strictly prohibited and may violate copyright, trademark, and unfair competition laws.


**O.P.S.** is a modular, real‑time training tool designed to enhance deployment efficiency for individuals and small teams.  
Its primary goal is to allow users to train deployment times with any piece of gear where speed is paramount. Logged sessions allow you to track deployment speeds over time and view your current average speed via an integrated graph.

---

## Acknowledgements
This project uses:
- [Dear PyGui](https://github.com/hoffstadt/DearPyGui) — Licensed under the MIT License
- [Vosk Speech Recognition Toolkit](https://alphacephei.com/vosk/) — Licensed under the Apache License 2.0
- [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/) — Licensed under the MIT License

---

## **Features**
- Add, remove, or clear all gear entries
- Train with voice‑controlled timing and logging
- Log successful deployments or fumbles "Eighty-Six's"
- Track deployment speed history
- View current average deployment speed in graph form

---

## **How to Use**

### **Installation & Execution**
**Supported Systems**: Windows 11
- **Run the update.bat**: Open a terminal in the O.P.S. main directory and run the "update.bat" file.
- **Run the run.bat**: Open a terminal in the O.P.S. main directory and run the "run.bat" file.
- Now unless an update happens, you can just run "run.bat" to execute O.P.S.

### **Home Screen**
- **Add**: Add a gear entry to the list.
- **Remove**: Remove a selected gear entry.
- **Nuke**: Remove all gear entries.
- **Train**: Select a gear item and begin a training session.
- **Set Reps**: Configure the number of repetitions before starting a session.

---

### **Starting a Training Session**
1. Click **Start Session (Voice‑Controlled)**.
2. Follow the voice prompts:
   - Program says: `Ready` → User responds: `Ready`
     - Program replies: `Ten-Four` (acknowledgment)
   - Program waits a random 1–2 seconds, giving a beep for each second.
   - Program says: `Deploy`
   - User options:
     - Say `Stop` → Timer stops, time is logged. Program replies: `Heard`.
     - Say `Eighty-Six` → Marks deployment as an Eighty-Six. Program replies: `Heard`.

---

### **Stopping Training**
- To end a session without logging data, click **Stop Training (No Log)**.

---

### **Tracking Performance**
- Click **Graph** to view:
  - Deployment speed history over time
  - Current average deployment speed

---

## **Planned Use Cases**
- Civilian and emergency deployment training
- Tactical gear readiness practice
- Time‑critical tool deployment simulations

---
