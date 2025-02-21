[Global Trade](../)
# Exiobase API Pull

## How to Use

Note : It's always recommended to work with a new environment when working with a new project


1. Install the requirements.txt file :
   ```
   pip install -r requirements.txt
   ```
2. Create a folder to store the required files (preferably in the same folder as `maps.py`
3. Update the folder information in Line 129 and 154 respectively
   <img style="width:100%;max-width:1000px" alt="image" src="https://github.com/user-attachments/assets/6cd9011a-081c-4f0d-8b9f-d391723ae2e0">

4. In the terminal, go to the folder where you've stored `maps.py` and run the fastapi app as :
   ```
   fastapi dev maps.py
   ```
5. It will open the webpage with the interactive map of emissions of 2017. You can view other years by passing the `/year` after your localhost server like so:
<img style="width:100%;max-width:1000px" alt="image" src="https://github.com/user-attachments/assets/ecd99874-da76-432b-a698-97594614dae7">


## Notes on Execution Time and Space Requirements

The program uses EXIOBASE files downloaded from pymrio, and these are huge files that take a really long time to download and extract. But the program is written such that it downloads the database of that year, does the processing, and saves a very small .feather file. It then also deletes all the bigger files that were downloaded with pymrio. So the first download of a particular year takes a long time, but then the consecutive runs are much faster. 
