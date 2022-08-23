from hashlib import new
import pandas as pd


def get_csv_data(file_location):
    df = pd.read_csv(file_location)
    return df


def isColAvailable(col_name, colOnSheet):
    if col_name in colOnSheet:
        return True
    return False


def availableCols(df):
    colOnSheet = list(df.columns)
    expectedCols = {
        "Company Name": ["Company Name"],
        "Domain": ["Domain"],
        "Additional Domains": ["Additional Domains"],
        "Representative Name": ["AE/Rep Name"],
        "Representative Email": ["AE/Rep Email"],
        "Representative Phone": ["AE Phone"],
        "Representative Title": ["AE Title"],
        "Banner Title": ["Banner Title"],
        "Banner Subtitle": ["Banner Subtitle"],
        "Items Title": ["Items Title"],
        "Items Subtitle": ["Items Subtitle"]
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

    print(f"Columns on sheet: {colOnSheet}")
    return col_available, col_status


def sep_domains(domains: str, sep: str = '\n'):
    domains = domains.replace(' ', sep)
    domainsList = domains.split(sep)
    for _ in range(len(domainsList)):
        try:
            domainsList.remove('')
        except ValueError:
            continue
    return domainsList


def remove_nan(column):
    new_col = []
    for value in column:
        if value == 'nan':
            new_col.append('')
        else:
            new_col.append(value)

    return new_col


def dataCleansing(df):
    col_available, col_status = availableCols(df)
    newData = {}
    for col in col_available:
        temp = list(map(lambda x: str(x).strip(), df[col]))
        temp = remove_nan(temp)
        if len(temp) < 1:
            col_status[col] = False
            continue
        newData[col] = temp

    newData['Domain'] = list(map(sep_domains, newData['Domain']))

    if 'Additional Domains' in col_available:
        newData['Additional Domains'] = list(map(sep_domains, newData['Additional Domains']))

    return newData, col_status


def dataInfo(col_status):
    col_found = []
    col_not_found = []
    for col in col_status.keys():
        if col_status[col]:
            col_found.append(col)
        else:
            col_not_found.append(col)
    print(f"Columns found: {col_found}")
    print(f"Columns not found: {col_not_found}")
    return col_found

# main function


def getCleanData(file_location):
    df = get_csv_data(file_location)
    cleanData, column_status = dataCleansing(df)
    column2choose = dataInfo(column_status)
    return cleanData, column2choose


if __name__ == "__main__":
    csvFileLocation = "data/data.csv"

    df = get_csv_data(csvFileLocation)

    # Expected values
    personalizationExpectedValues = {
        "Company Name": ["Company Name", "Company Name\nHow they're referred to verbally"],
        "Domain": ["Domain", "Domain\n(no leading letters)"],
        "Additional Domains": ["Additional Domains"],
        "Representative Name": ["AE/Rep Name", "Contact card\nAE/Rep Name"],
        "Representative Email": ["AE/Rep Email", "Contact card\nAE/Rep Email"],
        "Representative Phone": ["AE Phone", "AE Phone Number"],
        "Representative Title": ["AE Title", "AE Title"],
        "Banner Title": ["Banner Title", "Banner Title\nTitle Case 85 char"],
        "Banner Subtitle": ["Banner Subtitle", "Banner Subtitle\n500 char"],
        "Items Title": ["Items Title", "Items Title\nTitle Case 80 char"],
        "Items Subtitle": ["Items Subtitle", "Items Subtitle\n375 char"]
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
