---
name: Bug report
about: Create a report to help us improve
title: ''
labels: ''
assignees: ''

---

# Help us help you! Providing detailed information will help us solve the issue quickly with minimal back-and-forth. Make sure your issue includes the following information, or it may be closed automatically:

1. Paste the URL you're trying to access here: [PASTE URL HERE]
2. Paste your code inside the triple quotes below:
    ```py

    ```
3. Paste the HTML of the page in the triple quotes below (this is the output of `driver.page_source` on Selenium or `page.content()` on Playwright):
```html

```
4. Paste the full console logs set where log_level is set to DEBUG into the triple quotes below  (if you're not sure how to do this, instructions are below):
```

```

# How to set log_level to DEBUG:
Add the following lines to the top of your python script:
```py
import logging
logging.basicConfig(level=logging.DEBUG)
```

# Pull request
**Please consider cloning this repository and making adjustments as needed to the code. Often times issues can be fixed very quickly by making very small adjustments to the code.**
