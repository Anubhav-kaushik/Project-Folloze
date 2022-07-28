from dataCleansing import getCleanData
from output import speak
from input2folloze import PersonalizationBot
from follozeXtra import createFollozeLinks
import os
import pandas as pd

def getFiles():
    allFiles = os.listdir('data')
    notCSVFile = []
    for i in range(len(allFiles)):
        if allFiles[i][-4:] != '.csv':
            notCSVFile.append(allFiles[i])

    for file in notCSVFile:
        allFiles.remove(file)

    return allFiles

def isPersonalizePossible(colsAvailable):
    if 'Domain' in colsAvailable:
        return True
    return False

def checkPossibleFields(colsAvailable, what2personalize):
    possiblePersonalizes = []
    notPossiblePersonalizes = []
    for field in what2personalize:
        if (field == 'Banner') or (field == 'Logo') or (field == 'Leading Asset') or (field == 'Asset') or (field == 'Logo Dummy'):
            possiblePersonalizes.append(field)
        elif (field == 'Banner Title') and (field in colsAvailable):
            possiblePersonalizes.append(field)
        elif (field == 'Banner Subtitle') and (field in colsAvailable):
            possiblePersonalizes.append(field)
        elif (field == 'Items Title') and (field in colsAvailable):
            possiblePersonalizes.append(field)
        elif (field == 'Items Subtitle') and (field in colsAvailable):
            possiblePersonalizes.append(field)
        elif (field == 'Contact Card') and ('AE/Rep Email' in colsAvailable):
            possiblePersonalizes.append('AE/Rep Email')
        else:
            notPossiblePersonalizes.append(field)

    return possiblePersonalizes, notPossiblePersonalizes

def startPersonalize():
    availableCSVFiles = getFiles()
    numberFiles = {i+1: file for i, file in enumerate(availableCSVFiles)}
    print('Select the file you want to personalize')
    for i, file in enumerate(availableCSVFiles):
        print(f'{i+1}. {file}')
    fileNumber = int(input('Enter the corresponding number of the file you want to personalize: '))
    fileName = numberFiles[fileNumber]
    print(f'You selected {fileName}')
    print('\n')
    print('Please wait while we are processing your data...')
    print('\n')
    cleanData, columnsAvailable = getCleanData(f'data/{fileName}')

    # check if personalization is possible
    if not isPersonalizePossible(columnsAvailable):
        print('\n')
        print('Domain column is not available. Personalization is not possible. Program is terminating...')
        speak('Domain column is not available. Personalization is not possible. Program is terminating...')
        print('\n')
        return

    print('\n')
    print('Select the fields you want to personalize')
    what2personalizeChoices = [
        'Banner',
        'Logo',
        'Logo Dummy',
        'Banner Title',
        'Banner Subtitle',
        'Items Title',
        'Items Subtitle',
        'Leading Asset',
        'Asset',
        'Contact Card'
    ]
    for i, col in enumerate(what2personalizeChoices):
        print(f'{i+1}. {col}')

    columnNumber = input('Enter the corresponding number of the fields you want to personalize(separate the numbers by ","): ')
    if columnNumber.strip() == '':
        print('\n')
        print('No fields to personalize. Program is terminating...')
        speak('No fields to personalize. Program is terminating...')
        print('\n')
        return
    columnNumber = columnNumber.split(',')
    columnNumbers = [int(i) for i in columnNumber]
    fieldNames = [what2personalizeChoices[i-1] for i in columnNumbers]

    possibleFields, notPossibleFields = checkPossibleFields(columnsAvailable, fieldNames)

    if len(notPossibleFields) > 0:
        print('\n')
        print('The following fields are not possible to personalize:')
        speak('The following fields are not possible to personalize:')

        for field in notPossibleFields:
            print(f'{field}')
            speak(f'{field}')

        print('\n')
        isContinue = input('Do you want to continue with the available fields? (y/n): ')
        if isContinue == 'n':
            print('\n')
            print('Program is terminating...')
            speak('Program is terminating...')
            print('\n')
            return

    # create bot for every field
    bots = {}
    for field in possibleFields:
        bots[field] = PersonalizationBot(cleanData, field)
        print(f'Open {field} personalization window. Bot is ready to personalize.\nPress Ctrl+q to start')
        bots[field].personalize()

    wantFollozeLinks = input('Do you want to create folloze links (y/n): ').lower()
    if wantFollozeLinks == 'y':
        baseboardLink = input('Enter the baseboard link: ')
        follozeLinks = createFollozeLinks(baseboardLink, cleanData['Domain'])
        cleanData['Folloze Links'] = follozeLinks


startPersonalize()

