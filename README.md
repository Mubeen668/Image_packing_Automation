Image Packing on PDF - Python Automation Task


Project Overview:

This project implements a Python program to pack a set of images of various sizes and shapes into a PDF file while minimizing the total space used and preserving each image's original aspect ratio. The goal is to arrange images efficiently on A4-sized pages and generate a clean PDF output.


Setup Instructions:

Clone the repository or download the ZIP and extract it locally.

Created and activate a Python virtual environment:

--- python -m venv env

--- env\\Scripts\\activate  # For Windows


Installed required dependencies:

--- pip install Pillow reportlab


Generating Sample Images

Run the script to generate sample transparent images with random shapes in the input\_images folder:



--- python sample\_data\_generation.py


Running the Program

Run the main Python program to process images and generate the packed PDF:

--- python task\_1\_starter\_code.py

This will create an output.pdf file with images placed into A4 pages.


Implementation Details:

Image Preprocessing: Images are opened, transparent backgrounds removed by compositing on white, and cropped to visible bounding boxes.

Packing Logic: Each image is fit and centered on a separate A4 PDF page scaled down preserving aspect ratio.

Compression: A separate function compress\_images is implemented to optionally compress images before packing, reducing the final PDF size.

Temporary File Handling: Preprocessed images are saved temporarily for compatibility with ReportLab's PDF generation.



Project Status and Known Issues

I have implemented the image packing solution to the best of my ability within the given timeframe and resources. The program generates a PDF by preprocessing images and attempting to pack them onto A4-sized pages.
However, there is a known issue: the generated output PDF appears corrupted and cannot be opened with standard PDF viewers. Despite multiple debugging attempts — including ensuring images are processed properly, using temporary files, and validating scaling — the cause of the corruption could not be fully resolved before the deadline.
I am sharing the current working code with detailed comments and explanations of my approach. I believe this demonstrates my understanding of the problem, my coding skills, and my effort, even though the final output could not be fully realized.

Thank you for considering my submission. I look forward to any feedback and learning opportunities from this experience.


Contact

Mubeen Ahmad Shaik

Email: smubeen668@gmail.com

