# GUI - based pipeline

## Docker setup and start

[Link to Docker setup guide](../docker/README.md)

Running the Docker will automatically open the GUI interface, rendering the first few steps of the "running the pipeline" section obsolete.

## Running the pipeline

Using the Docker terminal Ensure you are in the "demo" folder of this repository on your computer, if you are not then use the "cd" command to navigate to the demo folder.

Run the following command to start up the GUI interface: `python a_GUI_main.py`

### How to run the GUIs

Several of the GUIs are quite involved and require following a set of instructions that is not immediatly apparent. [Please consult this guide for guides on how to use the various GUIs](./GUI_guides_v2.md).

## Errors

If the GUI based pipeline does not behave as one would expect in any way, (e.g. running a script does not automatically proceed to the next step, getting stuck anywhere, buttons being unresponsive), please contact Alex Newberry by email at adnewber@ucsd.edu with the issue you are experiencing.

Quick bug fixes:
  - Click the red "x" at the top left of every GUI window. 
  - Click on the terminal window and press "ctrl+c" on the keyboard to end the process. 
  - Click on the terminal window and press "ctrl+z". and then copy, paste, and run the following command in the terminal: `kill %1`
