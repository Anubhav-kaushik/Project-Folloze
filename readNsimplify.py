import pandas as pd

def get_csv_data(file_location):
    df = pd.read_csv(file_location)
    return df

def isColAvailable(col_name, colOnSheet):
    if col_name not in colOnSheet:
        return False
    return True

def availableCols(df):
    colOnSheet = list(df.columns)
    expectedCols = {
        "Company Name": ["Company Name", "Company"],
        "Domain": ["Domain", "Domain Name"],
        "Representative Name": ["AE Name", "AE"],
        "Representative Email": ["AE Email", "AE Email Address"],
        "Representative Phone": ["AE Phone", "AE Phone Number"],
        "Representative Title": ["AE Title", "AE Title"],
        "Banner Title": ["Banner Title"],
        "Banner Subtitle": ["Banner Subtitle"],
        "Items Title": ["Items Title"],
        "Items Subtitle": ["Items Subtitle"],
    }

    col_status = {}
    col_available = []
    for key in expectedCols.keys():
        for col in expectedCols[key]:
            if isColAvailable(col, colOnSheet):
                col_available.append(col)
                col_status[col] = True
                break
        else:
            col_status[col] = False
    
    return col_available, col_status

def sep_domains(domains: str, sep: str='\n'):
    domains = domains.replace(' ', sep)
    domainsList = domains.split(sep)
    for _ in range(len(domainsList)):
        try:
            domainsList.remove('')
        except ValueError:
            continue
    return domainsList

def dataCleansing(df):
    col_available, col_status = availableCols(df)
    newData = {}
    for col in col_available:
        temp = list(map(lambda x: x.strip(), df[col]))
        newData[col] = temp

    newData['Domain'] = list(map(sep_domains, newData['Domain']))

    return newData, col_status

if __name__ == "__main__":
    csvFileLocation = "../data/csv/data.csv"
    
    df = get_csv_data(csvFileLocation)
    
    colHeadings = list(df.head(0)) # Get the column headings

    # Expected values
    personalizationExpectedValues = {
        "Company Name": ["Company Name", "Company"],
        "Domain": ["Domain", "Domain Name"],
        "Representative Name": ["AE Name", "AE"],
        "Representative Email": ["AE Email", "AE Email Address"],
        "Representative Phone": ["AE Phone", "AE Phone Number"],
        "Representative Title": ["AE Title", "AE Title"],
        "Banner Title": ["Banner Title"],
        "Banner Subtitle": ["Banner Subtitle"],
        "Items Title": ["Items Title"],
        "Items Subtitle": ["Items Subtitle"],
    }

    baseboardExpectedValues = {
        "Banner Title": ["Banner Title"],
        "Banner Subtitle": ["Banner Subtitle"],
        "CTA text": ["CTA text"],
        "Items Title": ["Items Title"],
        "Items Subtitle": ["Items Subtitle"],
        "Promo Title": ["Promo Title"],
        "Promo Subtitle": ["Promo Subtitle"],
    }
