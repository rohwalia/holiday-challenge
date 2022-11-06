# holiday-challenge

---

#### Basic information

For the challenge the programming language Python was used, since it is the one I am most familiar with. With the streamlit library, which is an open-source app framework, a web application was created.

In the sidebar some general parameters (e.g. duration of holiday) can be set for the holiday to Mallorca. By pressing the "Find" button, the offers dataset is filtered according to the parameters and results (if there are any) are displayed in view 1 (only one offer per hotel is shown). There is the possibility to set more subtle parameters (e.g. roomtype) and limit the number of results shown. By clicking on the corresponding "More Offers" button, view 2 (all offers for one hotel) is shown. To switch back to view 1, the button "Back" at the end of the page can be pressed.

---

#### Details on implementation

The main file of this web application is the comparison.py file. Instead of reading the offers.csv file, the file was divided into multiple smaller parquet files, where parquet is a columnar file format designed for efficient data storage and retrieval. The division was done with the preprocessing.py file and the parquet files can be found in the directory parquet in the repository. To handle and filter data at this scale and not overwhelm the system storage the library dask was used. Still, on my system an average query takes around 1 minute to finish.

---

#### How to run web application

The required libraries can be found in the requirements.txt file and can be easily installed using pip. Then using the terminal, navigate to the directory in which comparison.py is located and run with the command "streamlit run comparison.py". Then the web application is exectued locally, popping up as a browser tab. Alternatively, the web application can also be accessed publicly: https://rohwalia-holiday-challenge-comparison-7ninck.streamlit.app/

Since the latter is hosted on streamlit cloud, only limited resources are available for computation. Hence, the time needed to display results might be even longer.
