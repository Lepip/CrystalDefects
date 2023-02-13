# Crystal defects detector

Detection of defects in scans of crystals.

The project is thought to be a command-line utility 
or a python library to be integrated.
## Usage  

Python required. Install ``requirments.txt``. Used libraries:  

1. opencv-python
2. numpy
3. tdqm  

Right now GUI mode is supported, but not polished. 
To start the program in GUI mode run  
```python
import cv_crystall

cv_crystall.windowed_mode('path_to_your_image')
```
This code is present in ``start.py``.  
Sliders:
- ``step``: A number of pixels to skip during edge detection 
(the bigger the step - the less resolution edge detection has).
- ``border_crop``: How many pixels to ignore on borders.
- ``corner_crop``: How many pixels to ignore in corners.
- ``defect_size``: How large are the defect's borders.
(it's usually 17, which corresponds to the defect_size of 8).  
Affects the size of the Sobel kernel.
- ``sens_mult``: Sensitivity multiplier, 
affects the sensitivity of detector by multiplying strength of its output.
The value used is divided by 10 due to discrete sliders.
- ``sens_lvl``: Sensitivity level, affects the function used to decide what is 
and what isn't a defect. The deviation is scaled from 0 to 1 and raised in power of (sens_lvl/10). For example, if the sensitivity lvl is at 2, it's quadratic. 
If it's one, it is linear. The value used is divided by 10 due to discrete sliders.
- ``Proceed``: If set to 1 starts the algorithm with set parameters.
- ``Save``: If set to 1 saves the image displayed below the sliders in the current running derictory (in real resolution, not the distorted one).
- ``postprocess``: If set to 1 applies postprocessor to the detected defects when proceeded, 
otherwise doesn't.

To use the program in the inline mode use
```python
import cv_crystall

cv_crystall.process_image('path_to_your_image', args)
```
Where ``args`` is a dictionary of arguments (similar to described above, the exact description right 
now is in ``cv_crystall\sobel_technique.py``).
