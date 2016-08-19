# Extracting Experience from Resumes

Use the **experience.py** script to extract experience from resume text. The script accepts **txt** files and outputs total years of experience. See sample code below to see how it can be run from python.

```python
from experience import GetExp


ge = GetExp()

# If you want to use current date to use the current date to get experience (default)
ge.chain_exp("sample_file_name.txt")

# If you want to use the application date to get experience (get the application date string from the postgres database)
ge.chain_exp("sample_file_name.txt", cur_date="application_date_from_postgres")
```
