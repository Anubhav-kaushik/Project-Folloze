
# Create folloze links
def createFollozeLink(baseboardLink, accountDomains):
    return f'{baseboardLink}?dom={accountDomains[0]}&utm_source=TEST'

def createFollozeLinks(baseboardLink, accountsDomains):
    follozeLinks = []
    for accountDomains in accountsDomains:
        follozeLinks.append(createFollozeLink(baseboardLink, accountDomains))

    return follozeLinks
