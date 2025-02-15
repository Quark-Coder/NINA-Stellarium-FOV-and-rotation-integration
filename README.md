# NINA-Stellarium-FOV-and-rotation-integration
This script allows you to transfer FOV and camera rotation directly to Stellarium in real time.

## Installation
Download this script and requirements.txt

Install [Python 3.12.7](https://www.python.org/downloads/release/python-3127/)

Run this command
```
pip install requirements.txt
```
Open NINA plugin manager and install Advanced API plugin.
Enable the two functions shown in the image. Make sure that the port is 1888:

![NINA_f90cC7Ki0k](https://github.com/user-attachments/assets/2f6436b9-37eb-4947-8f25-9bb4af2db9a9)

Install the [ASCOM](https://ascom-standards.org/Downloads/Index.htm)  driver if it is not already installed.

Enable Oculars, Telescope Control and Remote Control

![stellarium_jcbXlDSCY8](https://github.com/user-attachments/assets/d1e86ee2-c522-49a6-9e73-ecf6b1fad407)

Add your telescope and camera to the Oculars plugin. Remember their numbers.

To display the angles correctly, select the Equatorial mount in the telescope.
![stellarium_W7QlqQfAi3](https://github.com/user-attachments/assets/25ec7e4f-927b-4279-835c-6e4f7b242ec2)


Add new telescope to the Telescope Control plugin.

![stellarium_5Io796adL4](https://github.com/user-attachments/assets/970e5769-5fad-4f36-8dae-dcf3227a270a)
![stellarium_1AkYaMZhJC](https://github.com/user-attachments/assets/a2ed0899-1fb7-4c3e-84e0-6078f1d1a35c)

If you can't connect the mount to your computer, select telescope simulator:

![stellarium_KRqJP4QLZX](https://github.com/user-attachments/assets/ad3b1f4b-e3fc-481f-9ad0-43b5064100fe)

Right-click on the Remote Control Plugin

![stellarium_lkG7aN0TF6](https://github.com/user-attachments/assets/b0aa4dac-9ccb-4244-bd2e-602de582654f)
![stellarium_6BbMKF2yEc](https://github.com/user-attachments/assets/36f34d38-5fed-4797-a706-7d900dcb30ec)

## How to use it
Connect your telescope

![stellarium_R03TljSNTU](https://github.com/user-attachments/assets/a2922e08-70c2-4c60-b0f5-a944dff21b83)

Open NINA. Connect your camera, mount and rotator. If you do not have a rotator, the mount cannot be connected to a PC - select simulators:

![NINA_5W47cht3F2](https://github.com/user-attachments/assets/90c73c90-3616-4ba4-b755-4ff11f0105a1)
![NINA_3pjaRcezBj](https://github.com/user-attachments/assets/c4d5ffc0-e10e-4a60-95bc-c13da265925c)

After connecting the telescope simulator, turn on tracking:

![NINA_OPbrEg6OP4](https://github.com/user-attachments/assets/9863f765-4b5a-467f-9f04-abf0ea52d852)

Create an advanced sequence platesolver:

![NINA_s4rvWIchpr](https://github.com/user-attachments/assets/b279697e-f179-46ff-b47a-c61b9ff35d71)

Run this sequence and then run the script.
Remember the telescope number in Telescope Control, Oculars, and your camera number. Enter these values in the console. After restarting, these values are saved in config.json, where they can be changed.

![python_xzGPRmyQw2](https://github.com/user-attachments/assets/a758758a-224d-4aaf-b947-f95bf7ca26e0)

Now the script will automatically get the angle from platesolve, and telescope control will take the values of RA and DEC.
If you accidentally shifted the camera, press F and re-centering will occur.
To stop the script, press ESC.








